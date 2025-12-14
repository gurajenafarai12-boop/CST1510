import streamlit as st
import pandas as pd
from app.data.db import connect_database
from app.data.datasets import (
    get_all_datasets,
    insert_dataset,
    update_dataset,
    delete_dataset
)

# ==================== AUTHENTICATION ====================
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

# ==================== PAGE SETUP ====================
st.title("📊 Data Science ")
st.markdown("Manage datasets, view metrics, and perform data operations.")
conn = connect_database('DATA/intelligence_platforms.db')
    
    # ==================== TAB 1: VIEW DATA and METRICS====================
st.header("Data Science Datasets")
    
    # Get and display data
datasets = get_all_datasets(conn)
    
if not datasets.empty:
        # Show as table
        datasets_df = pd.DataFrame(datasets)
        st.dataframe(datasets_df)
     
        # Simple statistics
        st.subheader("Quick Statistics")
        col1, col2,col3,col4 = st.columns(4)
        with col1:
            total=len(datasets_df)
            st.metric("Total Datasets", total)
            
        with col2:
            if 'size' in datasets_df.columns:
                total_size = datasets_df['size'].sum()
                st.metric("Total Size", f"{total_size:.0f} MB")
        with col3:
            if 'category' in datasets_df.columns:
                unique_types = datasets_df['category'].nunique()
                st.metric("Unique Types", unique_types)
            else:
                st.metric("Unique Types", "N/A")
        with col4:
            if 'size' in datasets_df.columns:
                total_size = datasets_df['size'].sum()
                st.metric("Total Storage", f"{total_size:.1f} MB")
            else:
                st.metric("Total Storage", "N/A")
    
    
st.header("All Datasets")

if not datasets.empty:
        # Showing as table
        datasets_df = pd.DataFrame(datasets)
        st.dataframe(datasets_df)
        
        # Simple chart
        st.subheader("Dataset Categories")
        if 'category' in datasets_df.columns:
            category_counts = datasets_df['category'].value_counts()
            st.bar_chart(category_counts)
else:
        st.info("No datasets yet. Add your first one below!")
    
st.markdown("---")

    
    # ==================== TAB 2: ADDING DATA ====================
st.header("Add New Dataset")
    
with st.form("add_form"):
        name = st.text_input("Dataset Name")
        source = st.text_input("Source (e.g., Kaggle)")
        category = st.selectbox("Type", ["Tabular", "Image", "Text", "Other"])
        size = st.number_input("Size (MB)", min_value=0.1, value=10.0)
        
        if st.form_submit_button("Add Dataset"):
            if name and source:
                insert_dataset(conn, name, source, category, size)
                st.success(f"Added '{name}' to database!")
                st.rerun()
            else:
                st.error("Please fill in name and source")
    
st.markdown("---")
    
    # ==================== TAB 3: UPDATE/DELETE ====================
if not datasets.empty:
        st.header("Manage Datasets")
        
        # UPDATE SECTION
        st.subheader("Update Dataset")
        datasets_df = pd.DataFrame(datasets)
        dataset_names = [f"{row['name']} (ID: {row['id']})" for _, row in datasets_df.iterrows()]
        
        selected = st.selectbox("Choose dataset to update", dataset_names)
        
        if selected:
            # Finding the selected dataset
            dataset_id = int(selected.split("ID: ")[1].strip(")"))
            dataset_data = datasets_df[datasets_df['id'] == dataset_id].iloc[0]
            
            with st.form("update_form"):
                new_status = st.selectbox("Status", ["Active", "Archived", "Processing"])
                new_note = st.text_input("Add a note", value="")
                
                if st.form_submit_button("Update"):
                    st.success(f"Updated dataset {dataset_data['name']}!")
                    update_dataset(conn, dataset_id, new_status, new_note)
                    st.rerun()
        
        # DELETE SECTION
        st.subheader("Delete Dataset")
        st.warning("Be careful this cannot be undone!")
        
        delete_option = st.selectbox("Choose dataset to delete", dataset_names, key="delete")
        
        if st.button("Delete Selected", type="primary"):
            delete_id = int(delete_option.split("ID: ")[1].strip(")"))
            delete_dataset(conn, delete_id)
            st.success("Dataset deleted!")
            st.rerun()
    
    # ==================== SIMPLE DISPLAY CHART ====================
if not datasets.empty:  
        st.markdown("---")
        st.header("Simple Chart View")
        
        if 'category' in datasets_df.columns:
            # Counting datasets by category
            category_counts = datasets_df['category'].value_counts()
            
            # Showing as bar chart
            st.bar_chart(category_counts)
            st.caption("Number of datasets by type")
            
        # Showing as simple table
        expected = ['name', 'category', 'size']
        available = [col for col in expected if col in datasets_df.columns]

        summary_df = datasets_df[available].head(5)
        
        st.table(summary_df)




# ==================== NAVIGATION ====================
st.markdown("---")
if st.button("← Back to Home"):
    st.switch_page("Home.py")