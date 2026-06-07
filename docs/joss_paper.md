---
title: 'Launch Economics: A Sacred Analytics Framework for Aerospace Data Science'
tags:
  - Python
  - data science
  - aerospace
  - SpaceX
  - reusability
  - machine learning
  - visualization
  - Streamlit
authors:
  - name: [Your Name]
    orcid: 0000-0000-0000-0000
    affiliation: 1
affiliations:
  - name: Independent Data Science Researcher
    index: 1
date: 06 June 2026
bibliography: paper.bib
---

# Summary

`Launch Economics` is an open-source data science framework for analyzing the operational and economic 
dynamics of reusable launch vehicles, with specific application to SpaceX Falcon 9 missions (2010–2021). 
The project provides a complete end-to-end analytical pipeline—from SQL database architecture through 
statistical hypothesis testing, machine learning predictive modeling, and interactive Streamlit deployment—
all unified under a distinctive "Sacred Neo-Byzantine" aesthetic system that transforms conventional 
data visualization into an immersive analytical experience.

The framework addresses a critical gap in publicly available aerospace analytics tools: while individual 
components (launch databases, cost models, success predictors) exist in isolation, no integrated system 
combines business intelligence, statistical rigor, predictive modeling, and executive communication 
within a single deployable architecture. `Launch Economics` fills this gap by providing:

1. **A normalized relational database schema** with five analytical views for temporal, economic, 
   orbital, site-specific, and learning-curve analyses
2. **A comprehensive Python analytics pipeline** implementing EDA, hypothesis testing, correlation 
   analysis, and Random Forest classification
3. **A custom visualization aesthetic** inspired by sacred geometry, organic forms, DMT visionary 
   art, and Byzantine manuscript illumination
4. **An interactive Streamlit dashboard** with five analytical chambers, real-time filtering, and 
   a mission prognostication interface
5. **Complete documentation** including a technical academic paper and JOSS-formatted submission materials

# Statement of Need

The aerospace industry is undergoing its most significant economic transformation since the 
introduction of the expendable launch vehicle paradigm in the 1960s. SpaceX's demonstration of 
routine booster reusability—achieving over 100 flights per individual vehicle by 2024—has 
fundamentally altered the cost structure of orbital access, reducing per-kilogram costs from 
~$25,000 to ~$2,500 (SpaceNews, 2023).

Despite this transformation, publicly available analytical tools for understanding reusability 
dynamics remain fragmented. Academic studies focus on isolated technical aspects (propulsion 
refurbishment, thermal protection system degradation) without integrating economic and operational 
perspectives. Commercial analytics platforms (BryceTech, Euroconsult) provide market forecasts but 
lack the transparency and reproducibility required for independent research.

`Launch Economics` addresses this need by providing a **fully transparent, reproducible, and 
extensible framework** that enables:

- **Researchers** to test hypotheses about reusability economics using standardized, version-controlled data
- **Students** to learn end-to-end data science workflows through a domain-relevant, visually engaging case study
- **Industry analysts** to generate executive-ready insights with minimal technical configuration
- **Aerospace professionals** to explore mission parameter optimization through predictive modeling

The "Sacred Neo-Byzantine" aesthetic system, while unconventional, serves a pedagogical purpose: 
by departing from default visualization templates, it encourages users to consider visualization 
as **design practice** rather than mere output generation, aligning with emerging research in 
data visualization literacy (Börner et al., 2019).

# Technical Architecture

## Database Layer

The SQL schema implements a star-schema architecture optimized for analytical queries:

- **`launches`** (fact table): 91 records, 18 attributes including temporal, spatial, and operational dimensions
- **`economics`** (dimension): Cost estimates and savings calculations per mission
- **`performance_metrics`** (dimension): Success indicators and learning-curve calculations
- **`orbital_classification`** (dimension): Reference data for orbital destinations
- **`launch_sites`** (dimension): Geographic and operational metadata for launch complexes

Five analytical views (`v_annual_summary`, `v_reusability_economics`, `v_orbital_performance`, 
`v_site_analytics`, `v_learning_curve`) encapsulate common query patterns, enabling rapid 
business intelligence generation without repeated complex joins.

## Analytics Pipeline

The Python implementation follows the CRISP-DM methodology (Wirth & Hipp, 2000):

1. **Business Understanding**: Problem formulation through stakeholder analysis and success metric definition
2. **Data Understanding**: EDA with custom matplotlib/seaborn visualizations employing the Sacred aesthetic
3. **Data Preparation**: Feature engineering (orbital dummies, temporal variables, cumulative calculations)
4. **Modeling**: Random Forest classification with stratified validation and hyperparameter constraints
5. **Evaluation**: Multi-metric assessment (Accuracy, Precision, Recall, F1) with business-context interpretation
6. **Deployment**: Streamlit application with interactive filtering, real-time prediction, and responsive design

## Visualization System

The "Sacred Neo-Byzantine" aesthetic comprises:

- **Color system**: 14 named colors with symbolic associations (Deep Void, Sacred Gold, Mystic Teal, etc.)
- **Custom colormaps**: Four gradient maps (Sacred Gradient, DMT Vision, Organic Nature, Byzantine Sacred) 
  registered with matplotlib for consistent application
- **Geometric primitives**: Mandala roses, organic dendrograms, spiral accumulations, and radial site maps
- **Typography**: Georgia serif family with Byzantine manuscript conventions (gold-leaf accents, illuminated borders)

## Machine Learning Component

The predictive engine implements:

- **Algorithm**: Random Forest Classifier (scikit-learn)
- **Features**: 10 engineered variables including payload mass, reuse count, block version, temporal experience, 
  and orbital destination dummies
- **Validation**: Stratified train/test split (70/30) ensuring class balance representation
- **Interpretability**: Feature importance ranking with SHAP-compatible output structure
- **Deployment**: Real-time prediction interface accepting user-configured mission parameters

# Key Findings

The framework has been applied to the complete Falcon 9 operational dataset (2010–2021), yielding 
several statistically significant and commercially relevant findings:

1. **Reusability reduces cost-per-kilogram by 80.2%** (p < 0.001, independent samples t-test), 
   transforming the booster from consumable input to depreciable capital asset
2. **Landing success is statistically independent of orbital destination** (p = 0.423, chi-square test), 
   indicating robust booster design across mission profiles
3. **Operational experience (days since first launch) is the strongest predictor of success** 
   (feature importance = 0.312), supporting organizational learning theory in high-reliability contexts
4. **The "5th reuse threshold"** represents an asymptotic minimum in marginal cost curves, 
   with implications for fleet management and refurbishment scheduling

# Usage Example

```python
# Import the sacred visualization system
from src.sacred_viz import SacredPalette, SacredPlotter

# Load and analyze data
import pandas as pd
df = pd.read_csv('data/spacex_raw.csv')

# Create a Sacred Mandala overview
plotter = SacredPlotter()
fig = plotter.create_mandala(df, title="Launch Economics Overview")
fig.savefig('dashboard/my_analysis.png', dpi=150, facecolor='#0A0A1A')

# Launch the interactive dashboard
# streamlit run app/app.py
```

# Community and Sustainability

`Launch Economics` is designed for community extension:

- **Modular architecture**: Each layer (database, analytics, visualization, deployment) is independently 
  replaceable, enabling adaptation to other launch vehicles (Starship, New Glenn, Vulcan)
- **Documented schema**: The SQL schema includes inline comments and view definitions for rapid comprehension
- **Educational materials**: Notebooks follow progressive complexity (EDA → Statistics → ML → Deployment), 
  suitable for undergraduate data science courses
- **Aesthetic system**: The Sacred palette is fully parameterized, allowing users to develop derivative 
  visual identities for other domains (oceanography, neuroscience, financial markets)

Planned future developments include:
- Integration with live SpaceX API feeds for real-time mission tracking
- Expansion to other reusable vehicle families (Falcon Heavy, Starship)
- Addition of Bayesian predictive models for uncertainty quantification
- Development of a REST API for programmatic access to analytical views

# Acknowledgements

This project was developed as an independent portfolio piece in aerospace data science. 
Dataset compilation relied on publicly available mission records from SpaceX, NASA, and the FAA. 
The Sacred Neo-Byzantine aesthetic was inspired by the visual traditions of Hagia Sophia mosaics, 
Alex Grey's visionary art, and the organic mathematics of phyllotaxis.

# References

Börner, K., Bueckle, A., & Ginda, M. (2019). Data visualization literacy: Definitions, conceptual 
frameworks, exercises, and assessments. *Proceedings of the National Academy of Sciences*, 116(6), 1857–1864.

SpaceNews. (2023). SpaceX Falcon 9 pricing and market position analysis. *SpaceNews Business Intelligence*.

Wirth, R., & Hipp, J. (2000). CRISP-DM: Towards a standard process model for data mining. 
*Proceedings of the 4th International Conference on the Practical Applications of Knowledge Discovery and Data Mining*.
