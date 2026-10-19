"""
JobNext - Central Dashboard for Applied Jobs / Status Updates (backend feature)

Stack : FastAPI + MySQL (mysql-connector-python)
Setup : uv add fastapi uvicorn mysql-connector-python
        (optional) uv add python-dotenv   -> to read settings from a .env file

DB settings are read from environment variables (or .env):
    MYSQL_HOST=localhost
    MYSQL_PORT=3306
    MYSQL_USER=root
    MYSQL_PASSWORD=your_password
    MYSQL_DATABASE=jobnext

Usage : app.include_router(create_router())
        -> on startup the database + 2 tables are created automatically
           (applications, status_history) and you can see them in MySQL Workbench.

Endpoints (all need header  X-User-Id):
    POST   /dashboard/applications                    -> add an applied job
    GET    /dashboard/applications                    -> list (filter + pagination)
    GET    /dashboard/applications/{id}               -> single application
    PATCH  /dashboard/applications/{id}/status        -> update status
    GET    /dashboard/applications/{id}/history       -> status timeline
    GET    /dashboard/summary                         -> counts per status + response rate
"""
from __future__ import annotations

import os
import re
from contextlib import contextmanager
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

import mysql.connector
from fastapi import APIRouter, Header, HTTPException, Query
from pydantic import BaseModel, Field

try:  # optional: load .env file if python-dotenv is installed
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


# --------------------------------------------------------------------------
# DB configuration
# --------------------------------------------------------------------------
def get_db_config(database: Optional[str] = None) -> dict:
    """Build the MySQL connection settings from environment variables."""
    return {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
        "database": database or os.getenv("MYSQL_DATABASE", "jobnext"),
    }


# --------------------------------------------------------------------------
# Status model
# --------------------------------------------------------------------------
class ApplicationStatus(str, Enum):
    APPLIED = "APPLIED"
    UNDER_REVIEW = "UNDER_REVIEW"
    SHORTLISTED = "SHORTLISTED"
    INTERVIEW_SCHEDULED = "INTERVIEW_SCHEDULED"
    OFFER = "OFFER"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"
    FAILED = "FAILED"  # auto-apply bot could not submit


S = ApplicationStatus

# Which status can move to which status
ALLOWED_TRANSITIONS: dict[ApplicationStatus, set[ApplicationStatus]] = {
    S.FAILED: {S.APPLIED, S.WITHDRAWN},  # retry succeeded -> APPLIED
    S.APPLIED: {S.UNDER_REVIEW, S.SHORTLISTED, S.REJECTED, S.WITHDRAWN},
    S.UNDER_REVIEW: {S.SHORTLISTED, S.REJECTED, S.WITHDRAWN},
    S.SHORTLISTED: {S.INTERVIEW_SCHEDULED, S.REJECTED, S.WITHDRAWN},
    S.INTERVIEW_SCHEDULED: {S.OFFER, S.REJECTED, S.WITHDRAWN},
    S.OFFER: {S.WITHDRAWN},
    S.REJECTED: set(),   # final
    S.WITHDRAWN: set(),  # final
}

# Statuses that mean "company has not responded yet / nothing happened"
NO_RESPONSE_STATUSES = {S.APPLIED, S.FAILED}


# --------------------------------------------------------------------------
# Request / response schemas
# --------------------------------------------------------------------------
class ApplicationCreate(BaseModel):
    job_title: str = Field(min_length=1, max_length=200)
    company: str = Field(min_length=1, max_length=200)
    job_url: str = Field(min_length=1, max_length=500)
    source: str = Field(default="auto_apply", max_length=50)  # auto_apply / manual / linkedin ...
    status: ApplicationStatus = ApplicationStatus.APPLIED
    notes: Optional[str] = Field(default=None, max_length=2000)


class StatusUpdate(BaseModel):
    status: ApplicationStatus
    note: Optional[str] = Field(default=None, max_length=500)


# --------------------------------------------------------------------------
# Repository (all SQL lives here)
# --------------------------------------------------------------------------
def _now() -> datetime:
    # stored as UTC (naive datetime, MySQL DATETIME has no timezone)
    return datetime.now(timezone.utc).replace(tzinfo=None)


class ApplicationRepository:
    def __init__(self, db_config: dict):
        self.db_config = dict(db_config)
        self.database = self.db_config["database"]
        if not re.fullmatch(r"[A-Za-z0-9_]+", self.database):
            raise ValueError("Database name may contain only letters, digits and _")
        self._ensure_database()
        self._init_schema()

    # ---- connection helpers ----
    def _ensure_database(self) -> None:
        cfg = {k: v for k, v in self.db_config.items() if k != "database"}
        conn = mysql.connector.connect(**cfg)
        try:
            cur = conn.cursor()
            cur.execute(
                f"CREATE DATABASE IF NOT EXISTS `{self.database}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
            conn.commit()
        finally:
            conn.close()

    @contextmanager
    def _conn(self):
        conn = mysql.connector.connect(**self.db_config)
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def _clean(row: Optional[dict]) -> Optional[dict]:
        """Convert datetime objects to ISO strings so FastAPI can return JSON."""
        if row is None:
            return None
        return {k: (v.isoformat() if isinstance(v, datetime) else v) for k, v in row.items()}

    def _init_schema(self) -> None:
        with self._conn() as c:
            cur = c.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS applications (
                    id          INT AUTO_INCREMENT PRIMARY KEY,
                    user_id     VARCHAR(100) NOT NULL,
                    job_title   VARCHAR(200) NOT NULL,
                    company     VARCHAR(200) NOT NULL,
                    job_url     VARCHAR(500) NOT NULL,
                    source      VARCHAR(50)  NOT NULL,
                    status      VARCHAR(30)  NOT NULL,
                    notes       TEXT NULL,
                    applied_at  DATETIME(6)  NOT NULL,
                    updated_at  DATETIME(6)  NOT NULL,
                    UNIQUE KEY uq_user_job (user_id, job_url),
                    INDEX idx_app_user_status (user_id, status)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS status_history (
                    id              INT AUTO_INCREMENT PRIMARY KEY,
                    application_id  INT NOT NULL,
                    from_status     VARCHAR(30) NULL,
                    to_status       VARCHAR(30) NOT NULL,
                    note            VARCHAR(500) NULL,
                    changed_at      DATETIME(6) NOT NULL,
                    CONSTRAINT fk_history_application
                        FOREIGN KEY (application_id) REFERENCES applications(id)
                        ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """
            )

    # ---- create ----
    def create(self, user_id: str, data: ApplicationCreate) -> dict:
        now = _now()
        with self._conn() as c:
            cur = c.cursor()
            cur.execute(
                """INSERT INTO applications
                   (user_id, job_title, company, job_url, source, status, notes,
                    applied_at, updated_at)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (user_id, data.job_title.strip(), data.company.strip(),
                 data.job_url.strip(), data.source, data.status.value,
                 data.notes, now, now),
            )
            app_id = cur.lastrowid
            cur.execute(
                """INSERT INTO status_history
                   (application_id, from_status, to_status, note, changed_at)
                   VALUES (%s,%s,%s,%s,%s)""",
                (app_id, None, data.status.value, "Application created", now),
            )
        return self.get(user_id, app_id)  # type: ignore[return-value]

    # ---- read ----
    def get(self, user_id: str, app_id: int) -> Optional[dict]:
        with self._conn() as c:
            cur = c.cursor(dictionary=True)
            cur.execute(
                "SELECT * FROM applications WHERE id = %s AND user_id = %s",
                (app_id, user_id),
            )
            return self._clean(cur.fetchone())

    def list(self, user_id: str, status: Optional[ApplicationStatus],
             company: Optional[str], page: int, page_size: int) -> tuple[list[dict], int]:
        where, params = ["user_id = %s"], [user_id]
        if status:
            where.append("status = %s")
            params.append(status.value)
        if company:
            where.append("LOWER(company) LIKE %s")
            params.append(f"%{company.lower()}%")
        clause = " AND ".join(where)
        with self._conn() as c:
            cur = c.cursor(dictionary=True)
            cur.execute(f"SELECT COUNT(*) AS n FROM applications WHERE {clause}", params)
            total = cur.fetchone()["n"]
            cur.execute(
                f"""SELECT * FROM applications WHERE {clause}
                    ORDER BY applied_at DESC, id DESC LIMIT %s OFFSET %s""",
                params + [page_size, (page - 1) * page_size],
            )
            rows = cur.fetchall()
        return [self._clean(r) for r in rows], total  # type: ignore[misc]

    def history(self, app_id: int) -> list[dict]:
        with self._conn() as c:
            cur = c.cursor(dictionary=True)
            cur.execute(
                "SELECT * FROM status_history WHERE application_id = %s ORDER BY id",
                (app_id,),
            )
            return [self._clean(r) for r in cur.fetchall()]  # type: ignore[misc]

    def counts_by_status(self, user_id: str) -> dict[str, int]:
        with self._conn() as c:
            cur = c.cursor(dictionary=True)
            cur.execute(
                "SELECT status, COUNT(*) AS n FROM applications "
                "WHERE user_id = %s GROUP BY status",
                (user_id,),
            )
            return {r["status"]: r["n"] for r in cur.fetchall()}

    # ---- update ----
    def update_status(self, user_id: str, app_id: int,
                      new_status: ApplicationStatus, note: Optional[str]) -> dict:
        """Raises LookupError (not found) or ValueError (invalid transition)."""
        with self._conn() as c:
            cur = c.cursor(dictionary=True)
            # FOR UPDATE locks the row so two updates cannot clash
            cur.execute(
                "SELECT status FROM applications WHERE id = %s AND user_id = %s FOR UPDATE",
                (app_id, user_id),
            )
            row = cur.fetchone()
            if row is None:
                raise LookupError("Application not found")
            current = ApplicationStatus(row["status"])
            if new_status not in ALLOWED_TRANSITIONS[current]:
                raise ValueError(
                    f"Cannot change status from {current.value} to {new_status.value}"
                )
            now = _now()
            cur.execute(
                "UPDATE applications SET status = %s, updated_at = %s WHERE id = %s",
                (new_status.value, now, app_id),
            )
            cur.execute(
                """INSERT INTO status_history
                   (application_id, from_status, to_status, note, changed_at)
                   VALUES (%s,%s,%s,%s,%s)""",
                (app_id, current.value, new_status.value, note, now),
            )
        return self.get(user_id, app_id)  # type: ignore[return-value]


# --------------------------------------------------------------------------
# Business logic helper
# --------------------------------------------------------------------------
def build_summary(counts: dict[str, int]) -> dict:
    total = sum(counts.values())
    full = {s.value: counts.get(s.value, 0) for s in ApplicationStatus}
    no_response = sum(full[s.value] for s in NO_RESPONSE_STATUSES)
    responded = total - no_response
    response_rate = round(responded / total * 100, 1) if total else 0.0
    return {
        "total": total,
        "by_status": full,
        "response_rate_percent": response_rate,
        "active": sum(
            full[s.value]
            for s in (S.APPLIED, S.UNDER_REVIEW, S.SHORTLISTED, S.INTERVIEW_SCHEDULED)
        ),
    }


# --------------------------------------------------------------------------
# Router factory
# --------------------------------------------------------------------------
def create_router(db_config: Optional[dict] = None) -> APIRouter:
    """db_config=None -> settings are taken from environment variables / .env"""
    repo = ApplicationRepository(db_config or get_db_config())
    router = APIRouter(prefix="/dashboard", tags=["dashboard"])

    def require_user(x_user_id: Optional[str]) -> str:
        # TODO: replace with real auth (JWT) when the auth module is ready
        if not x_user_id or not x_user_id.strip():
            raise HTTPException(status_code=401, detail="X-User-Id header is required")
        return x_user_id.strip()

    @router.post("/applications", status_code=201)
    def add_application(body: ApplicationCreate,
                        x_user_id: Optional[str] = Header(default=None)):
        user_id = require_user(x_user_id)
        try:
            return repo.create(user_id, body)
        except mysql.connector.IntegrityError as e:
            if e.errno == 1062:  # duplicate entry (same user + same job_url)
                raise HTTPException(status_code=409,
                                    detail="You already applied to this job URL")
            raise

    @router.get("/applications")
    def list_applications(
        status: Optional[ApplicationStatus] = None,
        company: Optional[str] = None,
        page: int = Query(1, ge=1),
        page_size: int = Query(20, ge=1, le=100),
        x_user_id: Optional[str] = Header(default=None),
    ):
        user_id = require_user(x_user_id)
        items, total = repo.list(user_id, status, company, page, page_size)
        return {"items": items, "total": total, "page": page, "page_size": page_size}

    @router.get("/applications/{app_id}")
    def get_application(app_id: int, x_user_id: Optional[str] = Header(default=None)):
        user_id = require_user(x_user_id)
        app = repo.get(user_id, app_id)
        if app is None:
            raise HTTPException(status_code=404, detail="Application not found")
        return app

    @router.patch("/applications/{app_id}/status")
    def update_status(app_id: int, body: StatusUpdate,
                      x_user_id: Optional[str] = Header(default=None)):
        user_id = require_user(x_user_id)
        try:
            return repo.update_status(user_id, app_id, body.status, body.note)
        except LookupError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except ValueError as e:
            raise HTTPException(status_code=409, detail=str(e))

    @router.get("/applications/{app_id}/history")
    def get_history(app_id: int, x_user_id: Optional[str] = Header(default=None)):
        user_id = require_user(x_user_id)
        if repo.get(user_id, app_id) is None:
            raise HTTPException(status_code=404, detail="Application not found")
        return {"application_id": app_id, "history": repo.history(app_id)}

    @router.get("/summary")
    def get_summary(x_user_id: Optional[str] = Header(default=None)):
        user_id = require_user(x_user_id)
        return build_summary(repo.counts_by_status(user_id))

    return router
