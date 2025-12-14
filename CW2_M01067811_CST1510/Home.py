import streamlit as st
import bcrypt
from app.data.db import connect_database
from app.data.users import get_user_by_username,insert_user
# ========== OOP IMPORTS ==========
from services.database_manager import DatabaseManager

# Initializing OOP services
db_manager = DatabaseManager("DATA/intelligence_platforms.db")


# Page configuration
st.set_page_config(
    layout="wide",
    page_title="Intelligence Platform Dashboard"
)

# Initializing session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

# Initializing users storage
if "users" not in st.session_state:
    st.session_state.users = {}


st.title("Multi-Domain Intelligence Platform")

#Conection to the database 
db_path = 'DATA/intelligence_platforms.db'
conn = connect_database(db_path)

# Checking if user is logged in AND showing dashboard
if st.session_state.logged_in:
    st.success(f"Welcome {st.session_state.username}!")
    st.write("You are now logged in.")
    st.info("Redirecting to Dashboard...")
    #Navigating to different dashboard pages
    st.header("Dashboard Navigation")

    cols=st.columns(4)
    with cols[0]:
         if st.button("🔒 Cybersecurity", use_container_width=True):
            st.switch_page("pages/1_Cybersecurity.py")
    with cols[1]:
         if st.button("📊 Data Science", use_container_width=True):
            st.switch_page("pages/2_Data_Science.py")
    with cols[2]:
         if st.button("🖥️ IT Operations", use_container_width=True):
            st.switch_page("pages/3_IT_Operations.py")
    with cols[3]:
        if st.button("🤖 AI Assistant", use_container_width=True):
            st.switch_page("pages/AI_Chat.py")

    #Quick overwiew metrics
    st.divider()
    st.subheader("Quick Overview")
    
    metric_cols = st.columns(3)
    with metric_cols[0]:
        st.metric("Security Events", "24", delta="+12%")
    with metric_cols[1]:
        st.metric("ML Accuracy", "95.2%", delta="+0.5%")
    with metric_cols[2]:
        st.metric("System Uptime", "99.9%", delta="+0.1%")


    if st.button("Logout",type="secondary"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
    
    
    
else:
    # TABS for login and registration
    tab_login, tab_register = st.tabs(["Login", "Register"])

    # LOGIN Tab
    with tab_login:
        st.subheader("Login")
        
        login_username = st.text_input("Username", key="login_user")
        login_password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Log In", key="login_btn"):
            if login_username in st.session_state.users:
                stored_hash = st.session_state.users[login_username]
                if bcrypt.checkpw(login_password.encode("utf-8"), stored_hash.encode("utf-8")):
                    st.session_state.logged_in = True
                    st.session_state.username = login_username
                    st.session_state.role = "user"
                    st.success("Login successful! Redirecting...")
                    st.rerun()
                    
                else:
                    st.error("Incorrect password")
            else:
                st.error("User not found")

    # Registration Tab
    with tab_register:
        st.subheader("Create Account")
        new_username = st.text_input("Choose Username", key="reg_user")
        new_password = st.text_input("Choose Password", type="password", key="reg_pass")
        confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")

        if st.button("Register", key="reg_btn",type="primary"):
            if not new_username or not new_password:
                st.warning("Please fill out all fields")
            elif new_password != confirm_password:
                st.error("Passwords do not match")
            elif new_username in st.session_state.users:
                st.error("Username already exists")
            else:
                # Hash password and store
                hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
                st.session_state.users[new_username] = hashed.decode("utf-8")
                st.success("Account created! Please log in.")    
                try:
                    insert_user(new_username, hashed.decode("utf-8"))
                    st.success("Account saved to database!")
                except Exception as e:
                    st.error(f"Registration failed: {e}")