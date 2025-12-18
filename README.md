# Diabetes Prediction System

A machine learning-based diabetes prediction system with an interactive web UI built using Streamlit.

## Features

- **Multiple ML Models**: Logistic Regression, KNN, and Random Forest classifiers
- **Hyperparameter Tuning**: Optimized models using GridSearchCV
- **Interactive Web UI**: User-friendly Streamlit interface with:
  - Real-time predictions
  - Model performance comparison
  - Data analysis and visualizations
- **Automatic Dataset Download**: Downloads the diabetes dataset automatically if not present

## Installation

1. Make sure Python 3.8+ is installed on your system
   - Download from [python.org](https://www.python.org/downloads/) if needed
   - During installation, check "Add Python to PATH"

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

Or on Windows if `pip` is not recognized:
```bash
python -m pip install -r requirements.txt
```

## Usage

### Run the Web UI (Recommended)

```bash
streamlit run app.py
```

Or on Windows:
```bash
python -m streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Run the Python Script Directly

```bash
python diabetes_prediction.py
```

Or on Windows:
```bash
python -m diabetes_prediction
```

## Getting Started

1. **Sign Up**: Create a new account using the "Sign Up" tab on the login page
   - Username must be at least 3 characters
   - Password must be at least 6 characters
   - New users are automatically assigned "user" role

2. **Login**: Use your credentials to access the system

## Application Pages

1. **Prediction**: Enter patient information to get diabetes risk prediction
2. **Model Performance**: View and compare performance metrics of all models
3. **Data Analysis**: Explore the dataset with visualizations and statistics
4. **My Predictions**: View your prediction history (all users)
5. **Admin Panel**: View all predictions, statistics, and user activity (admin only)

## Model Performance

The system trains and evaluates multiple models:
- **KNN (Tuned)**: Best performing model (~81% accuracy)
- **Logistic Regression**: ~79% accuracy
- **Random Forest (Tuned)**: ~79% accuracy

## Dataset

The system uses the Pima Indians Diabetes Dataset, which is automatically downloaded if not present in the project directory.

## Requirements

- Python 3.8+
- See `requirements.txt` for package dependencies

