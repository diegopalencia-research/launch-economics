from setuptools import setup, find_packages

setup(
    name='launch-economics',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.5.0',
        'numpy>=1.23.0',
        'plotly>=5.13.0',
        'scikit-learn>=1.2.0',
        'scipy>=1.10.0',
        'streamlit>=1.20.0',
    ],
    python_requires='>=3.9',
)
