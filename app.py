import streamlit as st
from streamlit_option_menu import option_menu

# Importing all the scripts
from scripts import input_form, data_download, data_visualization, transformed_data_display, dashboard, report_scheduling


st.set_page_config(
    page_title="Automated Data Pipeline",
    page_icon=":bar_chart:",
    layout="wide",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

custom_css = """
<style>
/* General styling */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #F5F5F5;
    color: #333;
}

/* Styling the sidebar */
.stSidebar {
    background-color: #1E1E1E;
    border-right: 2px solid #E0E0E0;
}

/* Sidebar menu items */
.stSidebar .css-1aumxhk, .stSidebar .css-1vgnldc {
    color: #FFFFFF;
}

.stSidebar .stButton button {
    background-color: #E57373; /* Light red */
    border: none;
    color: white;
    padding: 10px 24px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    transition-duration: 0.4s;
    cursor: pointer;
    border-radius: 5px;
}
.stSidebar .stButton button:hover {
    background-color: #EF9A9A; /* Slightly lighter red */
}

/* Styling main menu */
div[role="radiogroup"] > div {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}
div[role="radiogroup"] > div > label {
    flex: 1;
    border: 1px solid #ddd;
    padding: 10px;
    margin: 0;
    border-radius: 8px;
    background-color: #ffffff;
    text-align: center;
    cursor: pointer;
    transition: background-color 0.3s, box-shadow 0.3s;
}
div[role="radiogroup"] > div > label:hover {
    background-color: #f0f0f0;
}
div[role="radiogroup"] > div > label:focus-within {
    background-color: #e0e0e0;
}
div[role="radiogroup"] > div > label > input {
    display: none;
}
div[role="radiogroup"] > div > label > input:checked + div {
    background-color: #E57373; /* Light red */
    color: white;
    border-color: #E57373;
    box-shadow: 0 4px 8px rgba(229, 115, 115, 0.2);
}

/* Styling buttons */
div.stButton button {
    background-color: #E57373; /* Light red */
    border: none;
    color: white;
    padding: 12px 28px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    transition-duration: 0.4s;
    cursor: pointer;
    border-radius: 5px;
}
div.stButton button:hover {
    background-color: #EF9A9A;
    color: white;
    border: none;
}

/* Styling headers */
h1, h2, h3, h4, h5, h6 {
    color: #333;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin-bottom: 10px;
}

/* Styling text input fields */
div.stTextInput div[data-testid="stTextInputContainer"] {
    border: 2px solid #E57373;
    border-radius: 5px;
    transition: border-color 0.3s, box-shadow 0.3s;
}
div.stTextInput div[data-testid="stTextInputContainer"]:focus-within {
    border-color: #EF9A9A;
    box-shadow: 0 0 8px rgba(229, 115, 115, 0.2);
}
div.stTextInput input {
    padding: 10px;
    border: none;
    border-radius: 5px;
}

/* Styling date input fields */
div.stDateInput div[data-testid="stDateInputContainer"] {
    border: 2px solid #E57373;
    border-radius: 5px;
    transition: border-color 0.3s, box-shadow 0.3s;
}
div.stDateInput div[data-testid="stDateInputContainer"]:focus-within {
    border-color: #EF9A9A;
    box-shadow: 0 0 8px rgba(229, 115, 115, 0.2);
}
div.stDateInput input {
    padding: 10px;
    border: none;
    border-radius: 5px;
}

/* Styling dropdown select boxes */
div.stSelectbox div[data-testid="stSelectboxContainer"] {
    border: 2px solid #E57373;
    border-radius: 5px;
    transition: border-color 0.3s, box-shadow 0.3s;
}
div.stSelectbox div[data-testid="stSelectboxContainer"]:focus-within {
    border-color: #EF9A9A;
    box-shadow: 0 0 8px rgba(229, 115, 115, 0.2);
}
div.stSelectbox select {
    padding: 10px;
    border: none;
    border-radius: 5px;
}

/* Styling tooltips */
.kpi-card:hover .tooltip {
    visibility: visible;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)


# Sidebar configuration
logo_path = r"C:\AI-ML\campus_x\INTERVIEW_PREP\Onboarding\assets\Terrapay-Logo.png"  # Path to the company logo

with st.sidebar:
    st.image(logo_path, use_column_width=True)
    selected = option_menu(
        "Main Menu", ["Input Form", "Download Data", "Data Visualization", "Transformed Data", "Dashboard", "Report Scheduling"],
        icons=['pencil', 'download', 'bar-chart', 'table', 'speedometer', 'calendar'],
        menu_icon="cast", default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#f0f0f0"},  # Light background color
            "icon": {"color": "#8A2BE2", "font-size": "25px"},  # Purple icons
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#ffcccc", "color": "#333"},  # Light red hover color and dark text
            "nav-link-selected": {"background-color": "#ff6666", "color": "white"},  # Light red selected color with white text
        }
    )

# Display the selected page
if selected == "Input Form":
    input_form.show()
elif selected == "Download Data":
    data_download.show()
elif selected == "Data Visualization":
    data_visualization.show()
elif selected == "Transformed Data":
    transformed_data_display.show()
elif selected == "Dashboard":
    dashboard.show()
elif selected == "Report Scheduling":
    report_scheduling.show()

