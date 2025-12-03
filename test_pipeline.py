import os
import sys
from dotenv import load_dotenv
from crew_modules import get_intake_crew, get_data_crew, get_analysis_crew, get_reporting_crew

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: GOOGLE_API_KEY not found in .env")
    sys.exit(1)

def run_test():
    print("==================================================")
    print("🧪 STARTING PIPELINE TEST")
    print("==================================================")

    # 1. INTAKE
    print("\n[1/4] Testing Intake Crew...")
    request = "Analyze the churn data to identify why customers are leaving and predict future churn."
    try:
        crew = get_intake_crew(api_key, request)
        crew.kickoff()
        if os.path.exists("jira_ticket.txt") and os.path.exists("project_plan.md"):
            print("✅ Intake Successful: jira_ticket.txt and project_plan.md created.")
        else:
            print("❌ Intake Failed: Missing output files.")
            return
    except Exception as e:
        print(f"❌ Intake Error: {e}")
        return

    # 2. DATA ENGINEERING
    print("\n[2/4] Testing Data Engineering Crew...")
    csv_path = "sample_churn_data.csv"
    if not os.path.exists(csv_path):
        print(f"❌ Error: {csv_path} not found.")
        return
        
    try:
        crew = get_data_crew(api_key, csv_path, request)
        crew.kickoff()
        if os.path.exists("cleaned_data.csv"):
            print("✅ Data Engineering Successful: cleaned_data.csv created.")
        else:
            print("❌ Data Engineering Failed: cleaned_data.csv not created.")
            return
    except Exception as e:
        print(f"❌ Data Engineering Error: {e}")
        return

    # 3. ANALYSIS
    print("\n[3/4] Testing Analysis Crew...")
    analysis_result = ""
    try:
        crew = get_analysis_crew(api_key, "cleaned_data.csv", request)
        result = crew.kickoff()
        analysis_result = str(result)
        print("✅ Analysis Successful.")
        print(f"   Result Snippet: {analysis_result[:100]}...")
    except Exception as e:
        print(f"❌ Analysis Error: {e}")
        return

    # 4. REPORTING
    print("\n[4/4] Testing Reporting Crew...")
    try:
        crew = get_reporting_crew(api_key, analysis_result)
        crew.kickoff()
        if os.path.exists("churn_presentation.pptx"):
            print("✅ Reporting Successful: churn_presentation.pptx created.")
        else:
            print("❌ Reporting Failed: churn_presentation.pptx not created.")
            return
    except Exception as e:
        print(f"❌ Reporting Error: {e}")
        return

    print("\n==================================================")
    print("🎉 PIPELINE TEST COMPLETED SUCCESSFULLY")
    print("==================================================")

if __name__ == "__main__":
    run_test()
