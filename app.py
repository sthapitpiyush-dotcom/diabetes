import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from diabetes_prediction import DiabetesPredictor, download_dataset
import os

# Page configuration
st.set_page_config(
    page_title="Diabetes Prediction System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-box {
        padding: 2rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        margin: 2rem 0;
    }
    .metric-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    """Load and train the diabetes prediction model"""
    dataset_path = download_dataset()
    predictor = DiabetesPredictor(dataset_path)
    
    # Load and process data
    predictor.load_data()
    predictor.clean_data()
    predictor.feature_selection()
    predictor.transform_features()
    predictor.split_data()
    predictor.train_all_models()
    
    return predictor

def main():
    st.markdown('<h1 class="main-header">🏥 Diabetes Prediction System</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Choose a page", ["Prediction", "Model Performance", "Data Analysis"])
    
    # Load model
    with st.spinner("Loading and training models... This may take a minute."):
        predictor = load_model()
    
    if page == "Prediction":
        show_prediction_page(predictor)
    elif page == "Model Performance":
        show_performance_page(predictor)
    elif page == "Data Analysis":
        show_analysis_page(predictor)

def show_prediction_page(predictor):
    st.header("🔮 Make a Prediction")
    st.markdown("Enter patient information to predict diabetes risk")
    
    col1, col2 = st.columns(2)
    
    with col1:
        pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=0, step=1)
        glucose = st.number_input("Glucose Level", min_value=0, max_value=300, value=100, step=1)
        skin_thickness = st.number_input("Skin Thickness (mm)", min_value=0, max_value=100, value=20, step=1)
    
    with col2:
        bmi = st.number_input("BMI (Body Mass Index)", min_value=0.0, max_value=70.0, value=25.0, step=0.1)
        age = st.number_input("Age", min_value=0, max_value=120, value=30, step=1)
    
    # Model selection
    st.subheader("Select Model")
    model_options = {
        "KNN (Tuned - Best)": "knn_tuned",
        "Logistic Regression": "logistic_regression",
        "KNN (Basic)": "knn",
        "Random Forest (Tuned)": "random_forest_tuned",
        "Random Forest (Basic)": "random_forest"
    }
    selected_model_name = st.selectbox("Choose a model", list(model_options.keys()))
    model_key = model_options[selected_model_name]
    model = predictor.models.get(model_key, predictor.best_model)
    
    if st.button("🔍 Predict", type="primary", use_container_width=True):
        try:
            features = {
                'Pregnancies': pregnancies,
                'Glucose': glucose,
                'SkinThickness': skin_thickness,
                'BMI': bmi,
                'Age': age
            }
            
            prediction, probability = predictor.predict(model, features)
            
            # Display result
            if prediction == 1:
                st.markdown("""
                    <div class="prediction-box">
                        <h2>⚠️ High Risk of Diabetes</h2>
                        <p style="font-size: 1.2rem;">The model predicts this patient is at risk of diabetes.</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="prediction-box" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">
                        <h2>✅ Low Risk of Diabetes</h2>
                        <p style="font-size: 1.2rem;">The model predicts this patient is not at risk of diabetes.</p>
                    </div>
                """, unsafe_allow_html=True)
            
            # Show probabilities
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Probability of No Diabetes", f"{probability[0]*100:.2f}%")
            with col2:
                st.metric("Probability of Diabetes", f"{probability[1]*100:.2f}%")
            
            # Progress bar
            st.progress(probability[1])
            st.caption(f"Risk Level: {probability[1]*100:.1f}%")
            
        except Exception as e:
            st.error(f"Error making prediction: {str(e)}")

def show_performance_page(predictor):
    st.header("📊 Model Performance Metrics")
    
    # Evaluate all models
    model_results = {}
    for model_name, model in predictor.models.items():
        metrics = predictor.evaluate_model(model, model_name)
        model_results[model_name] = metrics
    
    # Create comparison dataframe
    comparison_data = {
        'Model': [],
        'Accuracy (%)': [],
        'F1 Score': [],
        'Precision': [],
        'Recall': []
    }
    
    for model_name, metrics in model_results.items():
        comparison_data['Model'].append(model_name.replace('_', ' ').title())
        comparison_data['Accuracy (%)'].append(round(metrics['accuracy'], 2))
        comparison_data['F1 Score'].append(round(metrics['f1_score'], 4))
        comparison_data['Precision'].append(round(metrics['precision'], 4))
        comparison_data['Recall'].append(round(metrics['recall'], 4))
    
    df_comparison = pd.DataFrame(comparison_data)
    
    # Display comparison table
    st.subheader("Model Comparison")
    st.dataframe(df_comparison, use_container_width=True)
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Accuracy Comparison")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(df_comparison['Model'], df_comparison['Accuracy (%)'])
        ax.set_xlabel('Accuracy (%)')
        ax.set_title('Model Accuracy Comparison')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.subheader("F1 Score Comparison")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(df_comparison['Model'], df_comparison['F1 Score'])
        ax.set_xlabel('F1 Score')
        ax.set_title('Model F1 Score Comparison')
        plt.tight_layout()
        st.pyplot(fig)
    
    # Detailed metrics for each model
    st.subheader("Detailed Metrics")
    selected_model = st.selectbox("Select a model to view detailed metrics", 
                                  list(model_results.keys()))
    
    if selected_model:
        metrics = model_results[selected_model]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Accuracy", f"{metrics['accuracy']:.2f}%")
        with col2:
            st.metric("F1 Score", f"{metrics['f1_score']:.4f}")
        with col3:
            st.metric("Precision", f"{metrics['precision']:.4f}")
        with col4:
            st.metric("Recall", f"{metrics['recall']:.4f}")
        
        # Confusion Matrix
        st.subheader("Confusion Matrix")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(metrics['confusion_matrix'], annot=True, fmt='d', cmap='Blues', ax=ax)
        ax.set_xlabel('Predicted')
        ax.set_ylabel('Actual')
        ax.set_title(f'Confusion Matrix - {selected_model.replace("_", " ").title()}')
        st.pyplot(fig)
        
        # Classification Report
        st.subheader("Classification Report")
        st.text(metrics['classification_report'])

def show_analysis_page(predictor):
    st.header("📈 Data Analysis")
    
    # Dataset info
    st.subheader("Dataset Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", len(predictor.df))
    with col2:
        st.metric("Features", len(predictor.df.columns) - 1)
    with col3:
        st.metric("Target Variable", "Outcome (0/1)")
    
    # Data preview
    st.subheader("Data Preview")
    st.dataframe(predictor.df.head(10), use_container_width=True)
    
    # Statistics
    st.subheader("Dataset Statistics")
    st.dataframe(predictor.df.describe(), use_container_width=True)
    
    # Visualizations
    st.subheader("Data Visualizations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Outcome Distribution**")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.countplot(x='Outcome', data=predictor.df, ax=ax)
        ax.set_xlabel('Outcome (0: No Diabetes, 1: Diabetes)')
        ax.set_ylabel('Count')
        ax.set_title('Distribution of Diabetes Outcomes')
        st.pyplot(fig)
    
    with col2:
        st.write("**Correlation Heatmap**")
        fig, ax = plt.subplots(figsize=(10, 8))
        corrmat = predictor.df.corr()
        sns.heatmap(corrmat, annot=True, fmt='.2f', cmap='coolwarm', ax=ax)
        plt.tight_layout()
        st.pyplot(fig)
    
    # Feature distributions
    st.subheader("Feature Distributions")
    selected_feature = st.selectbox("Select a feature to visualize", 
                                   ['Glucose', 'BMI', 'Age', 'Pregnancies', 'BloodPressure', 'Insulin'])
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Histogram
    predictor.df[selected_feature].hist(bins=20, ax=ax1)
    ax1.set_xlabel(selected_feature)
    ax1.set_ylabel('Frequency')
    ax1.set_title(f'Distribution of {selected_feature}')
    
    # Box plot
    sns.boxplot(x=selected_feature, data=predictor.df, ax=ax2)
    ax2.set_title(f'Box Plot of {selected_feature}')
    
    plt.tight_layout()
    st.pyplot(fig)

if __name__ == "__main__":
    main()

