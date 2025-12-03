import os
import pandas as pd
from pptx import Presentation
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ==============================================================================
# 1. DEFINE TOOLS (The Skills)
# ==============================================================================

class TeamTools:

    @tool("Save File")
    def save_file(filename: str, content: str):
        """Saves text content to a file. Useful for reports, plans, and tickets."""
        with open(filename, 'w') as f:
            f.write(content)
        return f"File saved: {filename}"

    @tool("Create & Clean Data")
    def create_data(filename: str):
        """Creates a dummy dataset for churn prediction, cleans it, and saves it."""
        # Generating synthetic data
        data = {
            'Age': [25, 30, 45, 35, 50, 23, 60, 48, 33, 29, 22, 55],
            'Annual_Spend': [1200, 3000, 5000, 2500, 6000, 1000, 7000, 5500, 2800, 2900, 800, 6200],
            'Support_Calls': [1, 0, 0, 1, 0, 5, 0, 0, 1, 0, 4, 0],
            'Churn': [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0] # 1 = Churn (Left), 0 = Stayed
        }
        df = pd.DataFrame(data)
        # Mock cleaning: ensure no negative numbers
        df = df[df['Annual_Spend'] > 0] 
        df.to_csv(filename, index=False)
        return f"Clean dataset created at: {filename}"

    @tool("Train Random Forest")
    def train_model(csv_file: str):
        """
        Trains a Random Forest Classifier on the CSV data.
        Target column must be 'Churn'. 
        Returns accuracy score and feature importance.
        """
        try:
            df = pd.read_csv(csv_file)
            X = df.drop('Churn', axis=1)
            y = df['Churn']

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
            
            # Initialize and train Random Forest
            clf = RandomForestClassifier(n_estimators=100, random_state=42)
            clf.fit(X_train, y_train)
            
            # Predict
            preds = clf.predict(X_test)
            acc = accuracy_score(y_test, preds)
            
            # Get Feature Importance
            importances = dict(zip(X.columns, clf.feature_importances_))
            
            return f"Model Trained. Accuracy: {acc:.2f}. Feature Importance: {importances}"
        except Exception as e:
            return f"Error training model: {e}"

    @tool("Generate PowerPoint")
    def create_pptx(title: str, summary: str, findings: str):
        """Creates a .pptx slide deck. Inputs: Title, Summary, Findings."""
        prs = Presentation()

        # Slide 1: Title
        slide = prs.slides.add_slide(prs.slide_layouts[0])
        slide.shapes.title.text = "Project Update: Churn Analysis"
        slide.placeholders[1].text = title

        # Slide 2: Summary
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = "Executive Summary"
        slide.placeholders[1].text = summary

        # Slide 3: Model Findings
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = "Model Insights"
        slide.placeholders[1].text = findings

        prs.save('churn_presentation.pptx')
        return "Presentation saved as 'churn_presentation.pptx'"

# ==============================================================================
# 2. AGENT INITIALIZATION
# ==============================================================================

def init_llms(api_key):
    gemini_pro = LLM(
        model="gemini/gemini-2.5-pro",
        verbose=True,
        temperature=0.7,
        api_key=api_key
    )
    gemini_flash = LLM(
        model="gemini/gemini-2.5-flash",
        verbose=True,
        temperature=0.5,
        api_key=api_key
    )
    return gemini_pro, gemini_flash

def get_intake_crew(api_key, request):
    gemini_pro, gemini_flash = init_llms(api_key)

    intake = Agent(
        role='Project Intake Manager',
        goal='Validate project requirements.',
        backstory="You are a strict director who ensures projects have clear business value.",
        verbose=True,
        llm=gemini_pro
    )

    scrum = Agent(
        role='Scrum Master',
        goal='Manage project flow and Jira tickets.',
        backstory="You keep the team organized. You create ticket files for tracking.",
        tools=[TeamTools.save_file],
        verbose=True,
        llm=gemini_flash
    )

    task_intake = Task(
        description=f"Review request: '{request}'. Approve if valid.",
        expected_output="Approval decision.",
        agent=intake
    )

    task_scrum = Task(
        description="Create a 'jira_ticket.txt' with project scope and timeline.",
        expected_output="Confirmation of file creation.",
        agent=scrum
    )

    return Crew(
        agents=[intake, scrum],
        tasks=[task_intake, task_scrum],
        process=Process.sequential,
        verbose=True
    )

def get_data_crew(api_key, csv_path):
    gemini_pro, _ = init_llms(api_key)

    engineer = Agent(
        role='Data Engineer',
        goal='Prepare clean datasets.',
        backstory="You build robust pipelines. You create the CSV files for the team.",
        tools=[TeamTools.create_data], # Note: In a real app, we'd pass the CSV path to a cleaning tool
        verbose=True,
        llm=gemini_pro
    )

    task_eng = Task(
        description=f"Create/Clean the dataset '{csv_path}'. Ensure columns are correct.",
        expected_output="Confirmation that data is ready.",
        agent=engineer
    )

    return Crew(
        agents=[engineer],
        tasks=[task_eng],
        process=Process.sequential,
        verbose=True
    )

def get_analysis_crew(api_key, csv_path):
    gemini_pro, _ = init_llms(api_key)

    scientist = Agent(
        role='Senior Data Scientist',
        goal='Build predictive models.',
        backstory="You are an expert in Scikit-Learn. You interpret model accuracy and feature importance.",
        tools=[TeamTools.train_model],
        verbose=True,
        llm=gemini_pro
    )

    task_sci = Task(
        description=f"Train a Random Forest on '{csv_path}'. Report the Accuracy and which feature is most important.",
        expected_output="A summary of the model performance and key drivers.",
        agent=scientist
    )

    return Crew(
        agents=[scientist],
        tasks=[task_sci],
        process=Process.sequential,
        verbose=True
    )

def get_reporting_crew(api_key, analysis_result):
    _, gemini_flash = init_llms(api_key)

    slide_maker = Agent(
        role='Presentation Designer',
        goal='Create visual slide decks.',
        backstory="You take technical results and turn them into PowerPoint files.",
        tools=[TeamTools.create_pptx],
        verbose=True,
        llm=gemini_flash
    )

    task_ppt = Task(
        description=f"Create a PowerPoint. Title: 'Q4 Churn Analysis'. Use this summary: {analysis_result}",
        expected_output="Confirmation that .pptx is saved.",
        agent=slide_maker
    )

    return Crew(
        agents=[slide_maker],
        tasks=[task_ppt],
        process=Process.sequential,
        verbose=True
    )
