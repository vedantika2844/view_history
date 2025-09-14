import streamlit as st
import mysql.connector
import pandas as pd

# ---------- Database Connection ----------
def get_connection():
    return mysql.connector.connect(
        host="82.180.143.66",
        user="u263681140_students",
        password="testStudents@123",
        database="u263681140_students"
    )

# ---------- Fetch Medical History ----------
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

# ---------- Streamlit Page Config ----------
st.set_page_config(page_title="📖 View Patient History", layout="wide")

# ---------- Get RFID from URL ----------
rfid_filter = st.query_params.get("rfid_filter", [None])[0]

if not rfid_filter:
    st.warning("⚠️ No RFID passed. Please open from the main app.")
    st.stop()

st.title("📖 Patient Medical History")
st.subheader(f"🔎 History for RFID: `{rfid_filter}`")

# ---------- Load and Filter History ----------
try:
    history_data = get_all_medical_history()
    filtered = [r for r in history_data if r.get('RFID_No') == rfid_filter or r.get('RFIDNO') == rfid_filter]

    if filtered:
        df = pd.DataFrame(filtered)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No medical history records found for this RFID.")
except Exception as e:
    st.error(f"❌ Error loading history: {e}")

# ---------- Back Button ----------
st.markdown("[🔙 Back to Home](./)", unsafe_allow_html=True)
