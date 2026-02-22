import streamlit as st
import mysql.connector
from mysql.connector import Error

# Database Configuration
DB_CONFIG = {
    "host": "82.180.143.66",
    "user": "u263681140_students",
    "password": "testStudents@123",
    "database": "u263681140_students"
}

def insert_bell_data(btime, duration):
    try:
        # Establish connection
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            cursor = conn.cursor()
            # Prepare SQL Query
            query = "INSERT INTO ElectricBell (BTime, duration) VALUES (%s, %s)"
            cursor.execute(query, (btime, duration))
            conn.commit()
            return True
    except Error as e:
        st.error(f"Error: {e}")
        return False
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# --- Streamlit UI ---
st.title("🔔 Electric Bell Scheduler")

with st.form("bell_form"):
    st.write("Enter the bell schedule details below:")
    
    # Input for BTime using your specific format
    b_time = st.text_input("Bell Time (Format: 11:11:17:28)", placeholder="HH:MM:SS:MS")
    
    # Input for Duration
    duration = st.text_input("Duration (in seconds or ms)", placeholder="e.g. 5")
    
    submit_button = st.form_submit_button("Insert to Database")

if submit_button:
    if b_time and duration:
        success = insert_bell_data(b_time, duration)
        if success:
            st.success(f"Successfully inserted: Time {b_time} with duration {duration}")
    else:
        st.warning("Please fill in both fields.")
