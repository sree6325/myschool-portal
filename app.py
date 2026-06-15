import streamlit as st
import pandas as pd
from datetime import date
import sqlite3
# ഡാറ്റാബേസ് കണക്ഷൻ
def init_db():
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    # അറ്റൻഡൻസ് സേവ് ചെയ്യാൻ ടേബിൾ ഉണ്ടാക്കുന്നു
    c.execute('''CREATE TABLE IF NOT EXISTS attendance 
                 (date TEXT, class_section TEXT, student_name TEXT, status TEXT, reason TEXT)''')
    conn.commit()
    conn.close()

# ഡാറ്റ സേവ് ചെയ്യാൻ
def save_attendance(date, class_section, student_name, status, reason):
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    c.execute("INSERT INTO attendance VALUES (?, ?, ?, ?, ?)", 
              (date, class_section, student_name, status, reason))
    conn.commit()
    conn.close()

# ആപ്പ് റൺ ചെയ്യുമ്പോൾ ഡാറ്റാബേസ് ഉണ്ടെന്ന് ഉറപ്പാക്കുന്നു
init_db()
# 1. Page Configuration
st.set_page_config(page_title="Dechentsemo Central School", layout="wide")
st.markdown("<h1 style='text-align: center; color: #1f77b4;'>🏫 DECHENTSEMO CENTRAL SCHOOL</h1>", unsafe_allow_html=True)

# 2. Initialization (Session State)
if 'students_list' not in st.session_state:
    st.session_state.students_list = pd.DataFrame([
        {'Class_Section': '8A', 'Admission_No': '101', 'Name': 'Rahul'},
        {'Class_Section': '8A', 'Admission_No': '102', 'Name': 'Rahul'},
        {'Class_Section': '9B', 'Admission_No': '201', 'Name': 'Fathima'}
    ])

if 'attendance_df' not in st.session_state:
    st.session_state.attendance_df = pd.DataFrame(columns=['Date', 'Class_Section', 'Admission_No', 'Student_Name', 'Status', 'Reason'])
if 'records_df' not in st.session_state:
    st.session_state.records_df = pd.DataFrame(columns=['Date', 'Class_Section', 'Admission_No', 'Student_Name', 'Type', 'Detail'])

# 3. Sidebar Navigation
menu = st.sidebar.radio("Navigation", ["Teacher Portal", "Principal Dashboard"])

# 4. Teacher Portal Logic
if menu == "Teacher Portal":
    st.subheader("👨‍🏫 Teacher Entry Portal")
    sel_class_sec = st.selectbox("Select Class & Section", sorted(st.session_state.students_list['Class_Section'].unique()))
    filtered = st.session_state.students_list[st.session_state.students_list['Class_Section'] == sel_class_sec]
    
    def get_display_name(row):
        return f"{row['Name']} ({row['Admission_No']})"
    
    filtered['Display'] = filtered.apply(get_display_name, axis=1)
    sel_name = st.selectbox("Select Student", filtered['Display'].tolist())
    student_info = filtered[filtered['Display'] == sel_name].iloc[0]
    selected_date = st.date_input("Date", date.today())
    
    tab1, tab2 = st.tabs(["Attendance", "Discipline & Achievements"])
    with tab1:
        with st.form("att_form"):
            status = st.radio("Status", ["Present", "Absent"], horizontal=True)
            reason = st.text_input("Reason (if Absent)")
if st.form_submit_button("Save Attendance"):
            # 1. ഡാറ്റാബേസിലേക്ക് സേവ് ചെയ്യുന്നു
            class_section = student_info['Class_Section'].iloc[0]
            save_attendance(str(selected_date), class_section, sel_name, status, reason)

            # 2. പഴയ കോഡ് (ഇത് ആപ്പിൽ ഡാറ്റ കാണിക്കാൻ ആവശ്യമാണ്)
            new_row = {'Date': selected_date, 'Class_Section': class_section, 'Name': sel_name, 'Status': status, 'Reason': reason}
            st.session_state.attendance_df = pd.concat([st.session_state.attendance_df, pd.DataFrame([new_row])])
            st.success("Attendance saved!")

    with tab2:
        with st.form("rec_form"):
            rec_type = st.selectbox("Type", ["Discipline Issue", "Achievement"])
            detail = st.text_area("Details")
            if st.form_submit_button("Save Record"):
                new_rec = {'Date': selected_date, 'Class_Section': sel_class_sec, 'Admission_No': student_info['Admission_No'], 'Student_Name': student_info['Name'], 'Type': rec_type, 'Detail': detail}
                st.session_state.records_df = pd.concat([st.session_state.records_df, pd.DataFrame([new_rec])], ignore_index=True)
                st.success("Record Saved!")

# 5. Principal Dashboard Logic
elif menu == "Principal Dashboard":
    st.subheader("👔 Principal's Executive Dashboard")
    st.dataframe(st.session_state.attendance_df, use_container_width=True)
    st.dataframe(st.session_state.records_df, use_container_width=True)
