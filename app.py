import streamlit as st
import os
import pandas as pd
from crew_modules import get_intake_crew, get_data_crew, get_analysis_crew, get_reporting_crew

# Page Config
st.set_page_config(page_title="CrewAI Data Science Team", layout="wide")

# Sidebar
st.sidebar.title("Configuration")
api_key = st.sidebar.text_input("Google API Key", type="password", value=os.getenv("GOOGLE_API_KEY", ""))

if not api_key:
    st.warning("Please enter your Google API Key in the sidebar.")
    st.stop()

# Session State Initialization
if 'project_approved' not in st.session_state:
    st.session_state.project_approved = False
if 'cleaned_data_path' not in st.session_state:
    st.session_state.cleaned_data_path = None
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'project_request' not in st.session_state:
    st.session_state.project_request = ""

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["1. Intake & Scope", "2. Data Engineering", "3. Analysis", "4. Reporting"])

# --- TAB 1: INTAKE ---
with tab1:
    st.header("Project Intake")
    project_request = st.text_area("Describe your data science project request:", 
                                   value="Build a churn model to see why users leave")
    
    if st.button("Submit Request"):
        st.session_state.project_request = project_request
        with st.spinner("Intake Manager & Scrum Master are working..."):
            crew = get_intake_crew(api_key, project_request)
            result = crew.kickoff()
            st.success("Project Processed!")
            st.write(result)
            
            # Check for Jira ticket
            if os.path.exists("jira_ticket.txt"):
                with open("jira_ticket.txt", "r") as f:
                    st.session_state.jira_ticket = f.read()
                st.subheader("Jira Ticket Created")
                st.code(st.session_state.jira_ticket)
            
            # Check for Project Plan
            if os.path.exists("project_plan.md"):
                with open("project_plan.md", "r") as f:
                    st.session_state.project_plan = f.read()
                st.subheader("Project Plan Created")
                st.markdown(st.session_state.project_plan)
                
            st.session_state.project_approved = True

# --- TAB 2: DATA ENGINEERING ---
with tab2:
    st.header("Data Engineering")
    
    if not st.session_state.project_approved:
        st.warning("Please complete the Intake step first.")
    else:
        uploaded_file = st.file_uploader("Upload CSV Data", type=["csv"])
        
        if uploaded_file:
            # Save uploaded file temporarily
            temp_path = "uploaded_data.csv"
            df = pd.read_csv(uploaded_file)
            df.to_csv(temp_path, index=False)
            st.dataframe(df.head())
            
            if st.button("Clean Data"):
                with st.spinner("Data Engineer is cleaning the dataset..."):
                    # In a real app, we'd pass the temp_path to the agent
                    # For this demo, the agent uses its internal tool logic or we guide it
                    # Here we'll just let the agent 'create_data' which mocks cleaning
                    # To make it dynamic, we'd update the tool to read 'uploaded_data.csv'
                    
                    # Pass the project request so the agent knows how to clean the data
                    crew = get_data_crew(api_key, temp_path, st.session_state.project_request) 
                    result = crew.kickoff()
                    
                    st.success("Data Cleaned!")
                    st.write(result)
                    st.session_state.cleaned_data_path = "cleaned_data.csv"
                    
                    if os.path.exists("cleaned_data.csv"):
                        clean_df = pd.read_csv("cleaned_data.csv")
                        st.dataframe(clean_df.head())

# --- TAB 3: ANALYSIS ---
with tab3:
    st.header("Model Training & Analysis")
    
    if not st.session_state.cleaned_data_path:
        st.warning("Please complete the Data Engineering step first.")
    else:
        st.write(f"Using dataset: `{st.session_state.cleaned_data_path}`")
        
        if st.button("Run Analysis"):
            with st.spinner("Senior Data Scientist is training the model..."):
                crew = get_analysis_crew(api_key, st.session_state.cleaned_data_path, st.session_state.project_request)
                result = crew.kickoff()
                
                st.success("Analysis Complete!")
                st.session_state.analysis_result = str(result)
                st.markdown(st.session_state.analysis_result)

# --- TAB 4: REPORTING ---
with tab4:
    st.header("Reporting")
    
    if not st.session_state.analysis_result:
        st.warning("Please complete the Analysis step first.")
    else:
        st.write("Generating presentation based on analysis results...")
        
        if st.button("Generate Presentation"):
            with st.spinner("Presentation Designer is building the deck..."):
                crew = get_reporting_crew(api_key, st.session_state.analysis_result)
                result = crew.kickoff()
                
                st.success("Presentation Ready!")
                st.write(result)
                
                if os.path.exists("churn_presentation.pptx"):
                    with open("churn_presentation.pptx", "rb") as f:
                        st.download_button(
                            label="Download PowerPoint",
                            data=f,
                            file_name="churn_presentation.pptx",
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                        )
