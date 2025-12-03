# 🚀 CrewAI Data Science Team

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![CrewAI](https://img.shields.io/badge/CrewAI-Powered-orange?style=for-the-badge)
![Gemini](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-blueviolet?style=for-the-badge&logo=google)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

> **An autonomous, multi-agent Data Science team powered by CrewAI and Google Gemini.**

This project simulates a full-fledged data science department where AI agents collaborate to validate requests, plan projects, clean data, build predictive models, and generate executive presentations.

---

## 🤖 The Team

Our crew consists of **6 specialized agents**, each with a distinct role and set of skills:

| Agent | Role | Responsibilities |
| :--- | :--- | :--- |
| 🧑‍💼 | **Project Intake Manager** | Validates incoming project requests and ensures business value. |
| 🔄 | **Scrum Master** | Manages project flow, timelines, and creates Jira tickets. |
| 📋 | **Senior Project Manager** | Translates business needs into a detailed technical `project_plan.md`. |
| 🛠️ | **Data Engineer** | Inspects raw CSVs and writes custom Python code to clean and prepare data. |
| 🧠 | **Senior Data Scientist** | Performs statistical analysis and builds predictive models (e.g., Random Forest) using custom code. |
| 🎨 | **Presentation Designer** | Synthesizes findings into a professional PowerPoint deck (`.pptx`). |

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following:

-   **Python 3.10+** installed.
-   A **[Google AI Studio API Key](https://aistudio.google.com/)**.

---

## 🚀 Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/geoffkip/Crew-AI-DS-Team.git
    cd Crew-AI-DS-Team
    ```

2.  **Set Up Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**
    Create a `.env` file in the root directory:
    ```bash
    touch .env
    ```
    Add your API key:
    ```env
    GOOGLE_API_KEY="your_api_key_here"
    CREWAI_TRACING_ENABLED=true
    ```

---

## 🏃 Usage

### Option 1: Interactive Streamlit App (Recommended)
Run the dynamic web interface to interact with the agents:

```bash
streamlit run app.py
```

1.  **Intake Tab**: Submit your project request (e.g., "Predict Churn").
2.  **Data Tab**: Upload your CSV file (or use `sample_churn_data.csv`).
3.  **Analysis Tab**: Watch the Data Scientist build models in real-time.
4.  **Reporting Tab**: Download the final PowerPoint presentation.

### Option 2: CLI Mode (Legacy)
Run the original script for a headless execution:

```bash
python team_agent.py
```

---

## 📂 Project Structure & Outputs

The agents generate tangible artifacts throughout the pipeline:

-   📄 **`jira_ticket.txt`**: Project scope, timeline, and deliverables.
-   📝 **`project_plan.md`**: Detailed technical roadmap.
-   🧹 **`cleaned_data.csv`**: The processed dataset ready for modeling.
-   📊 **`churn_presentation.pptx`**: The final executive summary slide deck.

---

## 📦 Key Technologies

-   **[CrewAI](https://crewai.com)**: Framework for orchestrating role-playing AI agents.
-   **[LangChain](https://langchain.com)**: Building block for LLM applications.
-   **[Google Gemini](https://deepmind.google/technologies/gemini/)**: The intelligence engine (Gemini 2.5 Flash).
-   **[Streamlit](https://streamlit.io)**: The frontend interface.
-   **[Pandas](https://pandas.pydata.org/)** & **[Scikit-Learn](https://scikit-learn.org/)**: Data manipulation and machine learning.

---

<p align="center">
  Made with ❤️ by the CrewAI DS Team
</p>
