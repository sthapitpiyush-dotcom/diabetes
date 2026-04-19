import streamlit as st

from auth import is_logged_in
from services.doctors import load_doctors


def show_landing_page(predictor=None):
    st.markdown('<h1 class="main-header">Diabetes Prediction System</h1>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Home", "Features"])

    with tab1:
        col_img, col_text = st.columns([1, 1.2])

        with col_img:
            try:
                st.image("diab.png", caption="Diabetes Health Monitoring", use_container_width=True)
            except Exception:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                           border-radius: 15px; padding: 60px 20px; text-align: center; color: white;">
                    <h2 style="font-size: 48px; margin: 0;">Health</h2>
                    <p style="font-size: 18px; margin: 10px 0;">Diabetes Health Monitoring</p>
                </div>
                """, unsafe_allow_html=True)

        with col_text:
            st.header("Take Control of Your Health")
            st.markdown("""
            ### About Our System

            The **Diabetes Prediction System** is an advanced health assessment platform designed to help you understand your diabetes risk. Using sophisticated analysis algorithms trained on extensive health data, we provide you with:

            - **Accurate risk assessment** — evaluate your diabetes risk in minutes

            - **Personalized insights** — detailed probability scores and analysis

            - **Expert recommendations** — connect with healthcare professionals

            - **Progress tracking** — monitor your health over time

            Early detection can save lives. Don't wait for symptoms to appear—assess your risk today and take control of your health!
            """)

            if not is_logged_in():
                col_btn = st.columns([1, 1, 1])
                with col_btn[0]:
                    if st.button("Get Started", key="get_started_btn", use_container_width=True, type="primary"):
                        st.session_state.current_page = "Login"
                        st.rerun()
                with col_btn[2]:
                    if st.button("Learn More", key="learn_more_btn", use_container_width=True):
                        st.session_state.current_page = "About Us"
                        st.rerun()

        st.markdown("---")

        st.subheader("Why This Matters")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="feature-card">
                <h3>Early Detection</h3>
                <p>Identify diabetes risk early before symptoms appear. Early intervention can prevent serious complications.</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="feature-card">
                <h3>Quick Assessment</h3>
                <p>Get instant risk assessment results in seconds. Simple form to fill with basic health metrics.</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="feature-card">
                <h3>Expert Guidance</h3>
                <p>Receive personalized doctor recommendations based on your risk level for professional consultation.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        st.subheader("How It Works")
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("""
            **Step 1: Input Health Information**
            - Enter your basic health metrics (glucose level, BMI, age, etc.)
            - Takes less than 2 minutes

            **Step 2: Get Instant Analysis**
            - Our advanced analysis evaluates your data
            - Provides risk probability score

            **Step 3: Receive Recommendations**
            - Get doctor recommendations based on your risk
            - View detailed probability analysis

            **Step 4: Take Action**
            - Consult with recommended healthcare professionals
            - Take preventive measures if needed
            """)

        with col1:
            st.info("**Tip:** Regular check-ups and healthy lifestyle choices are key to diabetes prevention.")

    with tab2:
        st.header("Key Features")
        st.markdown("Everything you need for diabetes risk assessment")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class="feature-card">
                <h3>Accurate Assessment</h3>
                <p>Advanced analysis using comprehensive health metrics to evaluate your diabetes risk.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="feature-card">
                <h3>Doctor Network</h3>
                <p>Connect with healthcare professionals who can provide personalized medical advice.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="feature-card">
                <h3>Data Visualization</h3>
                <p>Explore comprehensive data analysis with interactive charts and insights.</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="feature-card">
                <h3>Risk Scoring</h3>
                <p>Get detailed probability scores showing your likelihood of diabetes based on analysis.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="feature-card">
                <h3>History Tracking</h3>
                <p>Keep track of your assessments over time to monitor health trends.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="feature-card">
                <h3>Secure and Private</h3>
                <p>Your health data is protected with secure authentication and privacy controls.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.header("Our Network of Healthcare Professionals")
        st.markdown("We partner with qualified healthcare professionals to provide expert guidance based on your risk assessment.")

        doctors = load_doctors()

        if doctors:
            specialist_doctors = [d for d in doctors if d.get("grade") == "higher"]
            general_doctors = [d for d in doctors if d.get("grade") == "lower"]

            if specialist_doctors:
                st.subheader("Diabetes Specialists (High Risk)")
                spec_cols = st.columns(len(specialist_doctors))
                for idx, doctor in enumerate(specialist_doctors):
                    with spec_cols[idx]:
                        st.markdown(f"""
                        <div class="doctor-card">
                            <h4>{doctor.get('name', 'N/A')}</h4>
                            <p><strong>Specialty:</strong> {doctor.get('specialty', 'N/A')}</p>
                            <p><strong>Phone:</strong> {doctor.get('phone', 'N/A')}</p>
                            <p><strong>Email:</strong> {doctor.get('email', 'N/A')}</p>
                        </div>
                        """, unsafe_allow_html=True)

            if general_doctors:
                st.subheader("Diabetes Care Doctors (Moderate Risk)")
                gen_cols = st.columns(len(general_doctors) if len(general_doctors) <= 3 else 3)
                for idx, doctor in enumerate(general_doctors):
                    with gen_cols[idx % len(gen_cols)]:
                        st.markdown(f"""
                        <div class="doctor-card">
                            <h4>{doctor.get('name', 'N/A')}</h4>
                            <p><strong>Specialty:</strong> {doctor.get('specialty', 'N/A')}</p>
                            <p><strong>Phone:</strong> {doctor.get('phone', 'N/A')}</p>
                            <p><strong>Email:</strong> {doctor.get('email', 'N/A')}</p>
                        </div>
                        """, unsafe_allow_html=True)

            st.info("**Note:** After your risk assessment, you will receive personalized doctor recommendations based on your results. Log in to get started.")
