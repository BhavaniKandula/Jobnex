# JobNex - An Algonex Product

JobNex is an intelligent Resume Analyzer web application designed to evaluate candidate resumes against job descriptions (JD), calculating skill match percentages, identifying missing proficiencies, and providing actionable career recommendations.

---

## 🚀 Features

- **Resume & Job Description Analysis**: Compare candidate resume text directly against job requirements.
- **Skill Match Score**: Automated percentage matching score based on required technical skillsets.
- **Skill Gap Insights**: Pinpoint matching skills as well as missing keywords and technologies.
- **Career Suggestions**: Tailored suggestions to help candidates bridge skill gaps.
- **History Tracking**: Stores analysis results in a MySQL database for candidate audit and analytics.

---

## 🛠️ Tech Stack

- **Frontend**: HTML5, Vanilla CSS3, JavaScript (Fetch API)
- **Backend**: FastAPI (Python 3.10+), Pydantic, Uvicorn
- **Database**: MySQL (`jobnex` database, `resume_analyzer` table)

---

## 📂 Project Structure

```text
JobNex/
├── Backend/
│   ├── Algonex/              # Virtual environment (ignored in git)
│   ├── analyzer.py           # Core resume analysis logic
│   ├── database.py           # MySQL database connector
│   ├── insert_test.py        # Database insertion test script
│   ├── main.py               # FastAPI application & REST endpoints
│   ├── requirements.txt      # Python dependencies
│   ├── test_analyzer.py      # Unit test for analysis logic
│   └── test_db.py            # Unit test for database connection
├── Frontend/
│   ├── Index.html            # Main UI interface
│   ├── script.js             # API communication and UI handler
│   └── style.css             # Frontend styling
├── .gitignore                # Git ignore patterns
└── README.md                 # Project documentation
```

---

## ⚡ Getting Started

### 1. Prerequisites
- Python 3.10+ installed
- MySQL Server installed and running

### 2. Database Setup
Create the `jobnex` database and the `resume_analyzer` table in MySQL:

```sql
CREATE DATABASE IF NOT EXISTS jobnex;
USE jobnex;

CREATE TABLE IF NOT EXISTS resume_analyzer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    resume_text TEXT NOT NULL,
    jd_text TEXT NOT NULL,
    matched_skills JSON,
    missing_skills JSON,
    matched_score DECIMAL(5, 2),
    suggestions JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Configure database credentials in `Backend/database.py` if needed:
```python
host = "127.0.0.1"
port = "3306"
user = "root"
password = "YOUR_PASSWORD"
database = "jobnex"
```

### 3. Backend Setup
1. Open a terminal and navigate to `Backend`:
   ```bash
   cd Backend
   ```
2. Create and activate a virtual environment (optional but recommended):
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
4. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
   API will be running at: `http://127.0.0.1:8000`  
   Interactive API docs (Swagger): `http://127.0.0.1:8000/docs`

### 4. Frontend Setup
1. Navigate to `Frontend` directory.
2. Open `Index.html` directly in any web browser or use a live server (e.g., Live Server extension in VS Code on port 5500/5501).

---

## 👥 Contributors & Attribution
Developed as an **Algonex Product**.
