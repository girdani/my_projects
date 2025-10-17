import streamlit
import re

def login():
    streamlit.title("Login")

    role = streamlit.selectbox("Select your role:", ["Patient", "Admin"])
    email = streamlit.text_input("Email")

    if streamlit.button("Login"):
        if not email.strip():
            streamlit.error("Please enter your email.")
            return None, None

        # Basic email regex pattern
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, email):
            streamlit.error("Please enter a valid email address.")
            return None, None

        streamlit.success(f"Logged in as {role} with email: {email}")
        return role, email

    return None, None
