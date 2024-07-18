import streamlit as st 
import pandas as pd
import plotly.express as px 
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import mysql.connector
'''
# Page configuration
st.set_page_config(
    
    page_title="Compliance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sample data
data = {
    "partner_name": ["Partner A", "Partner B", "Partner C", "Partner D"],
    "deal_type": ["imt", "payments", "issuance", "vendor"],
    "completion_date": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04"],
    "review_type": ["fresh_onboarding", "periodic_review", "fresh_onboarding", "periodic_review"],
    "escalation_type": ["other_red_flags", "adverse_media", "high_risk", "pep_association"],
    "EDD_reviewer": ["neelima_routhu", "francis_xavier", "rohan_vazapully", "rahil_fw"],
    "EDD_measures": ["document_review", "aml_review", "audit_review", "feedback_review"],
    "timestamp": ["2023-01-01 10:00:00", "2023-01-02 11:00:00", "2023-01-03 12:00:00", "2023-01-04 13:00:00"]
}

df = pd.DataFrame(data)

# Sidebar
with st.sidebar:
    st.title('📊 Compliance Dashboard')
    
    deal_types = df['deal_type'].unique().tolist()
    selected_deal_type = st.selectbox('Select Deal Type', deal_types)
    
    reviewers = df['EDD_reviewer'].unique().tolist()
    selected_reviewer = st.selectbox('Select Reviewer', reviewers)
    
    escalation_types = df['escalation_type'].unique().tolist()
    selected_escalation_type = st.selectbox('Select Escalation Type', escalation_types)
    
    edd_measures = df['EDD_measures'].unique().tolist()
    selected_edd_measures = st.selectbox('Select EDD Measures', edd_measures)
    
    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a Color Theme', color_theme_list)

# Filter data based on sidebar selections
df_filtered = df[
    (df['deal_type'] == selected_deal_type) & 
    (df['EDD_reviewer'] == selected_reviewer) & 
    (df['escalation_type'] == selected_escalation_type) & 
    (df['EDD_measures'] == selected_edd_measures)
]

# Define function for a bar chart
def make_bar_chart(df):
    chart = alt.Chart(df).mark_bar().encode(
        x='deal_type',
        y='count(partner_name)',
        color=alt.Color('deal_type', scale=alt.Scale(scheme=selected_color_theme))
    ).properties(
        width=400,
        height=300
    )
    return chart

# Define function for a line chart
def make_line_chart(df):
    chart = alt.Chart(df).mark_line().encode(
        x='completion_date',
        y='count(partner_name)',
        color=alt.Color('deal_type', scale=alt.Scale(scheme=selected_color_theme))
    ).properties(
        width=400,
        height=300
    )
    return chart

# Define function for a pie chart
def make_pie_chart(df):
    chart = px.pie(df, names='escalation_type', title='Distribution of Escalation Types', color_discrete_sequence=px.colors.sequential.Blues)
    return chart

# Define function for a scatter plot
def make_scatter_plot(df):
    chart = px.scatter(df, x='partner_name', y='EDD_measures', title='EDD Measures vs Partner Names', color='deal_type', color_continuous_scale=selected_color_theme)
    return chart

# Main Panel
st.title("Compliance Dashboard")
st.subheader("Interactive Visualizations")

# Create containers for each chart
with st.container():
    st.write("Bar Chart")
    st.altair_chart(make_bar_chart(df_filtered), use_container_width=True)
    
with st.container():
    st.write("Line Chart")
    st.altair_chart(make_line_chart(df_filtered), use_container_width=True)
    
with st.container():
    st.write("Pie Chart")
    st.plotly_chart(make_pie_chart(df_filtered))
    
with st.container():
    st.write("Scatter Plot")
    st.plotly_chart(make_scatter_plot(df_filtered))
'''