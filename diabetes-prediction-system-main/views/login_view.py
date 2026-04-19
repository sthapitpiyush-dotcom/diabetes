import streamlit as st

from auth import is_logged_in, login, signup


def show_login_page():
    if not is_logged_in():
        col_back = st.columns([1, 3, 1])
        with col_back[0]:
            if st.button("Back to Home", key="back_home_from_login", use_container_width=True):
                st.session_state.current_page = "Home"
                st.rerun()

    st.markdown('<h1 class="main-header">Login / Sign Up</h1>', unsafe_allow_html=True)

    show_login_after_signup = st.session_state.get("show_login_after_signup", False)
    if show_login_after_signup:
        st.session_state.show_login_after_signup = False
        st.info("Account created successfully. Please log in with your new credentials below.")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            with st.form("login_form"):
                st.subheader("Enter your credentials")
                username = st.text_input("Username", key="login_username")
                password = st.text_input("Password", type="password", key="login_password")
                submit_button = st.form_submit_button("Login", type="primary", use_container_width=True)

                if submit_button:
                    if login(username, password):
                        st.success(f"Welcome back, {username}!")
                        st.session_state.current_page = "Home"
                        st.session_state.show_login_success = True
                        st.rerun()
                    else:
                        st.error("Invalid username or password")

            st.markdown("---")
            st.info("**Default Credentials:**\n- Username: `admin` / Password: `admin123`\n- Username: `user` / Password: `user123`")

    with tab2:
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            with st.form("signup_form"):
                st.subheader("Create a new account")
                new_username = st.text_input("Username", key="signup_username")
                new_password = st.text_input("Password", type="password", key="signup_password")
                confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
                signup_button = st.form_submit_button("Sign Up", type="primary", use_container_width=True)

                if signup_button:
                    success, message = signup(new_username, new_password, confirm_password)
                    if success:
                        st.success(message)
                        st.session_state.show_login_after_signup = True
                        st.rerun()
                    else:
                        st.error(message)
