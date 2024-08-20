import streamlit as st
import pandas as pd
import mysql.connector
from io import BytesIO
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, GridUpdateMode, DataReturnMode
import plotly.express as px
import time
import altair as alt

# Replace these with your actual MySQL server details
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_DATABASE = "TERRAPAY"

def fetch_data():
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        query = "SELECT * FROM Hityshi"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except mysql.connector.Error as err:
        st.error(f"Error fetching data: {err}")
        return pd.DataFrame()

def to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data

def show():
    st.title("Download Data")
    st.subheader("Download the data from the database")

    df = fetch_data()

    if not df.empty:
        st.write("Data preview:")
        
        # AgGrid display with advanced features
        gb = GridOptionsBuilder.from_dataframe(df)
        
        # Enable pagination
        gb.configure_pagination(paginationAutoPageSize=True)
        
        # Enable sidebar with filters
        gb.configure_side_bar()
        
        # Enable column grouping and aggregation
        gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
        
        # Add a custom tooltip to a column
        gb.configure_column("EDD_reviewer", headerTooltip="This is the reviewer's name")
        
        # Add conditional formatting dynamically
        unique_deal_types = df['EDD_reviewer'].unique()
        
        cellsytle_jscode = JsCode(f"""
            function(params) {{
                if (params.value == '{unique_deal_types[0]}') {{
                    return {{
                        'color': 'black',
                        'backgroundColor': '#FFD700'  // Light Gold
                    }}
                }} else if (params.value == '{unique_deal_types[1]}') {{
                    return {{
                        'color': 'black',
                        'backgroundColor': '#98FB98'  // Pale Green
                    }}
                }} else if (params.value == '{unique_deal_types[2]}') {{
                    return {{
                        'color': 'black',
                        'backgroundColor': '#ADD8E6'  // Light Blue
                    }}
                }} else if (params.value == '{unique_deal_types[3]}') {{
                    return {{
                        'color': 'black',
                        'backgroundColor': '#FFC0CB'  // Light Pink
                    }}
                }} else if (params.value == '{unique_deal_types[4]}') {{
                    return {{
                        'color': 'black',
                        'backgroundColor': '#D3D3D3'  // Light Grey
                    }}
                }} else if (params.value == '{unique_deal_types[5]}') {{
                    return {{
                        'color': 'black',
                        'backgroundColor': '#E6E6FA'  // Lavender
                    }}
                }} else {{
                    return {{
                        'color': 'black',
                        'backgroundColor': '#FFFACD'  // Lemon Chiffon
                    }}
                }}
            }};
        """)

        gb.configure_column("EDD_reviewer", cellStyle=cellsytle_jscode)

        # Add row selection
        gb.configure_selection('multiple', use_checkbox=True)

        # Add charts
        gb.configure_grid_options(domLayout='autoHeight')
        gb.configure_grid_options(enableCharts=True)

        # Enable inline editing
        gb.configure_column("EDD_reviewer", editable=True)

        # Enable column visibility toggle
        gb.configure_column("completion_date", hide=True)

        # Enable drag and drop
        gb.configure_grid_options(rowDragManaged=True)
        
        # Enable scrollbars for sidebar and table
        gb.configure_grid_options(suppressHorizontalScroll=False)
        gb.configure_grid_options(suppressVerticalScroll=False)
        
        # Enable server-side data source
        gb.configure_grid_options(serverSideStoreType='full')
        
        gridOptions = gb.build()

        grid_response = AgGrid(
            df, 
            gridOptions=gridOptions, 
            enable_enterprise_modules=True, 
            height=500, 
            fit_columns_on_grid_load=True, 
            theme="alpine", 
            allow_unsafe_jscode=True,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            data_return_mode=DataReturnMode.FILTERED_AND_SORTED
        )

        selected_rows = grid_response['selected_rows']
        st.write("Selected Rows:", selected_rows)

        # Editable feature on selection
        if st.button("Enable Editing for Selected Rows"):
            if selected_rows:
                editable_columns = list(selected_rows[0].keys())  # Get the keys (columns) from the first selected row
                for col in editable_columns:
                    gb.configure_column(col, editable=True)
                gridOptions = gb.build()
                grid_response = AgGrid(
                    df, 
                    gridOptions=gridOptions, 
                    enable_enterprise_modules=True, 
                    height=500, 
                    fit_columns_on_grid_load=True, 
                    theme="alpine", 
                    allow_unsafe_jscode=True,
                    update_mode=GridUpdateMode.SELECTION_CHANGED,
                    data_return_mode=DataReturnMode.FILTERED_AND_SORTED
                )
                st.write("Editing Enabled for Selected Columns")
            else:
                st.warning("No rows selected. Please select rows to enable editing.")

        # CSS for styling
        custom_css = """
        <style>
        /* Styling the sidebar */
        div[data-testid="stSidebar"] {
            background-color: #2E2E2E;
        }
        div[data-testid="stSidebar"] .css-1d391kg {
            color: white;
        }
        div[data-testid="stSidebar"] .css-1aumxhk {
            color: white;
        }
        </style>
        """
        st.markdown(custom_css, unsafe_allow_html=True)

        # Display aggregated values
        agg_sel = st.toggle("Aggregated Data")
        if agg_sel:
            agg_data = df.groupby('EDD_reviewer').agg({'edd_escalation_tasks': 'count'}).reset_index()
            st.write(agg_data)

        # Main data download option
        st.error("Download Main Data")
        download_option = st.selectbox("Select format to download", ["CSV", "Excel"], key="main_download_option")

        if st.button("Download Main Data"):
            st.write("Preparing the download...")
            progress_bar = st.progress(0)

            for percent_complete in range(100):
                time.sleep(0.01)
                progress_bar.progress(percent_complete + 1)

            if download_option == "CSV":
                data = to_csv(df)
                st.download_button(
                    label="Download as CSV",
                    data=data,
                    file_name='data.csv',
                    mime='text/csv',
                )
            elif download_option == "Excel":
                data = to_excel(df)
                st.download_button(
                    label="Download as Excel",
                    data=data,
                    file_name='data.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                )
        
        # Aggregated data and visualizations
        st.subheader("Aggregated Data and Visualizations")

        # Aggregated data by EDD Reviewer with Year Tabs
        with st.expander("EDD Reviewer"):
            st.write("Select a year to view the EDD reviewer trends:")

            # Extract unique years
            df['completion_year'] = pd.to_datetime(df['completion_date']).dt.year
            years = sorted(df['completion_year'].unique())

            year_tabs_reviewer = st.tabs([str(year) for year in years])

            for year in years:
                with year_tabs_reviewer[years.index(year)]:
                    st.write(f"EDD Reviewer Performance for {year}")
                    df_year_reviewer = df[df['completion_year'] == year]
                    agg_df_reviewer = df_year_reviewer.groupby('EDD_reviewer').agg({'edd_escalation_tasks': 'count'}).reset_index()
                    AgGrid(agg_df_reviewer, fit_columns_on_grid_load=True, theme="alpine")
                    fig_reviewer = px.bar(agg_df_reviewer, x='EDD_reviewer', y='edd_escalation_tasks', title=f"Count of EDD/Escalation Tasks by Reviewer for {year}")
                    st.plotly_chart(fig_reviewer)
                    csv_agg_df_reviewer = to_csv(agg_df_reviewer)
                    st.download_button(label=f"Download Data for {year} as CSV", data=csv_agg_df_reviewer, file_name=f"agg_data_reviewer_{year}.csv", mime="text/csv")

        # Aggregated data by Month with Year Tabs
        with st.expander("Monthly Performance"):
            st.write("Select a year to view the monthly performance trends:")

            year_tabs = st.tabs([str(year) for year in years])

            for year in years:
                with year_tabs[years.index(year)]:
                    st.write(f"Monthly Performance for {year}")
                    df_year = df[df['completion_year'] == year]
                    df_year['completion_month'] = pd.to_datetime(df_year['completion_date']).dt.to_period('M').astype(str)
                    agg_df_monthly = df_year.groupby('completion_month').agg({'edd_escalation_tasks': 'count'}).reset_index()
                    AgGrid(agg_df_monthly, fit_columns_on_grid_load=True, theme="alpine")
                    fig_monthly = px.line(agg_df_monthly, x='completion_month', y='edd_escalation_tasks', title=f"Monthly Count of EDD/Escalation Tasks for {year}")
                    st.plotly_chart(fig_monthly)
                    csv_agg_df_monthly = to_csv(agg_df_monthly)
                    st.download_button(label=f"Download Monthly Data for {year} as CSV", data=csv_agg_df_monthly, file_name=f"agg_data_monthly_{year}.csv", mime="text/csv")

    else:
        st.write("No data available to download.")

if __name__=="__main__":
    show()