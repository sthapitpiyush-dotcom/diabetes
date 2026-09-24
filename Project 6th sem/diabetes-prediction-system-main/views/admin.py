import streamlit as st
import json
import os
import pandas as pd

from services.doctors import load_doctors, save_doctors


def load_model_metrics(filepath="saved_models/model_metrics.json"):
    """Load model evaluation metrics from JSON file"""
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading metrics: {e}")
        return None


def show_admin_panel():
    st.markdown('<h1 class="main-header">Admin Panel</h1>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Manage Doctors", "Add Doctor", "Model Metrics"])

    with tab1:
        st.header("Manage Doctors")

        doctors = load_doctors()

        if not doctors:
            st.warning("No doctors found in the system.")
        else:
            st.subheader(f"Total Doctors: {len(doctors)}")

            for idx, doctor in enumerate(doctors):
                with st.expander(f"{doctor.get('name', 'Unknown')} — {doctor.get('specialty', 'N/A')}"):
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        name = st.text_input("Name", value=doctor.get('name', ''), key=f"name_{idx}")
                        specialty = st.text_input("Specialty", value=doctor.get('specialty', ''), key=f"specialty_{idx}")
                        phone = st.text_input("Phone", value=doctor.get('phone', ''), key=f"phone_{idx}")
                        email = st.text_input("Email", value=doctor.get('email', ''), key=f"email_{idx}")
                        grade = st.selectbox(
                            "Grade",
                            ["lower", "higher"],
                            index=0 if doctor.get('grade') == 'lower' else 1,
                            key=f"grade_{idx}"
                        )

                        if st.button(f"Update Doctor {idx+1}", key=f"update_{idx}", use_container_width=True):
                            doctors[idx] = {
                                "name": name,
                                "specialty": specialty,
                                "phone": phone,
                                "email": email,
                                "grade": grade
                            }
                            save_doctors(doctors)
                            st.success(f"{name} updated successfully.")
                            st.rerun()

                    with col2:
                        if st.button("Delete", key=f"delete_{idx}", use_container_width=True, type="secondary"):
                            doctors.pop(idx)
                            save_doctors(doctors)
                            st.success("Doctor deleted successfully.")
                            st.rerun()

    with tab2:
        st.header("Add New Doctor")

        st.markdown("Fill in the doctor's information to add them to the system.")

        col1, col2 = st.columns(2)

        with col1:
            new_name = st.text_input("Doctor Name", placeholder="e.g., Dr. John Smith")
            new_specialty = st.text_input("Specialty", placeholder="e.g., Diabetes Specialist")
            new_phone = st.text_input("Phone Number", placeholder="e.g., +977-9840312345")

        with col2:
            new_email = st.text_input("Email Address", placeholder="e.g., doctor@email.com")

            st.info("""
            **Grading system:**
            *   **Higher:** For Critical Risk patients (**> 70%**).
            *   **Lower:** For Moderate Risk patients (**50% - 70%**).
            """)

            new_grade = st.selectbox(
                "Doctor Grade",
                ["lower", "higher"],
                help="Select 'Higher' for >70% risk or 'Lower' for 50-70% risk."
            )

        if st.button("Add Doctor", use_container_width=True, type="primary"):
            if not new_name or not new_specialty or not new_phone or not new_email:
                st.error("Please fill in all fields.")
            elif "@" not in new_email:
                st.error("Please enter a valid email address.")
            elif not new_phone.startswith("+"):
                st.error("Please enter a valid phone number (should start with +).")
            else:
                doctors = load_doctors()
                new_doctor = {
                    "name": new_name,
                    "specialty": new_specialty,
                    "phone": new_phone,
                    "email": new_email,
                    "grade": new_grade
                }
                doctors.append(new_doctor)
                save_doctors(doctors)
                st.success(f"{new_name} has been added successfully.")
                st.rerun()

    with tab3:
        st.header("Model Evaluation Metrics")
        
        metrics = load_model_metrics()
        
        if not metrics:
            st.warning("No model metrics found. Please train the model first by running: `python diabetes_prediction.py`")
        else:
            # Display key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Accuracy", f"{metrics.get('accuracy', 0):.2f}%")
            
            with col2:
                st.metric("F1 Score", f"{metrics.get('f1_score', 0):.4f}")
            
            with col3:
                st.metric("Precision", f"{metrics.get('precision', 0):.4f}")
            
            with col4:
                st.metric("Recall", f"{metrics.get('recall', 0):.4f}")
            
            st.divider()
            
            # Display Confusion Matrix Visualization
            st.subheader("Confusion Matrix Visualization")
            if os.path.exists("saved_models/confusion_matrix.png"):
                st.image("saved_models/confusion_matrix.png", use_container_width=True)
            else:
                st.info("Confusion matrix visualization not found. Train the model to generate it.")
            
            # Display Confusion Matrix as Table
            st.subheader("Confusion Matrix (Numerical)")
            cm = metrics.get('confusion_matrix', [])
            if cm:
                cm_df = pd.DataFrame(
                    cm,
                    index=["No Diabetes", "Diabetes"],
                    columns=["Predicted No Diabetes", "Predicted Diabetes"]
                )
                st.dataframe(cm_df, use_container_width=True)
            
            # Display Classification Report
            st.subheader("Classification Report")
            report = metrics.get('classification_report', '')
            if report:
                st.text(report)
