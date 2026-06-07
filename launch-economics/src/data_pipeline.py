"""
============================================================
PROJECT ALPHA: LAUNCH ECONOMICS
Data Pipeline Module
============================================================
Sacred data ingestion, cleaning, and transformation utilities
for SpaceX Falcon 9 launch economics analysis.

Author: [Your Name]
Date: 2026-06-06
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Tuple, Optional, Dict
import warnings
warnings.filterwarnings('ignore')


class SpaceXDataPipeline:
    """
    ETL pipeline for SpaceX Falcon 9 launch data.

    Handles data ingestion, cleaning, feature engineering,
    and preparation for analytical and machine learning workflows.
    """

    def __init__(self, data_path: str = 'data/spacex_raw.csv'):
        """
        Initialize pipeline with data source path.

        Parameters:
        -----------
        data_path : str
            Path to raw CSV data file
        """
        self.data_path = data_path
        self.raw_data = None
        self.processed_data = None
        self.features = None
        self.target = None

    def load_data(self) -> pd.DataFrame:
        """
        Load raw data from CSV source.

        Returns:
        --------
        pd.DataFrame
            Raw launch data with all original columns
        """
        self.raw_data = pd.read_csv(self.data_path)
        print(f"✅ Loaded {len(self.raw_data)} records with {len(self.raw_data.columns)} features")
        return self.raw_data

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize raw data.

        Operations:
        - Date parsing and temporal feature extraction
        - Null value handling for landing pad information
        - Categorical standardization
        - Outlier detection and flagging

        Parameters:
        -----------
        df : pd.DataFrame
            Raw data frame

        Returns:
        --------
        pd.DataFrame
            Cleaned data frame
        """
        df_clean = df.copy()

        # Parse dates
        df_clean['Date'] = pd.to_datetime(df_clean['Date'])
        df_clean['Year'] = df_clean['Date'].dt.year
        df_clean['Month'] = df_clean['Date'].dt.month
        df_clean['Quarter'] = df_clean['Date'].dt.quarter
        df_clean['DayOfWeek'] = df_clean['Date'].dt.dayofweek
        df_clean['DaysSinceFirst'] = (df_clean['Date'] - df_clean['Date'].min()).dt.days

        # Handle nulls in landing pad
        df_clean['LandingPad'] = df_clean['LandingPad'].fillna('None')

        # Standardize categorical variables
        df_clean['Orbit'] = df_clean['Orbit'].str.upper().str.strip()
        df_clean['LaunchSite'] = df_clean['LaunchSite'].str.strip()
        df_clean['Outcome'] = df_clean['Outcome'].str.strip()

        # Create binary success indicator
        df_clean['Success'] = df_clean['Outcome'].apply(
            lambda x: 1 if x in ['True ASDS', 'True RTLS', 'True Ocean'] else 0
        )

        # Calculate cumulative metrics
        df_clean = df_clean.sort_values('Date').reset_index(drop=True)
        df_clean['CumulativeLaunches'] = range(1, len(df_clean) + 1)
        df_clean['RollingSuccessRate'] = df_clean['Success'].expanding().mean()

        # Cost calculations
        df_clean['EstimatedCost'] = 62.0
        df_clean.loc[df_clean['Reused'] == True, 'EstimatedCost'] = 50.0
        df_clean.loc[df_clean['PayloadMass'] > 10000, 'EstimatedCost'] += 10.0
        df_clean['CompetitorCost'] = 165.0
        df_clean['CostPerKg'] = (df_clean['EstimatedCost'] * 1_000_000) / df_clean['PayloadMass']

        # Cumulative savings
        df_clean['CumulativeSavings'] = (df_clean['CompetitorCost'] - df_clean['EstimatedCost']).cumsum()

        print(f"✅ Cleaned data: {len(df_clean)} records, {len(df_clean.columns)} features")
        return df_clean

    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create engineered features for machine learning.

        Features:
        - Orbital dummy variables (LEO, GTO, ISS, PO, SSO, MEO)
        - Launch site dummy variables
        - Temporal interaction features
        - Payload mass bins
        - Reuse efficiency ratios

        Parameters:
        -----------
        df : pd.DataFrame
            Cleaned data frame

        Returns:
        --------
        pd.DataFrame
            Data frame with engineered features
        """
        df_feat = df.copy()

        # Orbital dummy variables
        for orbit in df_feat['Orbit'].unique():
            df_feat[f'Orbit_{orbit}'] = (df_feat['Orbit'] == orbit).astype(int)

        # Launch site dummy variables
        for site in df_feat['LaunchSite'].unique():
            site_clean = site.replace(' ', '_').replace('-', '_')
            df_feat[f'Site_{site_clean}'] = (df_feat['LaunchSite'] == site).astype(int)

        # Payload mass categories
        df_feat['PayloadCategory'] = pd.cut(
            df_feat['PayloadMass'],
            bins=[0, 2000, 5000, 10000, 20000],
            labels=['Light', 'Medium', 'Heavy', 'SuperHeavy']
        )

        # Reuse efficiency (flights per booster)
        df_feat['ReuseEfficiency'] = df_feat['ReusedCount'] / (df_feat['ReusedCount'].max() + 1)

        # Temporal features
        df_feat['IsWeekend'] = (df_feat['DayOfWeek'] >= 5).astype(int)
        df_feat['IsYearEnd'] = (df_feat['Month'] >= 11).astype(int)

        # Interaction features
        df_feat['Payload_x_Reuse'] = df_feat['PayloadMass'] * df_feat['ReusedCount']
        df_feat['Block_x_Days'] = df_feat['Block'] * df_feat['DaysSinceFirst']

        print(f"✅ Engineered {len(df_feat.columns) - len(df.columns)} new features")
        return df_feat

    def prepare_ml_data(self, df: pd.DataFrame, 
                       target_col: str = 'Success',
                       feature_cols: Optional[list] = None) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepare data for machine learning.

        Parameters:
        -----------
        df : pd.DataFrame
            Feature-engineered data frame
        target_col : str
            Name of target variable column
        feature_cols : list, optional
            Specific feature columns to use. If None, uses numeric columns

        Returns:
        --------
        Tuple[pd.DataFrame, pd.Series]
            Feature matrix X and target vector y
        """
        if feature_cols is None:
            # Auto-select numeric features
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            exclude_cols = ['FlightNumber', 'Longitude', 'Latitude', target_col]
            feature_cols = [c for c in numeric_cols if c not in exclude_cols]

        X = df[feature_cols].fillna(0)
        y = df[target_col]

        self.features = X
        self.target = y

        print(f"✅ ML data prepared: X shape {X.shape}, y shape {y.shape}")
        print(f"   Features: {len(feature_cols)} | Target: {target_col}")
        return X, y

    def run_full_pipeline(self) -> pd.DataFrame:
        """
        Execute complete ETL pipeline.

        Returns:
        --------
        pd.DataFrame
            Fully processed data ready for analysis
        """
        self.load_data()
        cleaned = self.clean_data(self.raw_data)
        engineered = self.engineer_features(cleaned)
        self.processed_data = engineered
        return engineered

    def get_summary_stats(self) -> Dict:
        """
        Generate comprehensive summary statistics.

        Returns:
        --------
        Dict
            Dictionary of summary statistics
        """
        if self.processed_data is None:
            self.run_full_pipeline()

        df = self.processed_data

        stats = {
            'total_launches': len(df),
            'date_range': (df['Date'].min().strftime('%Y-%m-%d'), 
                          df['Date'].max().strftime('%Y-%m-%d')),
            'success_rate': df['Success'].mean(),
            'reused_count': int(df['Reused'].sum()),
            'avg_payload_mass': df['PayloadMass'].mean(),
            'avg_cost_per_kg': df['CostPerKg'].mean(),
            'total_savings': (df['CompetitorCost'] - df['EstimatedCost']).sum(),
            'orbits': df['Orbit'].unique().tolist(),
            'sites': df['LaunchSite'].unique().tolist(),
            'blocks': sorted(df['Block'].unique().tolist()),
        }

        return stats


if __name__ == '__main__':
    # Example usage
    pipeline = SpaceXDataPipeline('data/spacex_raw.csv')
    df = pipeline.run_full_pipeline()
    stats = pipeline.get_summary_stats()

    print("\n" + "="*60)
    print("⟁ PIPELINE EXECUTION COMPLETE ⟁")
    print("="*60)
    for key, value in stats.items():
        print(f"   {key}: {value}")
