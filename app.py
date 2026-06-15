import streamlit as st
import pandas as pd
import sqlite3

# ഡാറ്റാബേസ് സെറ്റപ്പ്
def init_db():
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS attendance 
                 (date TEXT, class_section TEXT, student_name TEXT, status TEXT, reason TEXT)''')
    conn.commit()
    conn.close()

# ഡാറ്റ സേവ് ചെയ്യുന്ന ഫംഗ്ഷൻ
def save_attendance(date, class_section, student_name, status, reason):
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    c.execute("INSERT INTO attendance VALUES (?, ?, ?, ?, ?)", 
              (date, class_section, student_name, status, reason))
    conn.commit()
    conn.close()

# ഡാറ്റ തിരിച്ചു കാണാനുള്ള ഫംഗ്ഷൻ
def get_attendance():
    conn = sqlite3.connect('school.db')
    df = pd.read_sql_query("SELECT * FROM attendance", conn)
    conn.close()
    return df

init_db()

st.title("My School Portal")

# അറ്റൻഡൻസ് ഫോം
with st.form("attendance_form"):
    selected_date = st.date_input("Date")
    class_section = st.text_input("Class/Section")
    student_name = st.text_input("Student Name")
    status = st.selectbox("Status", ["Present", "Absent"])
    reason = st.text_input("Reason (if absent)")
    
    submit = st.form_submit_button("Save Attendance")

    if submit:
        save_attendance(str(selected_date), class_section, student_name, status, reason)
        st.success("Attendance saved successfully!")

# ഡാഷ്ബോർഡ് (ഡാറ്റ കാണാൻ)
st.subheader("Attendance Records")
df = get_attendance()
st.dataframe(df)

# ഡാറ്റ ഡൗൺലോഡ് ചെയ്യാനുള്ള സൗകര്യം
if not df.empty:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Data as CSV", csv, "attendance.csv", "text/csv")
