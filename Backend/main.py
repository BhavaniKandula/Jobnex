# changed main.py

#main.py                                                                                                      
# pyrefly: ignore [missing-import]
from logging import Logger
from fastapi import FastAPI, HTTPException
# pyrefly: ignore [missing-import]
from pydantic import BaseModel,Field,field_validator 
from database import get_connection
from analyzer import analyse_resume
import json
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
import logging
logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5501",
        "*"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class analyseRequest(BaseModel):
    resume_text: str=Field(min_length=50)
    jd_text: str=Field(min_length=50)
    @field_validator("resume_text","jd_text")
    @classmethod
    def not_blank_valid(cls,value):
        if not value.strip():
            raise ValueError("Fill without spaces")
        return value 

import os
from fastapi.responses import FileResponse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
if not os.path.exists(STATIC_DIR):
    alt_dir = os.path.join(BASE_DIR, "..", "public")
    if os.path.exists(alt_dir):
        STATIC_DIR = alt_dir
    else:
        STATIC_DIR = os.path.join(BASE_DIR, "..", "Frontend")

@app.get("/")
def home():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "message": "Resume analyser Backend is Running"
    }

@app.get("/style.css")
def get_style():
    file_path = os.path.join(STATIC_DIR, "style.css")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="text/css")
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/script.js")
def get_script():
    file_path = os.path.join(STATIC_DIR, "script.js")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/javascript")
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/api/health")
def health_check():
    return {
        "message": "Resume analyser Backend is Running",
        "status": "ok"
    }


@app.post("/api/analyse")
def analyse(request: analyseRequest):

    result = analyse_resume(request.resume_text,request.jd_text)
    print(result)
    connection = None
    cursor = None
    analysis_id = None

    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = """
            INSERT INTO resume_analyzer (resume_text, jd_text, matched_skills, missing_skills, matched_score, suggestions)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            query, (
                request.resume_text,
                request.jd_text,
                json.dumps(result["matched_skills"]),
                json.dumps(result["missing_skills"]),
                result["matched_score"],
                json.dumps(result["suggestions"])
            )
        )

        connection.commit()
        analysis_id = cursor.lastrowid

        
        
    except Exception as error:
        if connection is not None and connection.is_connected():
            connection.rollback()
        logger.warning("Could not save to database (running without DB or connection failed): %s", error)
        analysis_id = None

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()
    return {
        "Analysis_Id": analysis_id,
        **result
    }

# Backend API: Retrieve analysis history
@app.get("/api/analyses")
def get_analyses():
    connection = None
    cursor = None

    try:
        # Connect to MySQL
        connection = get_connection()

        # Create a cursor that returns dictionary rows
        cursor = connection.cursor(dictionary=True)

        # Fetch the latest 20 analyses
        query = """SELECT
                id AS Analysis_id,
                matched_score,
                matched_skills,
                missing_skills,
                created_at AS created_At
            FROM resume_analyzer
            ORDER BY id DESC
            LIMIT 3"""

        cursor.execute(query)
        analyses = cursor.fetchall()

        for i in analyses:
            for field in ("matched_skills", "missing_skills"):
                value = i[field]

                if isinstance(value, str):
                    i[field] = json.loads(value)

        return {"analyses": analyses}

    except Exception as error:
        logger.warning("Failed to retrieve analyses from database: %s", error)
        return {"analyses": []}

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()