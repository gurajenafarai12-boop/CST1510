import streamlit as st
import pandas as pd
from app.data.db import connect_database
from app.data.tickets import (
    get_all_tickets,
    insert_ticket,
    update_ticket_status,
    delete_ticket
)

# ==================== AUTHENTICATION ====================
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

# ==================== PAGE SETUP ====================
st.title("🖥️ IT Operations")
st.markdown("---")


conn = connect_database('DATA/intelligence_platforms.db')
    
    # ==================== VIEWING TICKETS AND METRICS ====================
tickets = get_all_tickets(conn)
    
    # Convert to DataFrame if it's not empty, otherwise empty DF
if not tickets.empty:
        tickets_df = pd.DataFrame(tickets)
else:
        tickets_df = pd.DataFrame()

    # METRICS ROW
st.subheader("📊 System Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
        st.metric("CPU Usage", "67%", delta="+5%", delta_color="inverse")
with col2:
        st.metric("Memory", "78%", delta="+3%", delta_color="inverse")
with col3:
        st.metric("Disk Space", "245 GB")
with col4:
        st.metric("Uptime", "99.8%", delta="+0.1%")
    
st.markdown("---")
        
    # ==================== TICKET METRICS ====================
st.header("IT Tickets")
    
if not tickets_df.empty:
        # Ticket Metrics
        st.subheader("Ticket Status")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_tickets = len(tickets_df)
            st.metric("Total Tickets", total_tickets)
        with col2:
            open_tickets = len(tickets_df[tickets_df['status'] == 'Open'])
            st.metric("Open", open_tickets)
        with col3:
            high_priority = len(tickets_df[tickets_df['priority'] == 'High'])
            st.metric("High Priority", high_priority)
        with col4:
            resolved = len(tickets_df[tickets_df['status'] == 'Resolved'])
            st.metric("Resolved", resolved)
        
        # Showing tickets table
        st.dataframe(tickets_df, use_container_width=True)
        
        # Simple chart
        if 'status' in tickets_df.columns:
            status_counts = tickets_df['status'].value_counts()
            st.bar_chart(status_counts)
else:
        st.info("No tickets yet. Create your first one below!")
    
st.markdown("---")  
    
    # ==================== CREATING A TICKET ====================
st.header("Create New Ticket")
    
with st.form("ticket_form"):
        title = st.text_input("What's the problem?")
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        description = st.text_area("Description")
        
        if st.form_submit_button("Create Ticket"):
            if title:
                insert_ticket(conn, title, priority, "Open")
                st.success(f"Created ticket: '{title}'")
                st.rerun()
            else:
                st.error("Please enter a title")

st.markdown("---")

    # ==================== UPDATE TICKET ====================
st.header("Update Ticket")
if not tickets_df.empty:
        # Create a list of options for the dropdown
        ticket_options = [f"{row['ticket_id']} - {row['status']} (ID: {row['id']})" for _, row in tickets_df.iterrows()]
        selected_ticket_str = st.selectbox("Select Ticket to Update", ticket_options)
        
        # Extract the database ID from the string "ID: 123)"
        selected_id = int(selected_ticket_str.split("ID: ")[1].replace(")", ""))
        
        with st.form("update_form"):
            new_status = st.selectbox("New Status", ["Open", "In Progress", "Resolved", "Closed"])
            if st.form_submit_button("Update Status"):
                update_ticket_status(conn, selected_id, new_status)
                st.success("Status updated!")
                st.rerun()

    # ==================== SYSTEM STATUS ====================
if not tickets_df.empty:
        st.header("System Status")
    
        # Server status indicators
        st.subheader("🖥️ Server Health")
        
        servers = [
            {"name": "Web Server", "status": "Online", "load": "65%"},
            {"name": "Database", "status": "Online", "load": "42%"},
            {"name": "File Server", "status": "Warning", "load": "88%"},
        ]
        
        for server in servers:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{server['name']}**")
            with col2:
                if server['status'] == "Online":
                    st.success("● Online")
                elif server['status'] == "Warning":
                    st.warning("● Warning")
                else:
                    st.error("● Offline")
            with col3:
                st.write(f"Load: {server['load']}")
        
        # Simple line chart for resource usage
        st.subheader("📈 Resource Usage (Last 24h)")
        
        # Creating sample data
        import numpy as np
        hours = [f"{h}:00" for h in range(24)]
        np.random.seed(42)
        
        usage_data = pd.DataFrame({
            'Hour': hours,
            'CPU %': np.random.randint(40, 85, 24),
            'Memory %': np.random.randint(60, 95, 24)
        }).set_index('Hour')
        
        st.line_chart(usage_data)
       


# ==================== NAVIGATION ====================
st.markdown("---")
if st.button("← Back to Home"):
    st.switch_page("Home.py")