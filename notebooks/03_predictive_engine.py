# %% [markdown]
# # ⟁ PROJECT ALPHA: LAUNCH ECONOMICS ⟁
# ## Notebook 3: The Predictive Engine — Machine Learning & Mission Prognostication
# 
# **Author:** [Your Name]  
# **Date:** 2026-06-06  
# **Domain:** Aerospace Data Science | Predictive Modeling | scikit-learn
# 
# ---
# 
# ## Executive Summary
# 
# This notebook constitutes the **third analytical chamber**: the Predictive Engine. Here we transition 
# from descriptive and inferential analysis to **predictive modeling**—training machine learning algorithms 
# to forecast mission outcomes based on operational parameters. We employ Random Forest classification, 
# a robust ensemble method well-suited to the mixed data types (continuous, ordinal, categorical dummies) 
# and moderate sample sizes characteristic of aerospace operational data.
# 
# ### Learning Objectives
# 1. Implement end-to-end ML pipeline: data preparation → model training → evaluation → deployment
# 2. Apply feature engineering for domain-specific predictive variables
# 3. Interpret model performance through multiple metrics (Accuracy, Precision, Recall, F1, ROC-AUC)
# 4. Analyze feature importance for business insight generation
# 5. Create production-ready prediction interface for operational decision support
# 
# ---

# %% [markdown]
# ## 1. Sacred Imports & Environment

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.gridspec as gridspec
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold, GridSearchCV
from sklearn.metrics import (classification_report, confusion_matrix, 
                            accuracy_score, precision_score, recall_score, f1_score,
                            roc_curve, auc, precision_recall_curve, roc_auc_score)
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Sacred color palette
SC = {
    'deep_void': '#0A0A1A', 'nebula_purple': '#4A0E4E', 'sacred_gold': '#D4AF37',
    'mystic_teal': '#0D7377', 'organic_emerald': '#1B5E20', 'dmt_coral': '#FF6B6B',
    'ethereal_blue': '#4FC3F7', 'amber_resin': '#FF8F00', 'sacred_crimson': '#B71C1C',
    'mushroom_ivory': '#FFF8E1', 'forest_deep': '#1B4332', 'lotus_pink': '#F8BBD0',
    'mandala_orange': '#FF5722', 'crystal_cyan': '#00BCD4', 'obsidian': '#1C1C1C',
}

# Register colormaps
import matplotlib
for name, colors in {
    'sacred_cm': ['#0A0A1A', '#4A0E4E', '#D4AF37'],
    'dmt_vision': ['#1A0033', '#4A0E4E', '#D4AF37', '#FF6B6B', '#00BCD4', '#FFF8E1'],
}.items():
    cmap = LinearSegmentedColormap.from_list(name, colors)
    try:
        matplotlib.colormaps.register(cmap=cmap)
    except ValueError:
        pass

# Global style
plt.rcParams['figure.facecolor'] = SC['deep_void']
plt.rcParams['axes.facecolor'] = SC['deep_void']
plt.rcParams['text.color'] = SC['mushroom_ivory']
plt.rcParams['axes.labelcolor'] = SC['mushroom_ivory']
plt.rcParams['xtick.color'] = SC['mushroom_ivory']
plt.rcParams['ytick.color'] = SC['mushroom_ivory']
plt.rcParams['axes.edgecolor'] = SC['sacred_gold']
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.color'] = 'rgba(212, 175, 55, 0.15)'
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Georgia', 'Times New Roman', 'DejaVu Serif']

print("✅ Predictive Engine environment initialized")
print("   scikit-learn version: imported successfully")

# %% [markdown]
# ## 2. Data Loading & Feature Engineering

# %%
df = pd.read_csv('data/spacex_raw.csv')

print("=" * 70)
print("⟁ PREDICTIVE ENGINE: THE MACHINE LEARNING CHAMBER ⟁")
print("=" * 70)
print(f"
📊 Raw Dataset: {len(df)} launches | {len(df.columns)} features")

# Feature engineering
print("
◈ Feature Engineering: The Alchemy of Prediction")
print("─" * 70)

# 2.1 Orbital dummy variables
orbits = df['Orbit'].unique()
for orbit in orbits:
    df[f'Orbit_{orbit}'] = (df['Orbit'] == orbit).astype(int)
print(f"   ✦ Created {len(orbits)} orbital dummy variables")

# 2.2 Launch site dummy variables
sites = df['LaunchSite'].unique()
for site in sites:
    site_clean = site.replace(' ', '_').replace('-', '_')
    df[f'Site_{site_clean}'] = (df['LaunchSite'] == site).astype(int)
print(f"   ✦ Created {len(sites)} launch site dummy variables")

# 2.3 Temporal features
df['Date'] = pd.to_datetime(df['Date'])
df['DaysSinceFirst'] = (df['Date'] - df['Date'].min()).dt.days
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Quarter'] = df['Date'].dt.quarter
df['DayOfWeek'] = df['Date'].dt.dayofweek
df['IsWeekend'] = (df['DayOfWeek'] >= 5).astype(int)
df['IsYearEnd'] = (df['Month'] >= 11).astype(int)
print(f"   ✦ Created 7 temporal features")

# 2.4 Interaction features
df['Payload_x_Reuse'] = df['PayloadMass'] * df['ReusedCount']
df['Block_x_Days'] = df['Block'] * df['DaysSinceFirst']
df['PayloadPerBlock'] = df['PayloadMass'] / df['Block']
print(f"   ✦ Created 3 interaction features")

# 2.5 Cumulative and rolling features
df = df.sort_values('Date').reset_index(drop=True)
df['CumulativeLaunches'] = range(1, len(df) + 1)
df['RollingSuccessRate'] = df['Success'].expanding().mean()
df['RollingPayloadMean'] = df['PayloadMass'].expanding().mean()
print(f"   ✦ Created 3 cumulative/rolling features")

# 2.6 Cost features
df['CostPerKg'] = (df['EstimatedCost'] * 1_000_000) / df['PayloadMass']
df['SavingsVsCompetitor'] = df['CompetitorCost'] - df['EstimatedCost']
print(f"   ✦ Created 2 cost-derived features")

print(f"
📊 Total Features: {len(df.columns)} (including target)")

# %% [markdown]
# ## 3. Feature Selection & Data Preparation

# %%
print("
" + "=" * 70)
print("◈ FEATURE SELECTION: THE DIVINATION RITUAL ◈")
print("=" * 70)

# Define feature set
feature_cols = [
    'PayloadMass', 'ReusedCount', 'Block', 'DaysSinceFirst',
    'Year', 'Month', 'Quarter', 'DayOfWeek', 'IsWeekend', 'IsYearEnd',
    'Payload_x_Reuse', 'Block_x_Days', 'PayloadPerBlock',
    'CumulativeLaunches', 'RollingSuccessRate', 'RollingPayloadMean',
    'CostPerKg', 'SavingsVsCompetitor'
]

# Add orbital dummies
orbital_dummies = [c for c in df.columns if c.startswith('Orbit_')]
feature_cols.extend(orbital_dummies)

# Add site dummies
site_dummies = [c for c in df.columns if c.startswith('Site_')]
feature_cols.extend(site_dummies)

# Target
X = df[feature_cols].fillna(0)
y = df['Success']

print(f"
📊 Feature Matrix: {X.shape[0]} samples × {X.shape[1]} features")
print(f"   Target Distribution: {dict(y.value_counts())}")
print(f"   Class Balance: {y.mean()*100:.1f}% positive (success)")

# Display feature descriptions
feature_descriptions = {
    'PayloadMass': 'Payload mass in kilograms',
    'ReusedCount': 'Number of prior flights for this booster',
    'Block': 'Vehicle generation (1.0–5.0)',
    'DaysSinceFirst': 'Days since program inception',
    'Year': 'Launch year',
    'Month': 'Launch month',
    'Quarter': 'Launch quarter',
    'DayOfWeek': 'Day of week (0=Monday)',
    'IsWeekend': 'Weekend launch flag',
    'IsYearEnd': 'Year-end launch flag',
    'Payload_x_Reuse': 'Interaction: payload × reuse count',
    'Block_x_Days': 'Interaction: block × temporal experience',
    'PayloadPerBlock': 'Payload normalized by generation',
    'CumulativeLaunches': 'Program flight count to date',
    'RollingSuccessRate': 'Cumulative success rate',
    'RollingPayloadMean': 'Cumulative mean payload mass',
    'CostPerKg': 'Estimated cost per kilogram',
    'SavingsVsCompetitor': 'Cost advantage vs. traditional providers',
}

print(f"
📋 Feature Descriptions:")
for feat in feature_cols[:10]:  # Show first 10
    desc = feature_descriptions.get(feat, 'Dummy variable')
    print(f"   • {feat:25s} — {desc}")

# %% [markdown]
# ## 4. Train/Test Split & Model Training

# %%
print("
" + "=" * 70)
print("◈ MODEL TRAINING: THE FOREST OF FORESIGHT ◈")
print("=" * 70)

# Stratified split to maintain class balance
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

print(f"
📊 Data Partition:")
print(f"   Training Set:   {len(X_train)} samples ({len(X_train)/len(X)*100:.1f}%)")
print(f"   Test Set:       {len(X_test)} samples ({len(X_test)/len(X)*100:.1f}%)")
print(f"   Train Balance:  {y_train.mean()*100:.1f}% positive")
print(f"   Test Balance:   {y_test.mean()*100:.1f}% positive")

# Initialize Random Forest with sacred parameters
# We constrain complexity to prevent overfitting given moderate sample size
rf_model = RandomForestClassifier(
    n_estimators=100,        # Forest size: balance between stability and computation
    max_depth=5,             # Tree depth: prevent overfitting
    min_samples_split=4,       # Minimum samples for split: ensure statistical validity
    min_samples_leaf=2,      # Minimum leaf samples: smooth predictions
    class_weight='balanced', # Handle class imbalance
    random_state=42,         # Reproducibility
    n_jobs=-1                # Parallel computation
)

print(f"
🌲 Random Forest Configuration:")
print(f"   Estimators:     {rf_model.n_estimators}")
print(f"   Max Depth:      {rf_model.max_depth}")
print(f"   Min Split:      {rf_model.min_samples_split}")
print(f"   Min Leaf:       {rf_model.min_samples_leaf}")
print(f"   Class Weight:   {rf_model.class_weight}")

# Train the model
rf_model.fit(X_train, y_train)
print(f"
✅ Model trained successfully on {len(X_train)} samples")

# %% [markdown]
# ## 5. Model Evaluation — The Oracle's Verdict

# %%
print("
" + "=" * 70)
print("◈ MODEL EVALUATION: THE ORACLE'S VERDICT ◈")
print("=" * 70)

# Predictions
y_pred = rf_model.predict(X_test)
y_prob = rf_model.predict_proba(X_test)[:, 1]

# Core metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)
roc_auc = roc_auc_score(y_test, y_prob)

# Confusion matrix components
tn = int(((y_pred == 0) & (y_test == 0)).sum())
fp = int(((y_pred == 1) & (y_test == 0)).sum())
fn = int(((y_pred == 0) & (y_test == 1)).sum())
tp = int(((y_pred == 1) & (y_test == 1)).sum())

print(f"
📊 Classification Metrics:")
print(f"   {'─'*50}")
print(f"   Accuracy:       {accuracy:.4f}  |  Correct predictions / Total")
print(f"   Precision:      {precision:.4f}  |  True positives / Predicted positives")
print(f"   Recall:         {recall:.4f}  |  True positives / Actual positives")
print(f"   F1-Score:       {f1:.4f}  |  Harmonic mean of Precision & Recall")
print(f"   ROC-AUC:        {roc_auc:.4f}  |  Area under ROC curve")
print(f"   {'─'*50}")

print(f"
📊 Confusion Matrix:")
print(f"   {'─'*40}")
print(f"                    Predicted")
print(f"   Actual    Failure    Success")
print(f"   Failure   {tn:5d}      {fp:5d}     (Specificity: {tn/(tn+fp):.3f})")
print(f"   Success   {fn:5d}      {tp:5d}     (Sensitivity: {tp/(tp+fn):.3f})")
print(f"   {'─'*40}")

# Cross-validation
print(f"
📊 Cross-Validation (5-Fold Stratified):")
cv_scores = cross_val_score(rf_model, X, y, 
                            cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
                            scoring='accuracy')
print(f"   Fold Scores:    {[f'{s:.4f}' for s in cv_scores]}")
print(f"   Mean Accuracy:  {cv_scores.mean():.4f} (±{cv_scores.std():.4f})")

# Classification report
print(f"
📊 Detailed Classification Report:")
print(classification_report(y_test, y_pred, 
                           target_names=['Failure', 'Success'],
                           digits=4))

# %% [markdown]
# ### 5.1 Visualization: The Sacred Confusion Matrix

# %%
fig, ax = plt.subplots(figsize=(10, 8), facecolor=SC['deep_void'])
ax.set_facecolor(SC['deep_void'])

cm = np.array([[tn, fp], [fn, tp]])

# Custom colormap
cmap = LinearSegmentedColormap.from_list('sacred_cm', 
                                        [SC['deep_void'], SC['nebula_purple'], SC['sacred_gold']])

im = ax.imshow(cm, interpolation='nearest', cmap=cmap)

# Text annotations
thresh = cm.max() / 2.
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        color = SC['mushroom_ivory'] if cm[i, j] > thresh else SC['sacred_gold']
        ax.text(j, i, format(cm[i, j], 'd'),
               ha="center", va="center",
               color=color, fontsize=28, fontweight='bold')

# Labels
classes = ['Failure', 'Success']
ax.set_xticks([0, 1])
ax.set_yticks([0, 1])
ax.set_xticklabels(classes, color=SC['mushroom_ivory'], fontsize=14, fontweight='bold')
ax.set_yticklabels(classes, color=SC['mushroom_ivory'], fontsize=14, fontweight='bold')

ax.set_xlabel('Predicted Label', color=SC['mushroom_ivory'], fontsize=14, fontweight='bold')
ax.set_ylabel('True Label', color=SC['mushroom_ivory'], fontsize=14, fontweight='bold')
ax.set_title('⟁ Sacred Confusion Matrix ⟁
Random Forest Classifier Performance',
            color=SC['sacred_gold'], fontsize=16, fontweight='bold', pad=20)

# Colorbar
cbar = plt.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label('Count', color=SC['mushroom_ivory'], fontsize=12)
cbar.ax.yaxis.set_tick_params(color=SC['mushroom_ivory'])
plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color=SC['mushroom_ivory'])

# Metrics box
metrics_text = (f"Accuracy:  {accuracy:.3f}\n"
               f"Precision: {precision:.3f}\n"
               f"Recall:    {recall:.3f}\n"
               f"F1-Score:  {f1:.3f}\n"
               f"ROC-AUC:   {roc_auc:.3f}")

box = FancyBboxPatch((1.15, 0.25), 0.3, 0.5,
                    boxstyle="round,pad=0.02,rounding_size=0.02",
                    facecolor=SC['nebula_purple'], edgecolor=SC['sacred_gold'],
                    alpha=0.9, linewidth=2, transform=ax.transAxes)
ax.add_patch(box)
ax.text(1.3, 0.5, metrics_text, ha='center', va='center',
       color=SC['mushroom_ivory'], fontsize=11, fontweight='bold',
       transform=ax.transAxes)

plt.tight_layout()
plt.savefig('dashboard/08_sacred_confusion_matrix.png', dpi=150,
           facecolor=SC['deep_void'], bbox_inches='tight')
plt.show()

print("
✅ Sacred Confusion Matrix saved!")

# %% [markdown]
# ### 5.2 Visualization: The ROC Curve — The Receiver Operating Characteristic

# %%
fig, ax = plt.subplots(figsize=(10, 8), facecolor=SC['deep_void'])
ax.set_facecolor(SC['deep_void'])

fpr, tpr, thresholds = roc_curve(y_test, y_prob)

# Plot ROC curve
ax.plot(fpr, tpr, color=SC['crystal_cyan'], linewidth=3,
       label=f'Random Forest (AUC = {roc_auc:.3f})')

# Diagonal reference
ax.plot([0, 1], [0, 1], color=SC['dmt_coral'], linewidth=2, 
       linestyle='--', alpha=0.7, label='Random Classifier (AUC = 0.500)')

# Fill area
ax.fill_between(fpr, tpr, alpha=0.3, color=SC['crystal_cyan'])

# Optimal threshold point (Youden's J statistic)
j_scores = tpr - fpr
optimal_idx = np.argmax(j_scores)
optimal_threshold = thresholds[optimal_idx]
ax.scatter(fpr[optimal_idx], tpr[optimal_idx], s=200, c=SC['sacred_gold'],
          edgecolors=SC['mushroom_ivory'], linewidth=3, zorder=10,
          label=f'Optimal Threshold = {optimal_threshold:.3f}')

ax.set_xlabel('False Positive Rate (1 - Specificity)', 
             color=SC['mushroom_ivory'], fontsize=12, fontweight='bold')
ax.set_ylabel('True Positive Rate (Sensitivity)', 
             color=SC['mushroom_ivory'], fontsize=12, fontweight='bold')
ax.set_title('⟁ The ROC Oracle: Receiver Operating Characteristic ⟁',
            color=SC['sacred_gold'], fontsize=16, fontweight='bold', pad=20)
ax.legend(loc='lower right', facecolor=SC['deep_void'], 
         edgecolor=SC['sacred_gold'], labelcolor=SC['mushroom_ivory'],
         fontsize=11)
ax.set_xlim([0, 1])
ax.set_ylim([0, 1])

plt.tight_layout()
plt.savefig('dashboard/09_roc_oracle.png', dpi=150,
           facecolor=SC['deep_void'], bbox_inches='tight')
plt.show()

print(f"
✅ ROC Oracle saved!")
print(f"   Optimal Classification Threshold: {optimal_threshold:.3f}")
print(f"   At Optimal Point: Sensitivity = {tpr[optimal_idx]:.3f}, Specificity = {1-fpr[optimal_idx]:.3f}")

# %% [markdown]
# ## 6. Feature Importance — The Hierarchy of Prophecy

# %%
print("
" + "=" * 70)
print("◈ FEATURE IMPORTANCE: THE HIERARCHY OF PROPHECY ◈")
print("=" * 70)

importance = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': rf_model.feature_importances_,
    'Std': np.std([tree.feature_importances_ for tree in rf_model.estimators_], axis=0)
}).sort_values('Importance', ascending=False)

importance['Cumulative'] = importance['Importance'].cumsum()
importance['Rank'] = range(1, len(importance) + 1)

print(f"
📊 Top 10 Prophetic Features:")
print(f"   {'─'*60}")
for _, row in importance.head(10).iterrows():
    bar = '█' * int(row['Importance'] * 50)
    print(f"   {row['Rank']:2d}. {row['Feature']:25s} {row['Importance']:.4f} {bar}")

print(f"
📊 Cumulative Importance:")
print(f"   Top 5 features explain:  {importance.head(5)['Cumulative'].iloc[-1]*100:.1f}% of variance")
print(f"   Top 10 features explain: {importance.head(10)['Cumulative'].iloc[-1]*100:.1f}% of variance")

# %% [markdown]
# ### 6.1 Visualization: The Sacred Feature Importance

# %%
fig, ax = plt.subplots(figsize=(12, 8), facecolor=SC['deep_void'])
ax.set_facecolor(SC['deep_void'])

top_n = min(15, len(importance))
top_features = importance.head(top_n).sort_values('Importance', ascending=True)

colors = plt.cm.dmt_vision(np.linspace(0.2, 0.9, top_n))

bars = ax.barh(range(top_n), top_features['Importance'],
              color=colors, edgecolor=SC['sacred_gold'], 
              linewidth=1.5, height=0.6,
              xerr=top_features['Std'], 
              error_kw={'ecolor': SC['mushroom_ivory'], 'capsize': 3, 'capthick': 1})

ax.set_yticks(range(top_n))
ax.set_yticklabels(top_features['Feature'], color=SC['mushroom_ivory'], fontsize=11)
ax.set_xlabel('Importance Score (Gini Importance)', 
             color=SC['mushroom_ivory'], fontsize=12, fontweight='bold')
ax.set_title('⟁ Sacred Feature Importance ⟁
The Hierarchy of Prophecy: What Drives Mission Success?',
            color=SC['sacred_gold'], fontsize=16, fontweight='bold', pad=20)

# Add value labels
for i, (bar, val, std) in enumerate(zip(bars, top_features['Importance'], top_features['Std'])):
    ax.text(bar.get_width() + std + 0.005, bar.get_y() + bar.get_height()/2,
           f'{val:.4f}', va='center', color=SC['mushroom_ivory'], fontsize=9)

# Add cumulative line
cumsum_sorted = top_features['Cumulative'].values
ax2 = ax.twiny()
ax2.set_facecolor(SC['deep_void'])
ax2.plot(cumsum_sorted, range(top_n), color=SC['amber_resin'], 
        linewidth=2, marker='o', markersize=6, linestyle='--')
ax2.set_xlim(0, 1)
ax2.set_xlabel('Cumulative Importance', color=SC['amber_resin'], fontsize=10)
ax2.tick_params(axis='x', colors=SC['amber_resin'])
ax2.spines['top'].set_color(SC['sacred_gold'])

plt.tight_layout()
plt.savefig('dashboard/10_sacred_feature_importance.png', dpi=150,
           facecolor=SC['deep_void'], bbox_inches='tight')
plt.show()

print("
✅ Sacred Feature Importance saved!")

# %% [markdown]
# ## 7. Mission Prognostication — The Interactive Oracle
# 
# We now create a prediction interface for hypothetical missions. This demonstrates the 
# **deployment-ready** nature of our model—transforming trained parameters into operational 
# decision support.

# %%
print("
" + "=" * 70)
print("◈ MISSION PROGNOSTICATION: THE INTERACTIVE ORACLE ◈")
print("=" * 70)

def prognosticate_mission(payload_mass=5000, reused_count=2, block=5.0, 
                       orbit='GTO', days_since_first=2500):
    """
    Predict mission success probability for a hypothetical launch configuration.

    Parameters:
    -----------
    payload_mass : int
        Payload mass in kilograms
    reused_count : int
        Number of prior flights for this booster
    block : float
        Vehicle generation (1.0–5.0)
    orbit : str
        Target orbital destination
    days_since_first : int
        Days since program inception (proxy for operational maturity)

    Returns:
    --------
    dict
        Prediction results with probability, confidence, and recommendation
    """
    # Create feature vector
    features = np.zeros(len(feature_cols))

    # Map inputs to feature positions
    feature_values = {
        'PayloadMass': payload_mass,
        'ReusedCount': reused_count,
        'Block': block,
        'DaysSinceFirst': days_since_first,
        'Year': 2021,  # Assumed current year
        'Month': 6,
        'Quarter': 2,
        'DayOfWeek': 2,
        'IsWeekend': 0,
        'IsYearEnd': 0,
        'Payload_x_Reuse': payload_mass * reused_count,
        'Block_x_Days': block * days_since_first,
        'PayloadPerBlock': payload_mass / block,
        'CumulativeLaunches': 91,  # Approximate current count
        'RollingSuccessRate': 0.857,  # Historical average
        'RollingPayloadMean': 6927,  # Historical average
        'CostPerKg': 50000000 / payload_mass if reused_count > 0 else 62000000 / payload_mass,
        'SavingsVsCompetitor': 165 - (50 if reused_count > 0 else 62),
    }

    # Set base features
    for feat, val in feature_values.items():
        if feat in feature_cols:
            features[feature_cols.index(feat)] = val

    # Set orbital dummy
    orbit_col = f'Orbit_{orbit}'
    if orbit_col in feature_cols:
        features[feature_cols.index(orbit_col)] = 1

    # Set site dummy (default to CCAFS)
    site_col = 'Site_CCAFS_SLC_40'
    if site_col in feature_cols:
        features[feature_cols.index(site_col)] = 1

    # Predict
    prediction = rf_model.predict([features])[0]
    probabilities = rf_model.predict_proba([features])[0]

    success_prob = probabilities[1]
    failure_prob = probabilities[0]
    confidence = max(probabilities)

    # Risk assessment
    if success_prob >= 0.95:
        risk_level = "MINIMAL"
        recommendation = "PROCEED — Mission parameters align with historical success patterns."
        color = SC['organic_emerald']
    elif success_prob >= 0.80:
        risk_level = "LOW"
        recommendation = "PROCEED WITH STANDARD PRECAUTIONS — Elevated but acceptable risk profile."
        color = SC['mystic_teal']
    elif success_prob >= 0.60:
        risk_level = "MODERATE"
        recommendation = "REVIEW PARAMETERS — Consider payload reduction or booster swap."
        color = SC['amber_resin']
    else:
        risk_level = "ELEVATED"
        recommendation = "HALT AND REASSESS — Significant risk factors detected."
        color = SC['dmt_coral']

    result = {
        'prediction': int(prediction),
        'success_probability': float(success_prob),
        'failure_probability': float(failure_prob),
        'confidence': float(confidence),
        'is_success': bool(prediction == 1),
        'risk_level': risk_level,
        'recommendation': recommendation,
        'color': color
    }

    return result

# Example predictions
print(f"
📊 Example Mission Prognostications:")
print(f"   {'─'*60}")

scenarios = [
    {"name": "Starlink Constellation (Routine)", "payload": 15600, "reuse": 8, "block": 5.0, "orbit": "LEO", "days": 3800},
    {"name": "Commercial GEO Satellite", "payload": 5500, "reuse": 2, "block": 5.0, "orbit": "GTO", "days": 3000},
    {"name": "ISS Resupply (Crew Dragon)", "payload": 3000, "reuse": 1, "block": 5.0, "orbit": "ISS", "days": 3200},
    {"name": "Experimental New Booster", "payload": 4000, "reuse": 0, "block": 5.0, "orbit": "LEO", "days": 3900},
    {"name": "Polar Orbit Observation", "payload": 2200, "reuse": 5, "block": 5.0, "orbit": "PO", "days": 3500},
]

for scenario in scenarios:
    result = prognosticate_mission(
        payload_mass=scenario["payload"],
        reused_count=scenario["reuse"],
        block=scenario["block"],
        orbit=scenario["orbit"],
        days_since_first=scenario["days"]
    )

    symbol = "✦" if result['is_success'] else "⚠"
    print(f"
   {symbol} {scenario['name']}")
    print(f"      Success Probability: {result['success_probability']*100:.1f}%")
    print(f"      Risk Level:        {result['risk_level']}")
    print(f"      Confidence:        {result['confidence']*100:.1f}%")
    print(f"      Verdict:           {result['recommendation']}")

# %% [markdown]
# ## 8. Model Persistence & Deployment Preparation

# %%
import joblib

print("
" + "=" * 70)
print("◈ MODEL PERSISTENCE: THE ETERNAL ARCHIVE ◈")
print("=" * 70)

# Save model
model_path = 'src/mission_prognosticator.pkl'
joblib.dump(rf_model, model_path)
print(f"
💾 Model saved to: {model_path}")

# Save feature list
feature_path = 'src/feature_columns.pkl'
joblib.dump(feature_cols, feature_path)
print(f"💾 Feature list saved to: {feature_path}")

# Save scaler (if used)
# scaler_path = 'src/scaler.pkl'
# joblib.dump(scaler, scaler_path)
# print(f"💾 Scaler saved to: {scaler_path}")

# Create prediction function script
prediction_script = 
Mission Prognostication API
Load trained model and make predictions for new missions.
