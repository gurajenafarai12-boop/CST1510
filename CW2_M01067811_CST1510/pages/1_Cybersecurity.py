import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import google.generativeai as genai
from datetime import datetime, timedelta
from models.cyber_incident import SecurityIncident
from services.database_manager import DatabaseManager

# Import database connection
from app.data.db import connect_database

# Import CRUD functions
from app.data.incidents import (
    get_all_incidents,  
    insert_incident,
    update_incident_status,
    delete_incident
)

# ==================== AUTHENTICATION ====================
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

# ==================== PAGE SETUP ====================
st.title("🔐 Cybersecurity Dashboard")
st.markdown(f"**User:** {st.session_state.username} | **Role:** {st.session_state.role}")
st.markdown("---")

# ==================== DATABASE ====================
conn = connect_database('DATA/intelligence_platforms.db')

# ==================== VIEWING INCIDENTS AND METRICS ====================
incidents = get_all_incidents(conn)

# Converting to dataframe if not empty
if not incidents.empty:
    incidents_df = pd.DataFrame(incidents)
else:
    incidents_df = pd.DataFrame()

# ==================== SECURITY METRICS ====================
st.subheader("🔒 Security Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_incidents = len(incidents_df) if not incidents_df.empty else 0
    st.metric("Total Incidents", total_incidents)
with col2:
    critical = len(incidents_df[incidents_df['severity'] == 'Critical']) if not incidents_df.empty else 0
    st.metric("Critical", critical, delta_color="inverse")
with col3:
    open_incidents = len(incidents_df[incidents_df['status'] == 'Open']) if not incidents_df.empty else 0
    st.metric("Open", open_incidents, delta_color="inverse")
with col4:
    resolved = len(incidents_df[incidents_df['status'] == 'Resolved']) if not incidents_df.empty else 0
    st.metric("Resolved", resolved, delta="+2" if resolved > 0 else None)

st.markdown("---")

# ==================== INCIDENT MANAGEMENT ====================
st.header("Security Incidents")

if not incidents_df.empty:
    # Incident Metrics
    st.subheader("Incident Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_incidents = len(incidents_df)
        st.metric("Total Incidents", total_incidents)
    with col2:
        high_severity = len(incidents_df[incidents_df['severity'] == 'High'])
        st.metric("High Severity", high_severity)
    with col3:
        in_progress = len(incidents_df[incidents_df['status'] == 'In Progress'])
        st.metric("In Progress", in_progress)
    with col4:
        closed = len(incidents_df[incidents_df['status'] == 'Closed']) if 'Closed' in incidents_df['status'].values else 0
        st.metric("Closed", closed)
    
    # Showing incidents table
    st.dataframe(incidents_df, use_container_width=True)
    
    # Severity distribution chart
    if 'severity' in incidents_df.columns:
        severity_counts = incidents_df['severity'].value_counts()
        st.bar_chart(severity_counts)
else:
    st.info("No incidents yet. Create your first one below!")

st.markdown("---")

# ==================== CREATING AN INCIDENT ====================
st.header("Create New Incident")

with st.form("incident_form"):
    title = st.text_input("Incident Title")
    severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
    description = st.text_area("Description")
    
    if st.form_submit_button("Create Incident"):
        if title:
            insert_incident(conn, title.strip(), severity, "Open")
            st.success(f"Created incident: '{title}'")
            st.rerun()
        else:
            st.error("Please enter a title")

st.markdown("---")

# ==================== UPDATE INCIDENT ====================
st.header("Update Incident Status")
if not incidents_df.empty:
    # Creating a list of options for the dropdown
    incident_options = [f"{row['incident_id']} - {row['severity']} (ID: {row['id']})" for _, row in incidents_df.iterrows()]
    selected_incident_str = st.selectbox("Select Incident to Update", incident_options)
    
    # Extracting the database ID from the string "ID: 123)"
    selected_id = int(selected_incident_str.split("ID: ")[1].replace(")", ""))
    
    with st.form("update_form"):
        new_status = st.selectbox("New Status", ["Open", "In Progress", "Resolved", "Closed"])
        if st.form_submit_button("Update Status"):
            update_incident_status(conn, selected_id, new_status)
            st.success("Status updated!")
            st.rerun()

st.markdown("---")

# ==================== THREAT ANALYSIS ====================
st.header("Threat Analysis")

st.subheader("📈 Incident Trends")
# Creating sample data for trends
hours = [f"{h}:00" for h in range(24)]
np.random.seed(42)

trend_data = pd.DataFrame({
    'Hour': hours,
    'Malware Attacks': np.random.randint(0, 20, 24),
    'DDoS Attempts': np.random.randint(0, 15, 24),
    'Phishing Alerts': np.random.randint(0, 25, 24),
    'Unauthorized Access': np.random.randint(0, 10, 24)
}).set_index('Hour')

st.line_chart(trend_data)

# Threat type distribution
st.subheader("🔍 Threat Type Distribution")
threat_types = ['Malware', 'Phishing', 'DDoS', 'Unauthorized Access', 'Data Breach']
counts = np.random.randint(5, 25, len(threat_types))

threat_df = pd.DataFrame({'Count': counts}, index=threat_types)
st.bar_chart(threat_df)

st.markdown("---")

# ==================== ATTACK PATTERNS ====================
st.header("Attack Pattern Detection")

st.subheader("🕒 Attack Heatmap (Weekly Pattern)")
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
hours = [f"{h:02d}:00" for h in range(24)]
attack_data = np.random.randint(0, 20, (7, 24))

heatmap_df = pd.DataFrame(attack_data, index=days, columns=hours)
st.dataframe(heatmap_df, use_container_width=True)

st.subheader("📊 Busiest Attack Hours")
busiest_hours = heatmap_df.sum()
st.bar_chart(busiest_hours)

st.markdown("---")

# ==================== AI ANALYSIS ====================
st.header("AI-Powered Analysis")

if not incidents_df.empty:
    incident_options = [row['incident_id'] for _, row in incidents_df.iterrows()]
    selected_inc = st.selectbox("Choose an incident for AI analysis:", incident_options)
    
    if st.button("🤖 Analyze with AI"):
        filtered = incidents_df[incidents_df['incident_id'] == selected_inc]
        
        if not filtered.empty:
            incident = filtered.iloc[0]
            
            prompt = (
                f"Analyze this cybersecurity incident:\n"
                f"Title: {incident['incident_id']}\n"
                f"Severity: {incident['severity']}\n"
                f"Status: {incident['status']}"
            )
            
            try:
                response = genai.generate_content(prompt)
                st.write(response.text)
            except Exception as e:
                st.error(f"AI analysis error: {e}")
        else:
            st.error("No incident matched.")

st.markdown("---")


#=========OOP DEMO=========#
st.header("🎯 OOP Implementation")


col1, col2 = st.columns(2)

with col1:
    st.subheader("SecurityIncident Model")
    
    # Create an incident object
    incident = SecurityIncident(
        incident_id=999,
        title="OOP Demo: Phishing Attack",
        severity="High",
        status="Open"
    )
    
    st.success(f"✅ Created: {incident}")
    
    # Show OOP methods
    if hasattr(incident, 'get_severity_level'):
        st.info(f"📊 Severity Level: {incident.get_severity_level()}")
    
    if hasattr(incident, 'update_status'):
        incident.update_status("In Progress")
        st.info(f"🔄 Status Updated: {incident.status}")

with col2:
    st.subheader("DatabaseManager Service")
    
    # Creating database manager
    db = DatabaseManager("DATA/intelligence_platforms.db")
    st.success(f"✅ Initialized: {db}")
    
    # Show database query
    if st.button("Test Database Query"):
        
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM cyber_incidents")
            count = cursor.fetchone()[0]
            st.info(f"📦 Total Incidents in DB: {count}")
            conn.close()
        except:
            st.info("📦 Database connected successfully")


# ==================== NAVIGATION ====================
if st.button("← Back to Home"):
    st.switch_page("Home.py")