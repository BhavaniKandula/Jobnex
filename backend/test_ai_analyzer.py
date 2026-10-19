import json 

from ai_analyzer import analyze_resume_with_ai
resume_text='''K.V.L. Bhavani
+91 8125378548  ·  kandulab43@gmail.com  ·  linkedin.com/in/bhavanikandula  ·  github.com/bhavanikandula  ·  Bengaluru, 
India
PROFESSIONAL SUMMARY
Python Backend Developer pursuing a B.Tech in Computer Science and Design (2025), with hands-on internship experience building 
Django web applications, REST APIs, and SQL-backed data pipelines. Skilled in applying academic knowledge to practical projects 
spanning data analysis, machine learning, and full-stack development, with familiarity with industry trends in AI and hybrid cloud 
solutions.
EXPERIENCE
Python Developer Intern | Algonex IT Solutions | Jun 2025 – Present
• Reduced data preparation time by 35% by developing 15+ MySQL pipelines using CTEs, stored procedures, and triggers across 
10,000+ records, demonstrating basic project management through end-to-end ownership of data workflows.
• Achieved R² > 0.88 by building a scikit-learn regression model trained on 11 rental datasets, then deployed predictions via a Streamlit 
application integrated with a Pickle-serialized model, delivering real-time business insights.
• Built and tested RESTful APIs and CRUD applications using Django, FastAPI, and Flask, integrating MySQL and SQLite databases 
with Git and GitHub for version control and collaborative development.
Artificial Intelligence Intern | SkillDzire | Dec 2024 – Apr 2025
• Applied theoretical AI and machine learning concepts from academic programs to practical tasks including data processing with 
Pandas and NumPy, supporting business operations through actionable dataset analysis.
• Gained exposure to industry trends in AI and enterprise technology, completing structured training aligned with current developments 
in Python-based AI development.
AI / Technical Trainee | TMI E2E Academy, Youth Employability Program | Prior to Dec 2024
• Completed technical training covering Python fundamentals, OOP, and data structures, translating academic knowledge into foun
dational software development skills.
PROJECTS
Aura Estates Bangalore: Rental Price Analysis and Prediction | Python, MySQL, Pandas, scikit-learn, 
Streamlit
• Developed 15+ SQL queries using CTEs and subqueries to extract and transform 10,000+ rental records, reducing data preparation 
time by 35% and demonstrating basic project management from data ingestion to model deployment.
Real-Time Facial Attendance Monitoring System | Python, OpenCV, Machine Learning, SQL
• Automated attendance tracking by implementing facial detection and recognition workflows using OpenCV and ML, integrating SQL 
for record-keeping and demonstrating application of theoretical knowledge to a practical problem.
Payment Gateway System | Python, Django, Django REST Framework, MySQL | github.com/BhavaniKan
dula/Algonex_Payment_System
• Built a Django backend with REST APIs for payment transactions and CRUD operations on a MySQL database, connected to an 
HTML/CSS/JavaScript front end, applying full-stack academic training to a production-style project.
EDUCATION
Bachelor of Technology, Computer Science and Design | Eswar College of Engineering, JNTUK | 2021 – 
Jun 2025 | CGPA: 7.73
SKILLS
Technical: Python, SQL, Django, Django REST Framework, FastAPI, Flask, RESTful API design, CRUD operations, JWT authentication, 
MySQL, SQLite, Pandas, NumPy, scikit-learn, Streamlit, OpenCV, OOP, data structures and algorithms, DBMS
Tools: Git, GitHub, Postman, Pickle, debugging, data visualization
CERTIFICATIONS
• Microsoft DigiSaksham AI Internship Program, Microsoft India
• Python Full Stack Development Training, JSPiders'''
jd_text ='''Your role and responsibilities
Students completing Engineering Degree ( BE/B.Tech/ME/M.Tech) by May 2027 with Computer Science, Electrical and Electronics Specializations/Branch of Studies only can apply•Only Students with a current aggregate of 6/ 60% or above CGPA / Percentage in the highest degree pursuing can apply

Required education
Bachelor's Degree
Required technical and professional expertise
• Exposure to Academic Programs: Currently enrolled at a university or educational institution, or recently completed qualification.

• Understanding of Business Operations: Familiarity with basic business concepts and processes, gained through academic studies or previous internships.

• Basic Administrative Skills: Experience with administrative tasks, such as data entry, record-keeping, or document management.

• Foundational Communication Skills: Ability to effectively communicate ideas and collaborate with colleagues in a team environment.

• Application of Theoretical Knowledge: Exposure to applying theoretical concepts and skills learned in an academic setting to practical problems or projects.



These are basic call outs and actual required skills may differ

Preferred technical and professional experience
• Familiarity with Industry Trends: Exposure to current industry trends and developments in a specific field, gained through academic studies or personal projects, would be beneficial in this role.

• Basic Project Management: Experience working on small projects or contributing to group assignments, demonstrating an understanding of project planning and execution principles.

• Data Analysis Skills: Exposure to data analysis tools and techniques, such as data visualization or statistical analysis, would be advantageous in supporting business operations and projects.

These are high-level callouts, and the specific skills required may vary based on the role.

Years of Experience:0 - 0    Job Title
Intern / Associate Engineer
Job ID
137023
City / Township / Village
Bangalore
State / Province
Karnataka
Country
India
Work arrangement
Hybrid
Area of work
Cloud
Employment type
Regular
Position type
Entry Level
Travel required
No Travel
Company
(0063) IBM India Private Limited
Shift
General (daytime)
Is this role a commissionable/sales incentive based position?
No
Apply'''
result = analyze_resume_with_ai(resume_text,jd_text)
try:
    data = json.loads(result)
    print("matchscore : " ,data["matched_score"])
    print("matched skills : " ,data["matched_skills"])
    print("missing skills : " ,data["missing_skills"])
    print("suggestions : " ,data["suggestions"])
    print("Summary :" , data["summary"])
except(json.JSONDecodeError,KeyError) as error:
    print("hey! fix the json or column names")
    print("hey! error is :" , error)

    
    

