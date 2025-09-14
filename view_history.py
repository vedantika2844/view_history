import streamlit as st
import mysql.connector
import pandas as pd

# ---------- DB Connection ----------
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

# ---------- Main Logic ----------
st.set_page_config(page_title="View History", layout="wide")

st.title("📖 Patient Medical History")

# ✅ Read RFID from URL query
rfid_filter = st.query_params.get("rfid_filter", [None])[0]

if not rfid_filter:
    st.warning("No RFID provided in URL.")
    st.stop()

# ✅ Show Medical History
st.subheader(f"Medical History for RFID: `{rfid_filter}`")

try:
    data = get_all_medical_history()
    filtered_data = [r for r in data if r.get('RFID_No') == rfid_filter or r.get('RFIDNO') == rfid_filter]

    if filtered_data:
        df = pd.DataFrame(filtered_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No medical history records found for this RFID.")

except Exception as e:
    st.error(f"❌ Error: {e}")

# Back button
st.markdown("[🔙 Back to Home](./)", unsafe_allow_html=True)

