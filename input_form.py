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
            CREATE TABLE IF NOT EXISTS onboarding (
                id VARCHAR(255) PRIMARY KEY,
                completion_date DATE,
                partner_name VARCHAR(255),
                deal_type VARCHAR(255),
                review_type VARCHAR(255),
                escalation_type VARCHAR(255),
                EDD_reviewer VARCHAR(255),
                EDD_measures VARCHAR(255),
                timestamp TIMESTAMP
            )
        ''')
        conn.commit()
        c.close()
        conn.close()
        #st.write("Database initialized successfully.")
    except mysql.connector.Error as err:
        st.error(f"Error initializing database: {err}")


def insert_entry(entry_id, completion_date, partner_name, deal_type, review_type, escalation_type, EDD_reviewer, EDD_measures, timestamp):
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root",
            database="TERRAPAY"
        )
        c = conn.cursor()
        query = '''
            INSERT INTO onboarding (id, completion_date, partner_name, deal_type, review_type, escalation_type, EDD_reviewer, EDD_measures, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        #st.write(f"Executing query: {query}")
        c.execute(query, (entry_id, completion_date, partner_name, deal_type, review_type, escalation_type, EDD_reviewer, EDD_measures, timestamp))
        conn.commit()
        #st.write(f"Rows affected: {c.rowcount}")
        c.close()
        conn.close()
        #st.success(f"Entry submitted successfully at {timestamp}")
    except mysql.connector.Error as err:
        st.error(f"Error inserting entry: {err}")
'''        
def retrieve_entries():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root",
            database="TERRAPAY"
        )
        c = conn.cursor()
        c.execute('SELECT * FROM onboarding')
        rows = c.fetchall()
        conn.close()
        return rows
    except mysql.connector.Error as err:
        st.error(f"Error retrieving entries: {err}")
        return []
'''        
def show():
    st.title("Input Form")
    st.subheader("Enter your data below")

    # Initialize the database
    #st.write("Initializing database...")
    
    # Initialize the database
    init_db()

    completion_date = st.date_input("Completion Date", value=datetime.today())
    partner_name = st.text_input("Partner Name")
    deal_type = st.selectbox("Deal Type", ['', 'imt', 'payments', 'issuance', 'vendor'])
    review_type = st.selectbox("Review Type", ['', 'fresh_onboarding', 'periodic_review'])
    escalation_type = st.selectbox("Escalation Type", ['', 'other_red_flags', 'adverse_media', 'high_risk', 'pep_association', 'country_risk', 'complex_ownership', 'young_company', 'medium_risk', 'feedback_review'])
    EDD_reviewer = st.selectbox("EDD Reviewer", ['', 'neelima_routhu', 'francis_xavier', 'rohan_vazapully', 'rahil_fw', 'moustapha', 'laura_castillo', 'hityshi'])
    EDD_measures = st.selectbox("EDD Measures", ['', 'document_review', 'aml_review', 'audit_review', 'feedback_review'])
    
    
    if st.button("Submit"):
        # Validate required fields
        if not partner_name:
            st.error("Partner Name cannot be empty.")
        elif not EDD_reviewer:
            st.error("EDD Reviewer cannot be empty.")
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry_id = str(uuid.uuid4())  # Generate a unique entry ID

            # Replace empty strings with None (which will be treated as NULL in SQL)
            if deal_type == '': deal_type = None
            if review_type == '': review_type = None
            if escalation_type == '': escalation_type = None
            if EDD_measures == '': EDD_measures = None

            # Insert entry into the database
            insert_entry(entry_id, completion_date, partner_name, deal_type, review_type, escalation_type, EDD_reviewer, EDD_measures, timestamp)
            st.success(f"Entry submitted successfully at {timestamp}")