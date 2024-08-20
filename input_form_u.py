import streamlit as st 
import pandas as pd
import plotly.express as px 
import mysql.connector
from datetime import datetime
import uuid  # For generating unique entry IDs

def init_db():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root",
            database="TERRAPAY"
        )
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS Hityshi (
                id VARCHAR(255) PRIMARY KEY,
                completion_date DATE,
                partner_name VARCHAR(255),
                deal_type VARCHAR(255),
                review_type VARCHAR(255),
                edd_escalation_tasks VARCHAR(255),
                EDD_reviewer VARCHAR(255),
                comments TEXT,
                timestamp TIMESTAMP
            )
        ''')
        conn.commit()
        c.close()
        conn.close()
    except mysql.connector.Error as err:
        st.error(f"Error initializing database: {err}")

def generate_custom_id(partner_name, deal_type):
    # Get the first three letters of the partner name and deal type
    partner_part = partner_name[:3].upper() if partner_name else "XXX"
    deal_part = deal_type[:3].upper() if deal_type else "XXX"
    
    # Get a timestamp in the format YYYYMMDDHHMMSS
    timestamp_part = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Combine parts to form the ID
    custom_id = f"{partner_part}_{deal_part}_{timestamp_part}"
    return custom_id

def insert_entry(entry_id, completion_date, partner_name, deal_type, review_type, edd_escalation_tasks, EDD_reviewer, comments, timestamp):
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root",
            database="TERRAPAY"
        )
        c = conn.cursor()
        query = '''
            INSERT INTO Hityshi (id, completion_date, partner_name, deal_type, review_type, edd_escalation_tasks, EDD_reviewer, comments, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        c.execute(query, (entry_id, completion_date, partner_name, deal_type, review_type, edd_escalation_tasks, EDD_reviewer, comments, timestamp))
        conn.commit()
        c.close()
        conn.close()
    except mysql.connector.Error as err:
        st.error(f"Error inserting entry: {err}")

def show():
    st.title("Input Form")
    st.subheader("Enter your data below")

    # Initialize the database
    init_db()

    # Input fields
    completion_date = st.date_input("Completion Date", value=datetime.today())
    partner_name = st.text_input("Partner Name")
    deal_type = st.selectbox("Deal Type", ['', 'imt', 'payments', 'issuance', 'vendor'])
    review_type = st.selectbox("Review Type", ['', 'fresh_onboarding', 'periodic_review'])
    
    edd_escalation_tasks = st.selectbox(
        "EDD/Escalation Tasks", 
        ['', 'document_review', 'aml_review', 'audit_review', 'feedback_review', 'other_red_flags', 'adverse_media', 'high_risk', 'pep_association', 'country_risk', 'complex_ownership', 'young_company', 'medium_risk']
    )
    
    EDD_reviewer = st.selectbox("EDD Reviewer", ['', 'neelima_routhu', 'francis_xavier', 'rohan_vazapully', 'rahil_fw', 'moustapha', 'laura_castillo', 'hityshi'])
    comments = st.text_area("Comments", placeholder="Enter any additional comments or notes here.")

    if st.button("Submit"):
        # Validate required fields
        if not partner_name:
            st.error("Partner Name cannot be empty.")
        elif not EDD_reviewer:
            st.error("EDD Reviewer cannot be empty.")
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Generate a custom ID
            entry_id = generate_custom_id(partner_name, deal_type)

            # Replace empty strings with None (which will be treated as NULL in SQL)
            if deal_type == '': deal_type = None
            if review_type == '': review_type = None
            if edd_escalation_tasks == '': edd_escalation_tasks = None
            if comments == '': comments = None

            # Insert entry into the database
            insert_entry(entry_id, completion_date, partner_name, deal_type, review_type, edd_escalation_tasks, EDD_reviewer, comments, timestamp)
            st.success(f"Entry submitted successfully at {timestamp}")

    # Enhance UI with CSS (can be expanded or modified as needed)
    st.markdown("""
    <style>
        .stButton button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .stTextInput input, .stTextArea textarea, .stSelectbox select {
            background-color: #f1f1f1;
            border: 2px solid #ccc;
            border-radius: 5px;
            padding: 10px;
        }
        .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox select:focus {
            border-color: #007BFF;
            outline: none;
        }
    </style>
    """, unsafe_allow_html=True)


if __name__=="__main__":
    show()