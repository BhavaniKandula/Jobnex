import json
from ai_analyzer import analyze_resume_with_ai


resume_text='''LANKEPALLI KAVERI
kaverilankepalli@gmail.com | +91 86888 87349
LinkedIn: linkedin.com/in/kaveri-lankepalli | GitHub: github.com/kaveri-chowdhary
PROFESSIONAL SUMMARY
Aspiring Data Analyst with a strong foundation in Python, SQL, MySQL, Excel, Power BI, and data analysis. Hands-on
experience through academic projects and an internship, with an interest in applying analytical thinking and data-driven
approaches to business problems.
TECHNICAL SKILLS
Programming & Analysis: Python, Pandas, data cleaning & preprocessing
Databases & Querying: SQL, MySQL
Visualization & Reporting: Power BI (dashboards), Excel
Machine Learning: Scikit-learn, feature preparation, classification
Tools & Other: GitHub, HTML, CSS, JavaScript
UNIVERSITY PROJECTS
ML-DRIVEN DYNAMIC TEST ITEM GENERATOR
• Developed a machine learning-based system to dynamically generate test questions based on selected topics and
difficulty levels.
• Implemented data preprocessing and feature preparation to improve the quality and consistency of generated test
items.
• Designed the system to generate varied questions dynamically, reducing repetitive and manually created test
content.
• Applied machine learning techniques to support automated question generation and classification based on input
requirements.
• Technologies: Python, Machine Learning, Pandas, Scikit-learn
PASSWORD STRENGTH CHECKER
Oct 2024
• Designed and developed a Password Strength Checker to evaluate password security based on length, character
diversity, and pattern complexity.
• Implemented real-time validation using JavaScript to provide instant feedback on password strength (Weak / Medium
/ Strong).
• Technologies: HTML, CSS, JavaScript
INTERNSHIP EXPERIENCE
Full Stack Web Developer Intern | MOTION CUT CRAFTING FUTURE’S
Nov 2024 – Jan 2025
• Designed and developed responsive user interfaces using HTML, CSS, and JavaScript, ensuring cross-browser
compatibility and mobile responsiveness.
• Integrated front-end interfaces with back-end logic, enabling smooth data flow and dynamic content rendering.
• Implemented form validation, authentication flows, and basic CRUD operations to enhance user interaction.
EDUCATION
DHANALAKSHMI SRINIVASAN UNIVERSITY | Trichy, TN
Bachelor of Technology in Computer Science and Engineering | CGPA: 7.3
NARAYANA JUNIOR COLLEGE | Andhra Pradesh
Intermediate: M.P.C | CGPA: 8.9
SRI NETAJI MSR PILOT HIGH SCHOOL | Andhra Pradesh
Secondary Education | CGPA: 10
ACTIVITIES
2022 – 2026
Jun 2020 – Mar 2022
Jun 2019 – Apr 2020
• Participated in Power BI Workshop by Office Mater, learning dashboard development and visualizations using
real-time datasets.'''


jd_text='''
HomeIBM
IBM Careers
Login
< Back to search results
Intern / Associate Engineer
Bangalore, Karnataka, India
Entry Level
Email
X
LinkedIn
Apply now
Introduction
This is a pre-requisition to screen and assess applicants across roles of IBM for different line of business and can be but not limited to the below units

IT Services & Consulting: Delivers enterprise technology, hybrid cloud solutions, and consulting services. Infrastructure & AI: Focuses on enterprise AI agents, hybrid cloud architecture, and infrastructure innovation

Your role and responsibilities
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

Years of Experience:0 - 0
ABOUT BUSINESS UNIT
IBM Corporate Headquarters (CHQ) team represents a variety of functions such as marketing, finance, legal, operations, HR, and more, all working together to solve some of the world's most complex problems, help our clients achieve success and build collaborative work environments for IBMers.
YOUR LIFE @ IBM
In a world where technology never stands still, we understand that, dedication to our clients success, innovation that matters, and trust and personal responsibility in all our relationships, lives in what we do as IBMers as we strive to be the catalyst that makes the world work better.

Being an IBMer means you’ll be able to learn and develop yourself and your career, you’ll be encouraged to be courageous and experiment everyday, all whilst having continuous trust and support in an environment where everyone can thrive whatever their personal or professional background.



Our IBMers are growth minded, always staying curious, open to feedback and learning new information and skills to constantly transform themselves and our company. They are trusted to provide on-going feedback to help other IBMers grow, as well as collaborate with colleagues keeping in mind a team focused approach to include different perspectives to drive exceptional outcomes for our customers. The courage our IBMers have to make critical decisions everyday is essential to IBM becoming the catalyst for progress, always embracing challenges with resources they have to hand, a can-do attitude and always striving for an outcome focused approach within everything that they do.



Are you ready to be an IBMer?

ABOUT IBM
IBM’s greatest invention is the IBMer. We believe that through the application of intelligence, reason and science, we can improve business, society and the human condition, bringing the power of an open hybrid cloud and AI strategy to life for our clients and partners around the world.



Restlessly reinventing since 1911, we are not only one of the largest corporate organizations in the world, we’re also one of the biggest technology and consulting employers, with many of the Fortune 500 companies relying on the IBM Cloud to run their business. 



At IBM, we pride ourselves on being an early adopter of artificial intelligence, quantum computing and blockchain. Now it’s time for you to join us on our journey to being a responsible technology innovator and a force for good in the world.

IBM is proud to be an equal-opportunity employer. All qualified applicants will receive consideration for employment without regard to race, color, religion, sex, gender, gender identity or expression, sexual orientation, national origin, genetics, pregnancy, disability, neurodivergence, age, or other characteristics protected by the applicable law. IBM is also committed to compliance with all fair employment practices regarding citizenship and immigration status.

OTHER RELEVANT JOB DETAILS
When applying to jobs of your interest, we recommend that you do so for those that match your experience and expertise. Our recruiters advise that you apply to not more than 3 roles in a year for the best candidate experience. For additional information about location requirements, please discuss with the recruiter following submission of your application.


Job Title
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
Apply now
< Back to search results
IBM Logo
Application Info
Be aware: Recruitment Scams
Privacy statement
Learn more about IBM
Linkedin Logo
Twitter Logo
Youtube Logo
Glassdoor Logo
Instagram Logo
Blog Logo
English
Contact IBM
Privacy
Terms of use
Accessibility'''



result=analyze_resume_with_ai(resume_text,jd_text)
try:
    data=json.load(result)
    print("matchscore:",data["matched_score"])
    print("matching skills:",data["matched_skills"])
    print("missing skills:",data["missing_skills"])
    print("suggestions:",data["suggestions"])
    print("summary:",data["summary"])
except(json.JSONDecodeError,KeyError)as error:
    print("Hey! Fix the json or column names")
    print("Hey! Error is:",error)