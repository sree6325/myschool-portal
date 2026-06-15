import streamlit as st
import pandas as pd
from datetime import date
import sqlite3

# 0. ഡാറ്റാബേസ് സെറ്റപ്പ്
def init_db():
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS attendance 
                 (date TEXT, class_section TEXT, student_name TEXT, status TEXT, reason TEXT)''')
    conn.commit()
    conn.close()

def save_attendance(date, class_section, student_name, status, reason):
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    c.execute("INSERT INTO attendance VALUES (?, ?, ?, ?, ?)", 
              (date, class_section, student_name, status, reason))
    conn.commit()
    conn.close()

init_db()

# 1. Page Configuration
st.set_page_config(page_title="Dechentsemo Central School", layout="wide")
st.markdown("<h1 style='text-align: center; color: #1f77b4;'>🏫 DECHENTSEMO CENTRAL SCHOOL</h1>", unsafe_allow_html=True)

# 2. Initialization
if 'students_list' not in st.session_state:
    st.session_state.students_list = pd.DataFrame([
        {'Class_Section': '8A', 'Admission_No': '101', 'Name': 'Rahul'},
        {'Class_Section': '8A', 'Admission_No': '102', 'Name': 'Rahul'},
        {'Class_Section': '9B', 'Admission_No': '201', 'Name': 'Fathima'}
    ])

if 'attendance_df' not in st.session_state:
    st.session_state.attendance_df = pd.DataFrame(columns=['Date', 'Class_Section', 'Name', 'Status', 'Reason'])
if 'records_df' not in st.session_state:
    st.session_state.records_df = pd.DataFrame(columns=['Date', 'Class_Section', 'Type', 'Detail'])

# 3. Logic
# ഇവിടെ നിങ്ങളുടെ പഴയ ഫിൽട്ടർ കോഡ് വരും (filtered = ... )
# ഉദാഹരണത്തിന്:
filtered = st.session_state.students_list
sel_name = st.selectbox("Select Student", filtered['Name'].unique())
student_info = filtered[filtered['Name'] == sel_name]
selected_date = st.date_input("Date", date.today())

# 4. Tabs
tab1, tab2 = st.tabs(["Attendance", "Discipline & Achievement"])

with tab1:
    with st.form("att_form"):
        status = st.radio("Status", ["Present", "Absent"])
        reason = st.text_input("Reason (if Absent)")
        if st.form_submit_button("Save Attendance"):
            class_section = student_info['Class_Section'].iloc[0]
            # DB സേവ്
            save_attendance(str(selected_date), class_section, sel_name, status, reason)
            # സ്‌ക്രീനിൽ കാണിക്കാൻ
            new_row = {'Date': selected_date, 'Class_Section': class_section, 'Name': sel_name, 'Status': status, 'Reason': reason}
            st.session_state.attendance_df = pd.concat([st.session_state.attendance_df, pd.DataFrame([new_row])])
            st.success("Attendance saved!")

with tab2:
    with st.form("rec_form"):
        rec_type = st.selectbox("Type", ["Discipline Issue", "Achievement"])
        detail = st.text_area("Details")
        if st.form_submit_button("Save Record"):
            new_rec = {'Date': selected_date, 'Class_Section': student_info['Class_Section'].iloc[0], 'Type': rec_type, 'Detail': detail}
            st.session_state.records_df = pd.concat([st.session_state.records_df, pd.DataFrame([new_rec])])
            st.success("Record Saved!")

# 5. Dashboard
st.subheader("Attendance Records")
st.dataframe(st.session_state.attendance_df)
