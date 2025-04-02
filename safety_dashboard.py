import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Connection to database
conn = sqlite3.connect('transit_safety.db')

# Dashboard title
st.title('Transit Safety Dashboard')

# Sidebar filters
st.sidebar.header('Filters')
year_options = pd.read_sql("SELECT DISTINCT Year FROM transit_safety ORDER BY Year DESC", conn)['Year']
years = st.sidebar.multiselect(
    'Select Years',
    options=year_options,
    default=None  
)

# Accident trend
trend_where = f"WHERE Year IN ({','.join(map(str, years))})" if years else ""
trend_query = f"""
    SELECT Year, COUNT(*) as accidents 
    FROM transit_safety 
    {trend_where}
    GROUP BY Year 
    ORDER BY Year
"""
trend_df = pd.read_sql(trend_query, conn)
st.plotly_chart(px.line(trend_df, x='Year', y='accidents', title='Accident Trend'))

# Injury severity
if years:
    placeholders = ','.join(['?'] * len(years))
    severity_query = f"""
        SELECT 
            SUM("Total Injuries") as injuries,
            SUM("Total Serious Injuries") as serious_injuries
        FROM transit_safety
        WHERE Year IN ({placeholders})
    """
    severity_df = pd.read_sql(severity_query, conn, params=years)
else:
    severity_query = """
        SELECT 
            SUM("Total Injuries") as injuries,
            SUM("Total Serious Injuries") as serious_injuries
        FROM transit_safety
    """
    severity_df = pd.read_sql(severity_query, conn)

st.plotly_chart(px.bar(severity_df.melt(), x='variable', y='value', 
                title='Injury Severity Breakdown',
                labels={'variable': 'Injury Type', 'value': 'Count'}))

# Close connection
conn.close()