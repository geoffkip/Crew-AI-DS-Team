# CrewAI Data Science Team

This project implements an autonomous Data Science team using [CrewAI](https://crewai.com) and Google's Gemini 2.5 models. The agents collaborate to validate requests, manage tasks, prepare data, train models, and generate reports.

## 🤖 The Team

The crew consists of 5 specialized agents:

1.  **Project Intake Manager**: Validates project requirements and business value.
2.  **Scrum Master**: Manages project flow and creates Jira tickets.
3.  **Data Engineer**: Generates and cleans synthetic datasets.
4.  **Senior Data Scientist**: Trains Random Forest models and analyzes feature importance.
5.  **Presentation Designer**: Creates PowerPoint slides summarizing the findings.

## 🛠️ Prerequisites

-   Python 3.10+
-   [Google AI Studio API Key](https://aistudio.google.com/)

## 🚀 Installation

1.  **Clone the repository** (if applicable) or navigate to the project directory.

2.  **Set up a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuration

1.  Create a `.env` file in the root directory:
    ```bash
    touch .env
    ```

2.  Add your Google API Key:
    ```env
    GOOGLE_API_KEY="your_api_key_here"
    CREWAI_TRACING_ENABLED=true
    ```

## 🏃 Usage

Run the main agent script:

```bash
python team_agent.py
```

## 📂 Output

The crew will generate the following files during execution:
-   `jira_ticket.txt`: Project scope and timeline.
-   `churn_data.csv`: Synthetic dataset used for training.
-   `churn_presentation.pptx`: Final presentation deck.

## 📦 Dependencies

Key libraries used:
-   `crewai`: Agent orchestration.
-   `langchain-google-genai`: Google Gemini integration.
-   `pandas`: Data manipulation.
-   `scikit-learn`: Machine learning models.
-   `python-pptx`: PowerPoint generation.
