import streamlit as st

from auth import is_logged_in


def show_about_page():
    if not is_logged_in():
        col_back = st.columns([1, 3, 1])
        with col_back[0]:
            if st.button("Back to Home", key="back_home_from_about", use_container_width=True):
                st.session_state.current_page = "Home"
                st.rerun()

    st.markdown('<h1 class="main-header">About Us</h1>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["About Website", "Our Mission", "How to Use"])

    with tab1:
        st.header("About Diabetes Prediction System")

        st.markdown("""
        ### What is This System?

        The **Diabetes Prediction System** is a web-based health assessment tool designed to help individuals
        evaluate their risk of developing diabetes. It combines advanced data analysis with a user-friendly interface
        to provide quick, reliable risk assessments.

        ---

        ### Technology Behind

        Our system uses machine learning algorithms trained on extensive health datasets to analyze your
        health metrics and provide accurate risk predictions. The system evaluates multiple health factors including:

        - **Glucose Level** - Blood sugar measurements
        - **BMI (Body Mass Index)** - Weight relative to height
        - **Age** - Demographic risk factor
        - **Pregnancies** - Reproductive history (for women)
        - **Skin Thickness** - Body composition indicator

        ---

        ### Key Features
        """)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Response Time", "Instant", "< 1 second")
        with col2:
            st.metric("Accuracy", "High", "Based on ML")
        with col3:
            st.metric("Security", "Protected", "User Auth")

        st.markdown("""
        ---

        ### Why Use This System?

        1. **Early Detection** - Identify risk before symptoms appear
        2. **Convenient** - Access from anywhere, anytime
        3. **Free Assessment** - No cost to check your risk
        4. **Professional Support** - Get doctor recommendations
        5. **Track Progress** - Monitor your health over time
        """)

    with tab2:
        st.header("Our Mission")

        st.markdown("""
        ### Making Healthcare Accessible

        Our mission is to **democratize health assessment** by providing an easy-to-use,
        accurate, and accessible tool for diabetes risk evaluation.

        We believe that:

        - **Health information should be accessible to everyone**
        - Not everyone has immediate access to healthcare professionals
        - Early warning signs can be detected with the right tools

        - **Prevention is better than treatment**
        - Early detection saves lives
        - Informed decisions lead to better health outcomes
        - Awareness drives preventive action

        - **Technology should serve healthcare**
        - Machine learning can enhance human decision-making
        - Not replace doctors, but support them
        - User-friendly interfaces improve health literacy

        ---

        ### Who We Serve

        - **Individuals** concerned about their diabetes risk
        - **Healthcare professionals** seeking assessment tools
        - **Families** wanting to monitor health trends
        - **Organizations** promoting health awareness

        ---

        ### Our Commitment

        We are committed to:
        - Providing accurate assessments
        - Protecting your privacy
        - Keeping the system simple and user-friendly
        - Supporting legitimate medical consultation
        """)

    with tab3:
        st.header("How to Use This Website")

        st.markdown("""
        ### Getting Started

        #### Step 1: Create an Account or Login
        - Use the credentials provided (or create your own)
        - Your data is securely protected

        #### Step 2: Make Your First Assessment
        1. Go to the **Prediction** page
        2. Enter your health information:
           - Gender
           - Age
           - Height & Weight (for BMI calculation)
           - Glucose level
           - Skin thickness
           - Number of pregnancies (if female)
        3. Click **Predict** button

        #### Step 3: Review Your Results
        - See your risk assessment (High/Low)
        - Check probability scores (0-100%)
        - Get doctor recommendations if applicable
        - Save the result to your history

        #### Step 4: Track Your Health
        - Visit **History** to see all your assessments
        - Monitor changes over time
        - Share results with healthcare providers

        #### Step 5: Explore More
        - **Model Performance** — see how accurate our system is
        - **Data Analysis** — understand diabetes patterns

        ---

        ### Tips for Best Results

        - **Use accurate health data** — the more accurate your input, the better the assessment

        - **Get professional advice** — this tool supplements, not replaces, medical professionals

        - **Regular check-ups** — use this alongside regular health check-ups

        - **Healthy lifestyle** — prevention through diet and exercise is key

        - **Track your data** — keep records of your assessments to see trends

        ---

        ### Important Note

        **Disclaimer:** This tool is for informational purposes only and should not replace professional medical advice.
        Always consult with a healthcare professional for proper diagnosis and treatment.
        """)
