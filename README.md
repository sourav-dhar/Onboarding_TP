streamlit_app/
│
├── scripts/
│   ├── input_form.py
│   ├── data_download.py
│   ├── data_visualization.py
│   ├── transformed_data_display.py
│   ├── dashboard.py
│   ├── report_scheduling.py
│
├── app.py
├── requirements.txt

 completion_date, partner_name, deal_type, review_type, escalation_type, QC_analyst, partner_name, EDD_reviewer, EDD_measures







 import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, GridUpdateMode, DataReturnMode
import plotly.express as px
import plotly.graph_objects as go
import mysql.connector
from datetime import datetime
import time
from io import BytesIO

# Define weights for each escalation type and EDD measure
weights = {
    'other_red_flags': 1,
    'adverse_media': 3,
    'high_risk': 5,
    'pep_association': 3,
    'country_risk': 1,
    'complex_ownership': 1,
    'young_company': 1,
    'medium_risk': 4,
    'combined_reviews': 2  # Combined weight for document review, aml review, audit review, and feedback review
}

def fetch_transformed_data(selected_dates):
    try:
        # Establish database connection
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='TERRAPAY'
        )

        # Fetch data
        query = "SELECT * FROM onboarding"
        df = pd.read_sql(query, conn)
        st.write("Fetched data from database:", df.head())

        # Filter data based on selected dates
        df = df[df['completion_date'].isin(selected_dates)]
        st.write("Data after date filter:", df.head())

        if df.empty:
            st.warning("No data available for the selected dates.")
            return pd.DataFrame()

        # Aggregating the counts of escalation types and EDD measures per reviewer
        agg_data = df.groupby('EDD_reviewer').agg(
            other_red_flags=('escalation_type', lambda x: (x == 'other_red_flags').sum()),
            adverse_media=('escalation_type', lambda x: (x == 'adverse_media').sum()),
            high_risk=('escalation_type', lambda x: (x == 'high_risk').sum()),
            pep_association=('escalation_type', lambda x: (x == 'pep_association').sum()),
            country_risk=('escalation_type', lambda x: (x == 'country_risk').sum()),
            complex_ownership=('escalation_type', lambda x: (x == 'complex_ownership').sum()),
            young_company=('escalation_type', lambda x: (x == 'young_company').sum()),
            medium_risk=('escalation_type', lambda x: (x == 'medium_risk').sum()),
            feedback_review_esc=('escalation_type', lambda x: (x == 'feedback_review').sum()),
            document_review=('EDD_measures', lambda x: (x == 'document_review').sum()),
            aml_review=('EDD_measures', lambda x: (x == 'aml_review').sum()),
            audit_review=('EDD_measures', lambda x: (x == 'audit_review').sum()),
            feedback_review_meas=('EDD_measures', lambda x: (x == 'feedback_review').sum())
        ).reset_index()

        st.write("Aggregated data:", agg_data.head())

        # Calculate totals for each row and column
        agg_data['Total'] = agg_data.iloc[:, 1:].sum(axis=1)
        total_row = pd.DataFrame(agg_data.sum(numeric_only=True)).transpose()
        total_row['EDD_reviewer'] = 'Total'
        agg_data = pd.concat([agg_data, total_row], ignore_index=True)
        st.write("Data with totals:", agg_data.head())

        # Calculate Total Working Hours based on selected dates
        total_working_hours = len(selected_dates) * 8
        agg_data['Total Working Hours'] = total_working_hours

        # Perform necessary transformations
        agg_data['Total SLA period'] = (
            agg_data['other_red_flags'] * weights['other_red_flags'] +
            agg_data['adverse_media'] * weights['adverse_media'] +
            agg_data['high_risk'] * weights['high_risk'] +
            agg_data['pep_association'] * weights['pep_association'] +
            agg_data['country_risk'] * weights['country_risk'] +
            agg_data['complex_ownership'] * weights['complex_ownership'] +
            agg_data['young_company'] * weights['young_company'] +
            agg_data['medium_risk'] * weights['medium_risk'] +
            (agg_data['document_review'] + agg_data['aml_review'] + agg_data['audit_review'] + agg_data['feedback_review_esc'] + agg_data['feedback_review_meas']) * weights['combined_reviews']
        )

        # Calculate the "Difference" column
        agg_data['Difference'] = agg_data['Total Working Hours'] - agg_data['Total SLA period']

        # Close the connection
        conn.close()
        return agg_data

    except mysql.connector.Error as err:
        st.error(f"Error fetching data: {err}")
        return pd.DataFrame()

def show():
    st.title("Weekly Data Report")
    st.subheader("View and download the required data")

    # Custom CSS for horizontal radio buttons and tooltips
    custom_css = """
    <style>
    div[data-baseweb="radio"] > div {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-evenly;
    }
    div[data-baseweb="radio"] > div > div {
        margin-right: 10px;
        margin-bottom: 10px;
    }
    .kpi-card {
        padding: 10px;
        border-radius: 5px;
        color: white;
        text-align: center;
        position: relative;
    }
    .kpi-card h3 {
        margin: 0;
        font-size: 16px;
    }
    .kpi-card h2 {
        margin: 0;
        font-size: 24px;
    }
    .tooltip {
        position: absolute;
        top: -5px;
        right: 105%;
        background-color: black;
        color: #fff;
        text-align: center;
        padding: 5px;
        border-radius: 6px;
        visibility: hidden;
        width: 200px;
        z-index: 1;
        font-size: 12px;
    }
    .kpi-card:hover .tooltip {
        visibility: visible;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # Toggle switch to show/hide date pickers
    show_date_picker = st.checkbox("Select Date Range")

    if show_date_picker:
        # Date selection
        start_date = st.date_input("Select start date", value=datetime.today())
        end_date = st.date_input("Select end date", value=datetime.today())

        # Multiselect for skipping dates
        skipped_dates = st.multiselect("Select dates to skip", pd.date_range(start=start_date, end=end_date).tolist())

        # Calculate working days excluding skipped dates and weekends
        working_days = [date for date in pd.date_range(start=start_date, end=end_date) if date not in skipped_dates and date.weekday() < 5]
        total_working_hours = len(working_days) * 8

        st.write(f"Total Working Hours: {total_working_hours}")
        st.write("Selected working days:", working_days)

        # Fetch transformed data based on selected dates
        filtered_df = fetch_transformed_data(working_days)

        st.write("Filtered DataFrame:", filtered_df.head())

        # KPIs
        with st.container():
            col1, col2, col3 = st.columns(3)

            if not filtered_df.empty and filtered_df['Total'].sum() > 0:
                total_count = filtered_df['Total'].sum()
                highest_reviewer = filtered_df.iloc[:-1].loc[filtered_df.iloc[:-1]['Total'].idxmax(), 'EDD_reviewer']
                lowest_reviewer = filtered_df.iloc[:-1].loc[filtered_df.iloc[:-1]['Total'].idxmin(), 'EDD_reviewer']
            else:
                total_count = 0
                highest_reviewer = "--"
                lowest_reviewer = "--"

            with col1:
                st.markdown(f"""
                <div class="kpi-card" style="background-color: #4CAF50;">
                    <h3>Total Count &#x1F4C8;</h3>  <!-- Bar Chart Icon -->
                    <h2>{total_count}</h2>
                    <small>Change: <span style="color: {'green' if total_count >= 0 else 'red'};">{total_count}</span></small>
                    <div class="tooltip">Total tasks completed in the selected period</div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="kpi-card" style="background-color: #2196F3;">
                    <h3>Highest Reviewer &#x1F4AA;</h3>  <!-- Flexed Biceps Icon -->
                    <h2>{highest_reviewer}</h2>
                    <div class="tooltip">Reviewer with the highest task count</div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="kpi-card" style="background-color: #f44336;">
                    <h3>Lowest Reviewer &#x1F622;</
                    <h3>Lowest Reviewer &#x1F622;</h3>  <!-- Crying Face Icon -->
                    <h2>{lowest_reviewer}</h2>
                    <div class="tooltip">Reviewer with the lowest task count</div>
                </div>
                """, unsafe_allow_html=True)

        # Display the table using Plotly
        st.write("Transformed Data preview:")
        if not filtered_df.empty:
            fig = go.Figure(data=[go.Table(
                header=dict(values=list(filtered_df.columns),
                            fill_color='paleturquoise',
                            align='left'),
                cells=dict(values=[filtered_df[col] for col in filtered_df.columns],
                           fill_color='lavender',
                           align='left'))
            ])
            st.plotly_chart(fig)

            # Download options
            st.subheader("Download Transformed Data")
            download_option = st.selectbox("Select format to download", ["CSV", "Excel"], key="download_option")

            if st.button("Download Transformed Data", key="download_button"):
                st.write("Preparing the download...")
                progress_bar = st.progress(0)

                for percent_complete in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(percent_complete + 1)

                if download_option == "CSV":
                    data = filtered_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download as CSV",
                        data=data,
                        file_name='transformed_data.csv',
                        mime='text/csv',
                    )
                elif download_option == "Excel":
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        filtered_df.to_excel(writer, index=False, sheet_name='Sheet1')
                    processed_data = output.getvalue()
                    st.download_button(
                        label="Download as Excel",
                        data=processed_data,
                        file_name='transformed_data.xlsx',
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    )

        else:
            st.write("No data available for the selected dates.")

        # Line chart using Altair
        with st.expander("Show Line Chart"):
            line_chart = alt.Chart(filtered_df).mark_line().encode(
                x='EDD_reviewer:N',
                y='Total:Q'
            ).properties(
                title="Line Chart"
            )
            st.altair_chart(line_chart, use_container_width=True)

        with st.expander("Show Line Chart"):
            line_chart = alt.Chart(filtered_df).mark_line().encode(
                x='completion_date:T',
                y='Total:Q'
            ).properties(
                title="Line Chart"
            )
            st.altair_chart(line_chart, use_container_width=True)

# Call the show function to render the page
show()

