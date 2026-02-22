import streamlit as st
import mysql.connector
import pandas as pd
from mysql.connector import Error

# --- Database Configuration ---
DB_CONFIG = {
    "host": "82.180.143.66",
    "user": "u263681140_students",
    "password": "testStudents@123",
    "database": "u263681140_students"
}

def get_db_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        st.error(f"Connection Error: {e}")
        return None

# --- Authentication Logic ---
def check_login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("🔒 Admin Login")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Login")
            
            if login_btn:
                if username == "admin" and password == "admin":
                    st.session_state.logged_in = True
                    st.rerun() # Refresh to show the app
                else:
                    st.error("Invalid Username or Password")
        return False
    return True

def logout():
    st.session_state.logged_in = False
    st.rerun()

# --- Main App Logic ---
if check_login():
    # Sidebar for Logout
    with st.sidebar:
        st.write(f"Logged in as: **Admin**")
        if st.button("Logout"):
            logout()

    st.title("🔔 Electric Bell Management")

    # Create two tabs
    tab1, tab2 = st.tabs(["Set Bell Time", "View Scheduled Times"])

    # --- TAB 1: Insert Data ---
    with tab1:
        st.header("Schedule New Bell")
        with st.form("bell_form", clear_on_submit=True):
            b_time = st.text_input("Bell Time (HH:MM:SS:MS)", placeholder="11:11:17:28")
            duration = st.text_input("Duration", placeholder="e.g. 5")
            submit_button = st.form_submit_button("Save to Database")

        if submit_button:
            if b_time and duration:
                conn = get_db_connection()
                if conn:
                    cursor = conn.cursor()
                    query = "INSERT INTO ElectricBell (BTime, duration) VALUES (%s, %s)"
                    cursor.execute(query, (b_time, duration))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    st.success(f"Successfully scheduled: {b_time}")
            else:
                st.warning("Both fields are required.")

    # --- TAB 2: View Data ---
    with tab2:
        st.header("Current Bell Schedules")
        
        # Display data automatically or with refresh
        conn = get_db_connection()
        if conn:
            query = "SELECT id, BTime, duration FROM ElectricBell ORDER BY id DESC"
            df = pd.read_sql(query, conn)
            conn.close()
            
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No bell times have been set yet.")
        
        if st.button("Refresh Data"):
            st.rerun()
