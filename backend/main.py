import json
import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

from database import get_connection
from analyzer import analyze_resume
from resume_privacy import router as resume_router, redact_text
from filter_logic import router as filter_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# app MUNDU create cheyyali, taruvata router include cheyyali
app = FastAPI()
app.include_router(resume_router)
app.include_router(filter_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    resume_text: str = Field(min_length=50)
    jd_text: str = Field(min_length=50)

    @field_validator("resume_text", "jd_text")
    @classmethod
    def not_blank_validate(cls, value):
        if not value.strip():
            raise ValueError("fill without spaces")
        return value


@app.get("/")
def home():
    return {"message": "Resume Analyzer Backend is Running"}


@app.post("/api/analyze")
def analyze(request: AnalyzeRequest):
    # Analysis original text tho chestam, kani DB lo save cheyyadaniki mundu
    # email/phone/links hide chestam
    result = analyze_resume(request.resume_text, request.jd_text)
    safe_resume_text = redact_text(request.resume_text)

    connection = None
    cursor = None
    analysis_id = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO resume_analyzer
                (resume_text, jd_text, matched_skills, missing_skills, matched_score, suggestions)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                safe_resume_text,
                request.jd_text,
                json.dumps(result["matched_skills"]),
                json.dumps(result["missing_skills"]),
                result["matched_score"],
                json.dumps(result["suggestions"]),
            ),
        )

        connection.commit()
        analysis_id = cursor.lastrowid

    except Exception as error:
        if connection is not None and connection.is_connected():
            connection.rollback()
        logger.exception("failed to save resume analysis")

        raise HTTPException(
            status_code=500,
            detail="Failed to save analysis",
        ) from error

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

    return {
        "Analysis_Id": analysis_id,
        **result,
    }


# Backend API: Retrieve analysis history
@app.get("/api/analyses")
def get_analyses():
    connection = None
    cursor = None

    try:
        connection = get_connection()

        # Dictionary rows return chese cursor
        cursor = connection.cursor(dictionary=True)

        # Latest 20 analyses
        query = """
            SELECT
                Analysis_id,
                matched_score,
                matched_skills,
                missing_skills,
                created_At
            FROM resume_analyzer
            ORDER BY Analysis_id DESC
            LIMIT 20
        """

        cursor.execute(query)
        analyses = cursor.fetchall()

        for row in analyses:
            for field in ("matched_skills", "missing_skills"):
                value = row[field]

                if isinstance(value, str):
                    row[field] = json.loads(value)

        return {"analyses": analyses}

    except Exception as error:
        logger.exception("failed to retrieve analyses")

        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve analyses",
        ) from error

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()