import streamlit as st

from diabetes_prediction import DiabetesPredictor, download_dataset


@st.cache_resource
def load_model():
    dataset_path = download_dataset()
    predictor = DiabetesPredictor(dataset_path)

    if predictor.load_saved_model():
        print("Using cached model.")
        predictor.load_data()
        predictor.clean_data()
        predictor.feature_selection()
        predictor.transform_features()
        predictor.split_data()
        return predictor

    print("No cached model found. Training new model...")
    predictor.load_data()
    predictor.clean_data()
    predictor.feature_selection()
    predictor.transform_features()
    predictor.split_data()
    predictor.train_knn_tuned_only()
    predictor.save_model()

    return predictor
