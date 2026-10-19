from analyzer import analyze_resume

resume_text = "python developer with python, SQL and React skills."
jd_text = "Looking for a python developer with SQL and FastAPI."

result = analyze_resume(resume_text, jd_text)
print(result)

