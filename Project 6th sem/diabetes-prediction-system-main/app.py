import streamlit as st

from auth import is_logged_in, is_admin, logout, get_current_user
from services.doctors import initialize_doctors
from services.predictor import load_model
from styles import apply_app_styles
from views.about import show_about_page
from views.admin import show_admin_panel
from views.history import show_history_page
from views.landing import show_landing_page
from views.login_view import show_login_page
from views.prediction import show_prediction_page

st.set_page_config(
    page_title="Diabetes Prediction System",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': "Diabetes Prediction System v1.0"}
)

apply_app_styles()


def main():
    initialize_doctors()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"
    if "show_login_success" not in st.session_state:
        st.session_state.show_login_success = False

    if is_logged_in():
        st.sidebar.title("Navigation")
        user = get_current_user()
        st.sidebar.success(f"Logged in as: **{user}**")
        if st.sidebar.button("Logout", use_container_width=True):
            logout()
            st.session_state.current_page = "Home"
            st.rerun()

        if is_admin():
            page = st.sidebar.radio(
                "Choose a page",
                ["Home", "About Us", "Prediction", "History", "Admin Panel"]
            )
        else:
            page = st.sidebar.radio(
                "Choose a page",
                ["Home", "About Us", "Prediction", "History"]
            )
    else:
        if "current_page" not in st.session_state:
            st.session_state.current_page = "Home"

        page = st.session_state.current_page

        valid_pages = ["Home", "About Us", "Login"]
        if page not in valid_pages:
            page = "Home"
            st.session_state.current_page = "Home"

    if page == "Home":
        show_landing_page()
    elif page == "About Us":
        show_about_page()
    elif page == "Login":
        show_login_page()
    elif page == "Prediction" and is_logged_in():
        if 'predictor' not in st.session_state:
            with st.spinner("Loading model..."):
                st.session_state.predictor = load_model()
        show_prediction_page(st.session_state.predictor)
    elif page == "History" and is_logged_in():
        show_history_page()
    elif page == "Admin Panel" and is_logged_in() and is_admin():
        show_admin_panel()
    elif not is_logged_in() and page not in ("Home", "About Us", "Login"):
        st.warning("Please login to access this page.")
        show_login_page()


if __name__ == "__main__":
    main()
