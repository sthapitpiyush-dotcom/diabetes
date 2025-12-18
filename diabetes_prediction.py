import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, r2_score, f1_score, precision_score, recall_score
from sklearn.model_selection import RepeatedStratifiedKFold, GridSearchCV
from sklearn.preprocessing import QuantileTransformer
import pickle
import os

class DiabetesPredictor:
    def __init__(self, data_path=None):
        self.data_path = data_path
        self.df = None
        self.df_selected = None
        self.df_new = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.quantile = QuantileTransformer()
        self.models = {}
        self.best_model = None
        
    def load_data(self, data_path=None):
        """Load diabetes dataset from CSV file"""
        if data_path:
            self.data_path = data_path
        if not self.data_path:
            raise ValueError("Data path not provided")
        
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Dataset file not found: {self.data_path}")
        
        self.df = pd.read_csv(self.data_path)
        return self.df
    
    def clean_data(self):
        """Clean and preprocess the data"""
        # Drop duplicates
        self.df = self.df.drop_duplicates()
        
        # Replace 0 values with mean/median
        self.df['Glucose'] = self.df['Glucose'].replace(0, self.df['Glucose'].mean())
        self.df['BloodPressure'] = self.df['BloodPressure'].replace(0, self.df['BloodPressure'].mean())
        self.df['SkinThickness'] = self.df['SkinThickness'].replace(0, self.df['SkinThickness'].median())
        self.df['Insulin'] = self.df['Insulin'].replace(0, self.df['Insulin'].median())
        self.df['BMI'] = self.df['BMI'].replace(0, self.df['BMI'].median())
        
        return self.df
    
    def feature_selection(self):
        """Select features based on correlation"""
        # Drop least correlated features
        self.df_selected = self.df.drop(['BloodPressure', 'Insulin', 'DiabetesPedigreeFunction'], axis='columns')
        return self.df_selected
    
    def transform_features(self):
        """Apply Quantile Transformation to handle outliers"""
        x = self.df_selected
        X = self.quantile.fit_transform(x)
        self.df_new = pd.DataFrame(X)
        self.df_new.columns = ['Pregnancies', 'Glucose', 'SkinThickness', 'BMI', 'Age', 'Outcome']
        return self.df_new
    
    def split_data(self, test_size=0.2, random_state=0):
        """Split data into training and testing sets"""
        target_name = 'Outcome'
        y = self.df_new[target_name]
        X = self.df_new.drop(target_name, axis=1)
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def train_logistic_regression(self):
        """Train Logistic Regression model"""
        reg = LogisticRegression()
        reg.fit(self.X_train, self.y_train)
        self.models['logistic_regression'] = reg
        return reg
    
    def train_knn(self, n_neighbors=7):
        """Train KNN model"""
        knn = KNeighborsClassifier(n_neighbors=n_neighbors)
        knn.fit(self.X_train, self.y_train)
        self.models['knn'] = knn
        return knn
    
    def train_random_forest(self):
        """Train Random Forest model"""
        rfc = RandomForestClassifier()
        rfc.fit(self.X_train, self.y_train)
        self.models['random_forest'] = rfc
        return rfc
    
    def tune_knn(self):
        """Hyperparameter tuning for KNN"""
        knn = KNeighborsClassifier()
        n_neighbors = list(range(15, 25))
        p = [1, 2]
        weights = ['uniform', 'distance']
        metric = ['euclidean', 'manhattan', 'minkowski']
        
        hyperparameters = dict(n_neighbors=n_neighbors, p=p, weights=weights, metric=metric)
        cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
        grid_search = GridSearchCV(estimator=knn, param_grid=hyperparameters, n_jobs=-1, 
                                   cv=cv, scoring='f1', error_score=0)
        
        best_model = grid_search.fit(self.X_train, self.y_train)
        self.models['knn_tuned'] = best_model.best_estimator_
        self.best_model = best_model.best_estimator_
        return best_model.best_estimator_
    
    def tune_random_forest(self):
        """Hyperparameter tuning for Random Forest"""
        model = RandomForestClassifier()
        n_estimators = [1800]
        max_features = ['sqrt', 'log2']
        
        grid = dict(n_estimators=n_estimators, max_features=max_features)
        cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
        grid_search = GridSearchCV(estimator=model, param_grid=grid, n_jobs=-1, 
                                   cv=cv, scoring='accuracy', error_score=0)
        
        best_model = grid_search.fit(self.X_train, self.y_train)
        self.models['random_forest_tuned'] = best_model.best_estimator_
        return best_model.best_estimator_
    
    def evaluate_model(self, model, model_name):
        """Evaluate a model and return metrics"""
        y_pred = model.predict(self.X_test)
        
        metrics = {
            'accuracy': accuracy_score(self.y_test, y_pred) * 100,
            'f1_score': f1_score(self.y_test, y_pred),
            'precision': precision_score(self.y_test, y_pred),
            'recall': recall_score(self.y_test, y_pred),
            'classification_report': classification_report(self.y_test, y_pred),
            'confusion_matrix': confusion_matrix(self.y_test, y_pred),
            'predictions': y_pred
        }
        return metrics
    
    def predict(self, model, features):
        """Make prediction on new data"""
        # Transform features using the same quantile transformer
        features_df = pd.DataFrame([features], columns=['Pregnancies', 'Glucose', 'SkinThickness', 'BMI', 'Age'])
        features_transformed = self.quantile.transform(features_df)
        prediction = model.predict(features_transformed)[0]
        probability = model.predict_proba(features_transformed)[0]
        return prediction, probability
    
    def train_all_models(self):
        """Train all models and tune hyperparameters"""
        print("Training Logistic Regression...")
        self.train_logistic_regression()
        
        print("Training KNN...")
        self.train_knn()
        
        print("Training Random Forest...")
        self.train_random_forest()
        
        print("Tuning KNN...")
        self.tune_knn()
        
        print("Tuning Random Forest...")
        self.tune_random_forest()
        
        print("Training complete!")
    
    def get_best_model(self):
        """Get the best performing model"""
        if not self.best_model:
            self.best_model = self.models.get('knn_tuned')
        return self.best_model

def download_dataset():
    """Download diabetes dataset if not present"""
    import urllib.request
    
    dataset_url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
    dataset_path = "diabetes.csv"
    
    if not os.path.exists(dataset_path):
        print(f"Downloading dataset from {dataset_url}...")
        urllib.request.urlretrieve(dataset_url, dataset_path)
        print("Dataset downloaded successfully!")
        
        # Add column names
        df = pd.read_csv(dataset_path, header=None)
        df.columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                     'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
        df.to_csv(dataset_path, index=False)
        print("Dataset prepared with column names!")
    
    return dataset_path

if __name__ == "__main__":
    # Download dataset if needed
    dataset_path = download_dataset()
    
    # Initialize predictor
    predictor = DiabetesPredictor(dataset_path)
    
    # Load and process data
    print("Loading data...")
    predictor.load_data()
    
    print("Cleaning data...")
    predictor.clean_data()
    
    print("Selecting features...")
    predictor.feature_selection()
    
    print("Transforming features...")
    predictor.transform_features()
    
    print("Splitting data...")
    predictor.split_data()
    
    print("Training models...")
    predictor.train_all_models()
    
    # Evaluate models
    print("\n=== Model Evaluation ===")
    for model_name, model in predictor.models.items():
        print(f"\n{model_name.upper()}:")
        metrics = predictor.evaluate_model(model, model_name)
        print(f"Accuracy: {metrics['accuracy']:.2f}%")
        print(f"F1 Score: {metrics['f1_score']:.4f}")
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recall: {metrics['recall']:.4f}")

