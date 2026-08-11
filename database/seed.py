import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("COGNODB_URI")
USERNAME = os.getenv("COGNODB_USERNAME")
PASSWORD = os.getenv("COGNODB_PASSWORD")

if not URI or not USERNAME or not PASSWORD:
    raise ValueError("CognoDB environment variables are missing.")

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


def seed_database():
    with driver.session() as session:

        # -------------------------
        # Candidates
        # -------------------------

        session.run("""
            UNWIND $candidates AS candidate
            MERGE (c:Candidate {id: candidate.id})
            SET c.name = candidate.name,
                c.email = candidate.email,
                c.location = candidate.location,
                c.experience = candidate.experience
        """, candidates=[
            {
                "id": "C001",
                "name": "Swamy",
                "email": "swamy@example.com",
                "location": "Hyderabad",
                "experience": 0
            },
            {
                "id": "C002",
                "name": "Rahul",
                "email": "rahul@example.com",
                "location": "Bangalore",
                "experience": 1
            },
            {
                "id": "C003",
                "name": "Priya",
                "email": "priya@example.com",
                "location": "Chennai",
                "experience": 2
            }
        ])

        # -------------------------
        # Skills
        # -------------------------

        session.run("""
            UNWIND $skills AS skill
            MERGE (s:Skill {id: skill.id})
            SET s.name = skill.name,
                s.category = skill.category
        """, skills=[
            {"id": "S001", "name": "Python", "category": "Programming"},
            {"id": "S002", "name": "SQL", "category": "Database"},
            {"id": "S003", "name": "JavaScript", "category": "Programming"},
            {"id": "S004", "name": "Flask", "category": "Framework"},
            {"id": "S005", "name": "React", "category": "Frontend"},
            {"id": "S006", "name": "Git", "category": "Tools"},
            {"id": "S007", "name": "Java", "category": "Programming"}
        ])

        # -------------------------
        # Degrees
        # -------------------------

        session.run("""
            UNWIND $degrees AS degree
            MERGE (d:Degree {id: degree.id})
            SET d.name = degree.name,
                d.specialization = degree.specialization
        """, degrees=[
            {
                "id": "D001",
                "name": "B.Tech",
                "specialization": "Electronics and Communication Engineering"
            },
            {
                "id": "D002",
                "name": "B.Tech",
                "specialization": "Computer Science Engineering"
            },
            {
                "id": "D003",
                "name": "MCA",
                "specialization": "Computer Applications"
            }
        ])

        # -------------------------
        # Certifications
        # -------------------------

        session.run("""
            UNWIND $certifications AS certification
            MERGE (c:Certification {id: certification.id})
            SET c.name = certification.name,
                c.issuer = certification.issuer
        """, certifications=[
            {
                "id": "CERT001",
                "name": "Python Basics",
                "issuer": "HackerRank"
            },
            {
                "id": "CERT002",
                "name": "SQL Basics",
                "issuer": "HackerRank"
            },
            {
                "id": "CERT003",
                "name": "Introduction to IoT",
                "issuer": "MREC"
            }
        ])

        # -------------------------
        # Companies
        # -------------------------

        session.run("""
            UNWIND $companies AS company
            MERGE (c:Company {id: company.id})
            SET c.name = company.name,
                c.industry = company.industry,
                c.location = company.location
        """, companies=[
            {
                "id": "CO001",
                "name": "Wexa AI",
                "industry": "Artificial Intelligence",
                "location": "Remote"
            },
            {
                "id": "CO002",
                "name": "TechNova Solutions",
                "industry": "Information Technology",
                "location": "Hyderabad"
            },
            {
                "id": "CO003",
                "name": "DataSphere",
                "industry": "Data Analytics",
                "location": "Bangalore"
            }
        ])

        # -------------------------
        # Jobs
        # -------------------------

        session.run("""
            UNWIND $jobs AS job
            MERGE (j:Job {id: job.id})
            SET j.title = job.title,
                j.location = job.location,
                j.experience_required = job.experience_required,
                j.description = job.description
        """, jobs=[
            {
                "id": "J001",
                "title": "Python Developer",
                "location": "Hyderabad",
                "experience_required": 0,
                "description": "Develop backend applications using Python and Flask."
            },
            {
                "id": "J002",
                "title": "Full Stack Developer",
                "location": "Bangalore",
                "experience_required": 1,
                "description": "Build web applications using Python, JavaScript and React."
            },
            {
                "id": "J003",
                "title": "Data Analyst",
                "location": "Bangalore",
                "experience_required": 0,
                "description": "Analyze business data using SQL and Python."
            },
            {
                "id": "J004",
                "title": "Java Developer",
                "location": "Hyderabad",
                "experience_required": 1,
                "description": "Develop enterprise applications using Java and SQL."
            }
        ])

        # -------------------------
        # Candidate -> Skill
        # -------------------------

        session.run("""
            UNWIND $relationships AS rel
            MATCH (c:Candidate {id: rel.candidate_id})
            MATCH (s:Skill {id: rel.skill_id})
            MERGE (c)-[:HAS_SKILL]->(s)
        """, relationships=[
            {"candidate_id": "C001", "skill_id": "S001"},
            {"candidate_id": "C001", "skill_id": "S002"},
            {"candidate_id": "C001", "skill_id": "S003"},
            {"candidate_id": "C001", "skill_id": "S004"},
            {"candidate_id": "C001", "skill_id": "S006"},

            {"candidate_id": "C002", "skill_id": "S001"},
            {"candidate_id": "C002", "skill_id": "S002"},
            {"candidate_id": "C002", "skill_id": "S005"},
            {"candidate_id": "C002", "skill_id": "S006"},

            {"candidate_id": "C003", "skill_id": "S007"},
            {"candidate_id": "C003", "skill_id": "S002"},
            {"candidate_id": "C003", "skill_id": "S003"}
        ])

        # -------------------------
        # Candidate -> Degree
        # -------------------------

        session.run("""
            UNWIND $relationships AS rel
            MATCH (c:Candidate {id: rel.candidate_id})
            MATCH (d:Degree {id: rel.degree_id})
            MERGE (c)-[:HAS_DEGREE]->(d)
        """, relationships=[
            {"candidate_id": "C001", "degree_id": "D001"},
            {"candidate_id": "C002", "degree_id": "D002"},
            {"candidate_id": "C003", "degree_id": "D003"}
        ])

        # -------------------------
        # Candidate -> Certification
        # -------------------------

        session.run("""
            UNWIND $relationships AS rel
            MATCH (c:Candidate {id: rel.candidate_id})
            MATCH (cert:Certification {id: rel.certification_id})
            MERGE (c)-[:HAS_CERTIFICATION]->(cert)
        """, relationships=[
            {"candidate_id": "C001", "certification_id": "CERT001"},
            {"candidate_id": "C001", "certification_id": "CERT002"},
            {"candidate_id": "C002", "certification_id": "CERT001"},
            {"candidate_id": "C003", "certification_id": "CERT002"}
        ])

        # -------------------------
        # Company -> Job
        # -------------------------

        session.run("""
            UNWIND $relationships AS rel
            MATCH (c:Company {id: rel.company_id})
            MATCH (j:Job {id: rel.job_id})
            MERGE (c)-[:OFFERS]->(j)
        """, relationships=[
            {"company_id": "CO001", "job_id": "J001"},
            {"company_id": "CO001", "job_id": "J002"},
            {"company_id": "CO002", "job_id": "J003"},
            {"company_id": "CO003", "job_id": "J004"}
        ])

        # -------------------------
        # Job -> Skill
        # -------------------------

        session.run("""
            UNWIND $relationships AS rel
            MATCH (j:Job {id: rel.job_id})
            MATCH (s:Skill {id: rel.skill_id})
            MERGE (j)-[:REQUIRES_SKILL]->(s)
        """, relationships=[
            {"job_id": "J001", "skill_id": "S001"},
            {"job_id": "J001", "skill_id": "S002"},
            {"job_id": "J001", "skill_id": "S004"},

            {"job_id": "J002", "skill_id": "S001"},
            {"job_id": "J002", "skill_id": "S003"},
            {"job_id": "J002", "skill_id": "S005"},

            {"job_id": "J003", "skill_id": "S001"},
            {"job_id": "J003", "skill_id": "S002"},

            {"job_id": "J004", "skill_id": "S007"},
            {"job_id": "J004", "skill_id": "S002"}
        ])

        # -------------------------
        # Job -> Degree
        # -------------------------

        session.run("""
            UNWIND $relationships AS rel
            MATCH (j:Job {id: rel.job_id})
            MATCH (d:Degree {id: rel.degree_id})
            MERGE (j)-[:PREFERS_DEGREE]->(d)
        """, relationships=[
            {"job_id": "J001", "degree_id": "D001"},
            {"job_id": "J002", "degree_id": "D002"},
            {"job_id": "J003", "degree_id": "D002"},
            {"job_id": "J004", "degree_id": "D002"}
        ])

        print("CareerGraph seed data loaded successfully.")


if __name__ == "__main__":
    try:
        seed_database()
    except Exception as error:
        print("Seed failed:")
        print(error)
    finally:
        driver.close()