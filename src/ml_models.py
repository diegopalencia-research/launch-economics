"""
============================================================
PROJECT ALPHA: LAUNCH ECONOMICS
Machine Learning Models Module
============================================================
Predictive modeling utilities for mission success prognostication
using Random Forest classification with sacred aesthetic reporting.

Author: [Your Name]
Date: 2026-06-06
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import (classification_report, confusion_matrix, 
                            accuracy_score, precision_score, recall_score, f1_score,
                            roc_curve, auc, precision_recall_curve)
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
import warnings
warnings.filterwarnings('ignore')


class MissionPrognosticator:
    """
    Machine learning pipeline for predicting SpaceX Falcon 9 landing success.

    Implements Random Forest classification with feature importance analysis,
    cross-validation, and sacred aesthetic reporting.
    """

    def __init__(self, random_state: int = 42):
        """
        Initialize the prognosticator.

        Parameters:
        -----------
        random_state : int
            Random seed for reproducibility
        """
        self.random_state = random_state
        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.feature_names = None
        self.scaler = StandardScaler()
        self.metrics = {}

    def prepare_data(self, X: pd.DataFrame, y: pd.Series,
                    test_size: float = 0.3,
                    stratify: bool = True) -> tuple:
        """
        Prepare train/test splits with optional stratification.

        Parameters:
        -----------
        X : pd.DataFrame
            Feature matrix
        y : pd.Series
            Target vector
        test_size : float
            Proportion for test set
        stratify : bool
            Whether to stratify by target class

        Returns:
        --------
        tuple
            (X_train, X_test, y_train, y_test)
        """
        self.feature_names = X.columns.tolist()

        stratify_param = y if stratify else None

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state,
            stratify=stratify_param
        )

        print(f"✅ Data prepared: Train {len(self.X_train)} | Test {len(self.X_test)}")
        print(f"   Class distribution - Train: {dict(self.y_train.value_counts())}")
        print(f"   Class distribution - Test: {dict(self.y_test.value_counts())}")

        return self.X_train, self.X_test, self.y_train, self.y_test

    def train_model(self, n_estimators: int = 100,
                   max_depth: int = 5,
                   min_samples_split: int = 2,
                   min_samples_leaf: int = 1,
                   class_weight: str = 'balanced') -> RandomForestClassifier:
        """
        Train Random Forest classifier.

        Parameters:
        -----------
        n_estimators : int
            Number of trees in forest
        max_depth : int
            Maximum tree depth
        min_samples_split : int
            Minimum samples for node split
        min_samples_leaf : int
            Minimum samples in leaf node
        class_weight : str
            Class weight balancing strategy

        Returns:
        --------
        RandomForestClassifier
            Trained model
        """
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            class_weight=class_weight,
            random_state=self.random_state,
            n_jobs=-1
        )

        self.model.fit(self.X_train, self.y_train)

        print(f"✅ Model trained: {n_estimators} estimators, max_depth={max_depth}")
        print(f"   Feature count: {len(self.feature_names)}")

        return self.model

    def evaluate_model(self) -> dict:
        """
        Comprehensive model evaluation with multiple metrics.

        Returns:
        --------
        dict
            Dictionary of evaluation metrics
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train_model() first.")

        y_pred = self.model.predict(self.X_test)
        y_prob = self.model.predict_proba(self.X_test)[:, 1]

        self.metrics = {
            'accuracy': accuracy_score(self.y_test, y_pred),
            'precision': precision_score(self.y_test, y_pred, zero_division=0),
            'recall': recall_score(self.y_test, y_pred, zero_division=0),
            'f1_score': f1_score(self.y_test, y_pred, zero_division=0),
            'true_positives': int(((y_pred == 1) & (self.y_test == 1)).sum()),
            'true_negatives': int(((y_pred == 0) & (self.y_test == 0)).sum()),
            'false_positives': int(((y_pred == 1) & (self.y_test == 0)).sum()),
            'false_negatives': int(((y_pred == 0) & (self.y_test == 1)).sum()),
        }

        # ROC AUC
        fpr, tpr, _ = roc_curve(self.y_test, y_prob)
        self.metrics['roc_auc'] = auc(fpr, tpr)

        # Cross-validation
        cv_scores = cross_val_score(self.model, 
                                    pd.concat([self.X_train, self.X_test]),
                                    pd.concat([self.y_train, self.y_test]),
                                    cv=StratifiedKFold(n_splits=5, shuffle=True, 
                                                      random_state=self.random_state),
                                    scoring='accuracy')
        self.metrics['cv_mean'] = cv_scores.mean()
        self.metrics['cv_std'] = cv_scores.std()

        print("\n" + "="*60)
        print("⟁ MODEL EVALUATION RESULTS ⟁")
        print("="*60)
        print(f"   Accuracy:  {self.metrics['accuracy']:.3f}")
        print(f"   Precision: {self.metrics['precision']:.3f}")
        print(f"   Recall:    {self.metrics['recall']:.3f}")
        print(f"   F1-Score:  {self.metrics['f1_score']:.3f}")
        print(f"   ROC-AUC:   {self.metrics['roc_auc']:.3f}")
        print(f"   CV Mean:   {self.metrics['cv_mean']:.3f} (±{self.metrics['cv_std']:.3f})")
        print("="*60)

        return self.metrics

    def get_feature_importance(self) -> pd.DataFrame:
        """
        Extract and rank feature importance from trained model.

        Returns:
        --------
        pd.DataFrame
            Feature importance rankings
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train_model() first.")

        importance = pd.DataFrame({
            'Feature': self.feature_names,
            'Importance': self.model.feature_importances_
        }).sort_values('Importance', ascending=False)

        importance['Cumulative'] = importance['Importance'].cumsum()
        importance['Rank'] = range(1, len(importance) + 1)

        print("\n✦ Feature Importance Rankings:")
        for _, row in importance.head(10).iterrows():
            bar = '█' * int(row['Importance'] * 50)
            print(f"   {row['Rank']:2d}. {row['Feature']:25s} {row['Importance']:.4f} {bar}")

        return importance

    def predict_mission(self, features: dict) -> dict:
        """
        Predict success probability for a hypothetical mission.

        Parameters:
        -----------
        features : dict
            Dictionary of feature values matching training features

        Returns:
        --------
        dict
            Prediction results with probability and confidence
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train_model() first.")

        # Create feature vector
        feature_vector = np.zeros(len(self.feature_names))
        for i, feat in enumerate(self.feature_names):
            if feat in features:
                feature_vector[i] = features[feat]

        # Predict
        prediction = self.model.predict([feature_vector])[0]
        probability = self.model.predict_proba([feature_vector])[0]

        result = {
            'prediction': int(prediction),
            'success_probability': float(probability[1]),
            'failure_probability': float(probability[0]),
            'confidence': float(max(probability)),
            'is_success': bool(prediction == 1)
        }

        return result

    def plot_confusion_matrix_sacred(self, figsize: tuple = (10, 8)) -> plt.Figure:
        """
        Create sacred aesthetic confusion matrix visualization.

        Parameters:
        -----------
        figsize : tuple
            Figure dimensions

        Returns:
        --------
        plt.Figure
            Confusion matrix figure
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train_model() first.")

        y_pred = self.model.predict(self.X_test)
        cm = confusion_matrix(self.y_test, y_pred)

        fig, ax = plt.subplots(figsize=figsize, facecolor='#0A0A1A')
        ax.set_facecolor('#0A0A1A')

        # Custom colors
        colors = ['#0A0A1A', '#4A0E4E', '#D4AF37', '#00BCD4']

        # Create custom colormap
        from matplotlib.colors import LinearSegmentedColormap
        cmap = LinearSegmentedColormap.from_list('sacred_cm', 
                                                ['#0A0A1A', '#4A0E4E', '#D4AF37'])

        im = ax.imshow(cm, interpolation='nearest', cmap=cmap)

        # Add text annotations
        thresh = cm.max() / 2.
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, format(cm[i, j], 'd'),
                       ha="center", va="center",
                       color="#FFF8E1" if cm[i, j] > thresh else "#D4AF37",
                       fontsize=20, fontweight='bold')

        # Labels
        classes = ['Failure', 'Success']
        ax.set_xticks(np.arange(len(classes)))
        ax.set_yticks(np.arange(len(classes)))
        ax.set_xticklabels(classes, color='#FFF8E1', fontsize=12)
        ax.set_yticklabels(classes, color='#FFF8E1', fontsize=12)

        ax.set_xlabel('Predicted Label', color='#FFF8E1', fontsize=14)
        ax.set_ylabel('True Label', color='#FFF8E1', fontsize=14)
        ax.set_title('⟁ Sacred Confusion Matrix ⟁', 
                    color='#D4AF37', fontsize=16, fontweight='bold', pad=20)

        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, shrink=0.8)
        cbar.set_label('Count', color='#FFF8E1')
        cbar.ax.yaxis.set_tick_params(color='#FFF8E1')
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#FFF8E1')

        # Add metrics box
        metrics_text = (f"Accuracy: {self.metrics.get('accuracy', 0):.3f}\n"
                       f"Precision: {self.metrics.get('precision', 0):.3f}\n"
                       f"Recall: {self.metrics.get('recall', 0):.3f}\n"
                       f"F1: {self.metrics.get('f1_score', 0):.3f}")

        box = FancyBboxPatch((1.15, 0.3), 0.3, 0.4,
                            boxstyle="round,pad=0.02,rounding_size=0.02",
                            facecolor='#4A0E4E', edgecolor='#D4AF37',
                            alpha=0.8, linewidth=2, transform=ax.transAxes)
        ax.add_patch(box)
        ax.text(1.3, 0.5, metrics_text, ha='center', va='center',
               color='#FFF8E1', fontsize=10, fontweight='bold',
               transform=ax.transAxes)

        plt.tight_layout()
        return fig

    def plot_feature_importance_sacred(self, figsize: tuple = (12, 8)) -> plt.Figure:
        """
        Create sacred aesthetic feature importance visualization.

        Parameters:
        -----------
        figsize : tuple
            Figure dimensions

        Returns:
        --------
        plt.Figure
            Feature importance figure
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train_model() first.")

        importance = self.get_feature_importance()

        fig, ax = plt.subplots(figsize=figsize, facecolor='#0A0A1A')
        ax.set_facecolor('#0A0A1A')

        # Plot top 10 features
        top_n = min(10, len(importance))
        top_features = importance.head(top_n).sort_values('Importance', ascending=True)

        colors = plt.cm.dmt_vision(np.linspace(0.2, 0.8, top_n))

        bars = ax.barh(range(top_n), top_features['Importance'],
                      color=colors, edgecolor='#D4AF37', linewidth=1.5, height=0.6)

        ax.set_yticks(range(top_n))
        ax.set_yticklabels(top_features['Feature'], color='#FFF8E1', fontsize=11)
        ax.set_xlabel('Importance Score', color='#FFF8E1', fontsize=12)
        ax.set_title('⟁ Sacred Feature Importance ⟁', 
                    color='#D4AF37', fontsize=16, fontweight='bold', pad=20)

        ax.tick_params(colors='#FFF8E1')
        for spine in ax.spines.values():
            spine.set_color('#D4AF37')
            spine.set_linewidth(0.8)

        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, top_features['Importance'])):
            ax.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height()/2,
                   f'{val:.4f}', va='center', color='#FFF8E1', fontsize=9)

        plt.tight_layout()
        return fig

    def run_full_pipeline(self, X: pd.DataFrame, y: pd.Series) -> dict:
        """
        Execute complete ML pipeline: prepare, train, evaluate.

        Parameters:
        -----------
        X : pd.DataFrame
            Feature matrix
        y : pd.Series
            Target vector

        Returns:
        --------
        dict
            Complete results dictionary
        """
        self.prepare_data(X, y)
        self.train_model()
        self.evaluate_model()
        importance = self.get_feature_importance()

        results = {
            'metrics': self.metrics,
            'feature_importance': importance.to_dict(),
            'model_params': self.model.get_params(),
            'feature_count': len(self.feature_names)
        }

        print("\n✅ Full ML pipeline completed successfully!")

        return results


if __name__ == '__main__':
    # Example usage
    from data_pipeline import SpaceXDataPipeline

    pipeline = SpaceXDataPipeline('data/spacex_raw.csv')
    df = pipeline.run_full_pipeline()
    X, y = pipeline.prepare_ml_data(df)

    prognosticator = MissionPrognosticator()
    results = prognosticator.run_full_pipeline(X, y)

    # Save visualizations
    fig_cm = prognosticator.plot_confusion_matrix_sacred()
    fig_cm.savefig('dashboard/sacred_confusion_matrix.png', 
                  dpi=150, facecolor='#0A0A1A', bbox_inches='tight')
    print("✅ Sacred Confusion Matrix saved!")

    fig_fi = prognosticator.plot_feature_importance_sacred()
    fig_fi.savefig('dashboard/sacred_feature_importance.png',
                  dpi=150, facecolor='#0A0A1A', bbox_inches='tight')
    print("✅ Sacred Feature Importance saved!")

    # Example prediction
    sample_features = {
        'PayloadMass': 5000,
        'ReusedCount': 3,
        'Block': 5.0,
        'DaysSinceFirst': 2000,
        'Orbit_GTO': 1,
        'Orbit_LEO': 0,
    }

    prediction = prognosticator.predict_mission(sample_features)
    print(f"\n✦ Mission Prediction:")
    print(f"   Success Probability: {prediction['success_probability']:.1%}")
    print(f"   Confidence: {prediction['confidence']:.1%}")
    print(f"   Verdict: {'✦ SUCCESS PROBABLE' if prediction['is_success'] else '⚠ CAUTION ADVISED'}")
