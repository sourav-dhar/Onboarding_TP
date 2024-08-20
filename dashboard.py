import streamlit as st
import pandas as pd
import altair as alt
import mysql.connector
from datetime import datetime

# Function to fetch data from the MySQL database
def fetch_data():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="TERRAPAY"
        )
        query = "SELECT * FROM Hityshi"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except mysql.connector.Error as err:
        st.error(f"Error fetching data: {err}")
        return pd.DataFrame()

def show():
    st.title("Dashboard")
    st.subheader("Trendline Visualizations for EDD Escalation Tasks")

    # Fetching data
    df = fetch_data()

    # Ensure that 'completion_date' is in datetime format
    df['completion_date'] = pd.to_datetime(df['completion_date'])

    # Adding columns for year, month, and week
    df['completion_year'] = df['completion_date'].dt.year
    df['completion_month'] = df['completion_date'].dt.month_name()

    # Explicitly sort months in the correct order
    month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    df['completion_month'] = pd.Categorical(df['completion_month'], categories=month_order, ordered=True)

    df['completion_week'] = df['completion_date'].dt.isocalendar().week

    # Summary Section
    st.subheader("Summary")
    total_tasks = len(df)
    top_performer = df.groupby('EDD_reviewer').size().idxmax()
    task_distribution = df['edd_escalation_tasks'].value_counts()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tasks Completed", total_tasks)
    col2.metric("Top Performer", top_performer)
    col3.metric("Most Common Task Type", task_distribution.idxmax())

    st.write("Task Distribution:")
    st.bar_chart(task_distribution)

    # Select year
    years = sorted(df['completion_year'].unique())
    selected_year = st.selectbox("Select Year for Analysis", years)

    # Filter data by selected year
    df_year = df[df['completion_year'] == selected_year]

    # Tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["Weekly Counts of Escalation Tasks", "Monthly Counts of All Escalation Tasks", "Week-wise Breakdowns of All Tasks", "Escalation Tasks Performed Associate-Wise"])

    with tab1:
        st.header("Weekly Counts of Escalation Tasks")
        # Select month
        selected_month = st.selectbox("Select Month", df_year['completion_month'].unique())
        df_month = df_year[df_year['completion_month'] == selected_month]

        # Weekly counts of escalation tasks as bar charts
        weekly_counts = df_month.groupby(['completion_week', 'edd_escalation_tasks']).size().reset_index(name='Count')

        weekly_chart = alt.Chart(weekly_counts).mark_bar().encode(
            x=alt.X('completion_week:O', title="Week"),
            y=alt.Y('Count:Q', title="Count"),
            color='edd_escalation_tasks:N'
        ).properties(
            title=f"Weekly Counts of Escalation Tasks for {selected_month} {selected_year}"
        )

        st.altair_chart(weekly_chart, use_container_width=True)

    with tab2:
        st.header("Monthly Counts of All Escalation Tasks")
        # Select month
        selected_month = st.selectbox("Select Month for Monthly Analysis", df_year['completion_month'].unique(), key='monthly')
        df_monthly = df_year[df_year['completion_month'] == selected_month]

        # Monthly counts of all escalation tasks
        monthly_counts = df_monthly['edd_escalation_tasks'].value_counts().reset_index(name='Count')

        # Renaming the index column to 'Task Type'
        monthly_counts.rename(columns={'index': 'Task Type'}, inplace=True)

        # Bar chart for monthly counts
        monthly_chart = alt.Chart(monthly_counts).mark_bar().encode(
            x=alt.X('Task Type:O', title="Task Type"),
            y=alt.Y('Count:Q', title="Count"),
            color=alt.condition(
                alt.datum['Count'] > 0,
                alt.value('steelblue'),
                alt.value('lightgray')
            )
        ).properties(
            title=f"Monthly Counts of All Escalation Tasks for {selected_month} {selected_year}"
        )

        # Display chart and table side by side
        col1, col2 = st.columns(2)
        with col1:
            st.altair_chart(monthly_chart, use_container_width=True)
        with col2:
            st.write("Monthly Counts Table")
            st.table(monthly_counts)

    with tab3:
        st.header("Week-wise Breakdowns of All Tasks")
        # Select month
        selected_month = st.selectbox("Select Month for Week-wise Breakdown", df_year['completion_month'].unique(), key='weekwise')
        df_weekwise = df_year[df_year['completion_month'] == selected_month]

        # Week-wise breakdowns of all tasks
        tasks = df_weekwise['edd_escalation_tasks'].unique()
        weeks = df_weekwise['completion_week'].unique()

        # Create two rows of charts in a 2x2 grid layout
        for task in tasks:
            weekwise_counts = df_weekwise[df_weekwise['edd_escalation_tasks'] == task].groupby('completion_week').size().reset_index(name='Count')
            weekwise_chart = alt.Chart(weekwise_counts).mark_bar().encode(
                x=alt.X('completion_week:O', title="Week"),
                y=alt.Y('Count:Q', title="Count"),
                color=alt.value('lightblue')
            ).properties(
                title=f"Weekly Breakdown of {task}"
            )
            st.altair_chart(weekwise_chart, use_container_width=True)

    with tab4:
        st.header("Escalation Tasks Performed Associate-Wise")
        # Select month
        selected_month = st.selectbox("Select Month for Associate Analysis", df_year['completion_month'].unique(), key='associate')
        df_associate = df_year[df_year['completion_month'] == selected_month]

        associates = df_associate['EDD_reviewer'].unique()

        for associate in associates:
            associate_data = df_associate[df_associate['EDD_reviewer'] == associate]
            associate_counts = associate_data.groupby(['completion_week', 'edd_escalation_tasks']).size().reset_index(name='Count')

            associate_chart = alt.Chart(associate_counts).mark_bar().encode(
                x=alt.X('completion_week:O', title="Week"),
                y=alt.Y('Count:Q', title="Count"),
                color='edd_escalation_tasks:N'
            ).properties(
                title=f"Weekly Task Counts for {associate} in {selected_month} {selected_year}"
            )

            st.altair_chart(associate_chart, use_container_width=True)

