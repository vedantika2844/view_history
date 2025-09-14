import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime

# ---------- DB Connection ----------
def get_connection():
    return mysql.connector.connect(
        host="82.180.143.66",
        user="u263681140_students",
        password="testStudents@123",
        database="u263681140_students"
    )

# ---------- DB Queries ----------
def insert_patient(data):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
    INSERT INTO E_casepatient 
    (Name, RFIDNO, Age, Gender, BloodGroup, DateofBirth, ContactNo, EmailID, Address, DoctorAssigned)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, data)
    conn.commit()
    cursor.close()
    conn.close()

def get_all_patients():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM E_casepatient ORDER BY ID DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_all_medical_history():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM medical_histroy ORDER BY ID DESC")
        rows = cursor.fetchall()
        if not rows or cursor.description is None:
            return []
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        st.error(f"❌ Error fetching medical history: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_current_appointments(): 
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT * FROM E_Case
            ORDER BY Date_Time DESC
        """)
        rows = cursor.fetchall()
        
        for row in rows:
            rfid_no = row.get('RFID_No', '')
            row['Status'] = f'<a href="./view_history?rfid_filter={rfid_no}" target="_blank">View History</a>'
        return rows
    except Exception as e:
        st.error(f"❌ Failed to fetch appointments: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# ---------- Streamlit App ----------
st.set_page_config(page_title="Patient Registration System", layout="wide")
st.title("🧾 Patient Registration System")

menu = st.sidebar.radio("Menu", ["Register Patient", "View All Patients", "View Medical History", "Current Appointments"])

# ---------- Register Patient ----------
if menu == "Register Patient":
    with st.form("patient_form"):
        st.subheader("Register New Patient")
        name = st.text_input("Full Name")
        rfid = st.text_input("RFID No")
        age = st.text_input("Age")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        blood_group = st.text_input("Blood Group")
        dob = st.date_input("Date of Birth")
        contact = st.text_input("Contact Number")
        email = st.text_input("Email ID")
        address = st.text_area("Address")
        doctor = st.text_input("Doctor Assigned")

        submitted = st.form_submit_button("Register Patient")
        if submitted:
            try:
                age = int(age)
                dob_str = dob.strftime('%Y-%m-%d')
                insert_patient((name, rfid, age, gender, blood_group, dob_str, contact, email, address, doctor))
                st.success("✅ Patient registered successfully!")
            except ValueError:
                st.error("❌ Age must be a number.")
            except Exception as e:
                st.error(f"❌ Error: {e
