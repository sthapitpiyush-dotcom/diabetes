import streamlit as st

from auth import get_current_user, is_admin
from predictions_db import get_all_predictions, get_user_predictions


def show_history_page():
    st.header("Prediction History")

    if is_admin():
        st.info("Admin view: showing all predictions.")
        predictions = get_all_predictions()
    else:
        username = get_current_user()
        st.info("Showing your prediction history")
        predictions = get_user_predictions(username)

    if not predictions:
        st.warning("No predictions found.")
        return

    predictions = sorted(predictions, key=lambda x: x.get('timestamp', ''), reverse=True)

    st.subheader(f"Total Predictions: {len(predictions)}")

    for idx, pred in enumerate(predictions, 1):
        with st.expander(f"Prediction #{idx} - {pred.get('timestamp', 'Unknown date')[:19]}"):
            col1, col2 = st.columns(2)

            with col1:
                st.write("**Patient Information:**")
                features = pred.get('features', {})
                gender = features.get('Gender', 'N/A')
                st.write(f"- Gender: {gender}")
                if gender == 'Female':
                    st.write(f"- Pregnancies (weeks): {features.get('Pregnancies', 0)}")
                if 'Height (feet)' in features:
                    st.write(f"- Height: {features.get('Height (feet)', 'N/A')} feet")
                if 'Weight (kg)' in features:
                    st.write(f"- Weight: {features.get('Weight (kg)', 'N/A')} kg")
                st.write(f"- BMI: {features.get('BMI', 'N/A')}")
                st.write(f"- Glucose Level: {features.get('Glucose', 'N/A')} Mg/dl")
                st.write(f"- Skin Thickness: {features.get('SkinThickness', 'N/A')} mm")
                st.write(f"- Age: {features.get('Age', 'N/A')}")

            with col2:
                st.write("**Prediction Results:**")
                prediction = pred.get('prediction', 0)
                prob_no = pred.get('probability_no_diabetes', 0) * 100
                prob_yes = pred.get('probability_diabetes', 0) * 100

                if prediction == 1:
                    st.error(f"High risk ({prob_yes:.1f}%)")
                else:
                    st.success(f"Low risk ({prob_no:.1f}%)")

                st.write(f"- No Diabetes: {prob_no:.2f}%")
                st.write(f"- Diabetes: {prob_yes:.2f}%")

                recommended_doctor = pred.get('recommended_doctor')
                if recommended_doctor:
                    st.markdown("---")
                    st.write("**Recommended doctor:**")
                    st.write(f"- {recommended_doctor.get('name', 'N/A')}")
                    st.write(f"- Specialty: {recommended_doctor.get('specialty', 'N/A')}")
                    st.write(f"- Phone: {recommended_doctor.get('phone', 'N/A')}")
                    st.write(f"- Email: {recommended_doctor.get('email', 'N/A')}")

                if is_admin():
                    st.write(f"**User:** {pred.get('username', 'Unknown')}")
