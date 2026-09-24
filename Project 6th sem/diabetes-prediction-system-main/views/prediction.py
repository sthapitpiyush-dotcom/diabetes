import streamlit as st

from auth import get_current_user
from predictions_db import add_prediction
from services.doctors import recommend_doctor


def show_prediction_page(predictor):
    st.header("Make a Prediction")
    st.markdown("Enter patient information to predict diabetes risk")

    gender = st.radio("Gender", ["Male", "Female"], horizontal=True)

    col1, col2 = st.columns(2)

    with col1:
        if gender == "Female":
            pregnancies = st.number_input("Pregnancies (weeks)", min_value=0, max_value=40, value=0, step=1)
        else:
            pregnancies = 0

        glucose = st.number_input("Glucose Level (Mg/dl)", min_value=0, max_value=300, value=100, step=1)
        skin_thickness = st.number_input("Skin Thickness (mm)", min_value=0, max_value=100, value=20, step=1)

    with col2:
        height_feet = st.number_input("Height (feet)", min_value=3.0, max_value=8.0, value=5.5, step=0.1)
        weight_kg = st.number_input("Weight (kg)", min_value=20.0, max_value=200.0, value=70.0, step=0.1)

        height_meters = height_feet * 0.3048
        bmi = weight_kg / (height_meters ** 2) if height_meters > 0 else 0

        st.metric("Calculated BMI", f"{bmi:.2f}")

        age = st.number_input("Age", min_value=0, max_value=120, value=30, step=1)

    model = predictor.models.get('knn_tuned', predictor.best_model)

    if st.button("Predict", type="primary", use_container_width=True):
        try:
            features = {
                'Pregnancies': pregnancies,
                'Glucose': glucose,
                'SkinThickness': skin_thickness,
                'BMI': bmi,
                'Age': age
            }

            prediction, probability = predictor.predict(model, features)
            risk_percentage = probability[1] * 100

            username = get_current_user()

            recommended_doctor = recommend_doctor(risk_percentage)

            features_with_gender = features.copy()
            features_with_gender['Gender'] = gender
            features_with_gender['Height (feet)'] = height_feet
            features_with_gender['Weight (kg)'] = weight_kg

            add_prediction(
                username=username,
                features=features_with_gender,
                prediction=prediction,
                probability=probability,
                recommended_doctor=recommended_doctor
            )

            if prediction == 1:
                st.markdown("""
                    <div class="prediction-box">
                        <h2>High Risk of Diabetes</h2>
                        <p style="font-size: 1.2rem;">The model predicts this patient is at risk of diabetes.</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="prediction-box" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">
                        <h2>Low Risk of Diabetes</h2>
                        <p style="font-size: 1.2rem;">The model predicts this patient is not at risk of diabetes.</p>
                    </div>
                """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Probability of No Diabetes", f"{probability[0]*100:.2f}%")
            with col2:
                st.metric("Probability of Diabetes", f"{probability[1]*100:.2f}%")

            st.progress(probability[1])
            st.caption(f"Risk Level: {risk_percentage:.1f}%")

            if recommended_doctor:
                st.markdown("---")
                st.subheader("Recommended Doctor")

                st.markdown(f"""
                <div class="doctor-card">
                    <h3>{recommended_doctor['name']}</h3>
                    <p><strong>Specialty:</strong> {recommended_doctor['specialty']}</p>
                    <p><strong>Phone:</strong> {recommended_doctor['phone']}</p>
                    <p><strong>Email:</strong> {recommended_doctor['email']}</p>
                    <p><strong>Recommended at Diabetes Risk:</strong>
                       <span style="font-weight:bold; color:#d32f2f;">
                       {risk_percentage:.1f}%
                       </span>
                    </p>
                </div>
                """, unsafe_allow_html=True)

                st.info(
                    f"Since your diabetes risk is **{risk_percentage:.1f}%**, "
                    f"we recommend consulting **{recommended_doctor['name']} ({recommended_doctor['specialty']})**."
                )

            elif risk_percentage > 50:
                st.warning(f"""
                 Your risk is **{risk_percentage:.1f}%** (Moderate).
                 We typically recommend a General Diabetes Care Physician for this range,
                 but no doctor is currently available in the database.
                 """)
            else:
                st.success(f"""
                Your risk is **{risk_percentage:.1f}%** (Low).
                Since your risk is **below 50%**, no specific doctor consultation is required at this time.
                Keep up the healthy lifestyle!
                """)

            st.success("Prediction saved to your history.")

        except Exception as e:
            st.error(f"Error making prediction: {str(e)}")
