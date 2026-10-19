# JobNex - An Algonex Product

JobNex is an intelligent Resume Analyzer that evaluates how well a candidate's resume aligns with a given job description, highlighting matched skills, missing skills, match score, and recommendations.

---

## 🚀 Features

- **Resume & Job Description Analysis**: Evaluates resumes against specific job requirements.
- **Skill Matching**: Automatically detects overlapping skills and identifies missing competencies.
- **Match Score**: Calculates a clear percentage match score.
- **Actionable Suggestions**: Provides tailored recommendations for skills to add or learn.
- **Database Logging**: Stores analysis records in MySQL for tracking and history.
- **Interactive UI**: Simple, responsive frontend for instant resume analysis.

---

## 📁 Project Structure

```text
jobnex/
├── backend/
│   ├── main.py              # FastAPI application & API endpoints
│   ├── analyzer.py          # Resume analysis core logic
│   ├── database.py          # MySQL database connection helper
│   ├── requirements.txt     # Python dependencies
│   ├── test_analyzer.py     # Unit tests for analyzer logic
│   └── test_db.py           # Database connectivity tests
├── frontend/
│   ├── index.html           # Main user interface
│   ├── style.css            # Styling and layout
│   └── script.js            # Frontend API client logic
├── .gitignore
└── README.md
```

---

## 🛠️ Getting Started

### 1. Prerequisites
- Python 3.9+
- MySQL Server

### 2. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure your MySQL database settings in `database.py`.
5. Run the FastAPI development server:
   ```bash
   uvicorn main:app --reload
   ```
   The backend API will run at `http://127.0.0.1:8000`.

### 3. Frontend Setup
1. Open `frontend/index.html` in your browser (or use VS Code Live Server at port 5500).
2. Enter your resume and job description to get instant feedback!
