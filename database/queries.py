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


# ---------------------------------------------------------
# 1. Get all jobs
# ---------------------------------------------------------

GET_ALL_JOBS = """
MATCH (company:Company)-[:OFFERS]->(job:Job)
RETURN
    job.id AS job_id,
    job.title AS title,
    job.location AS location,
    job.experience_required AS experience_required,
    job.description AS description,
    company.name AS company
ORDER BY job.title
"""


# ---------------------------------------------------------
# 2. Get a candidate
# ---------------------------------------------------------

GET_CANDIDATE = """
MATCH (candidate:Candidate {id: $candidate_id})
RETURN
    candidate.id AS id,
    candidate.name AS name,
    candidate.email AS email,
    candidate.location AS location,
    candidate.experience AS experience
"""


# ---------------------------------------------------------
# 3. Get candidate skills
# ---------------------------------------------------------

GET_CANDIDATE_SKILLS = """
MATCH (candidate:Candidate {id: $candidate_id})
      -[:HAS_SKILL]->(skill:Skill)

RETURN
    skill.id AS id,
    skill.name AS name,
    skill.category AS category
ORDER BY skill.name
"""


# ---------------------------------------------------------
# 4. Multi-hop job recommendation
# ---------------------------------------------------------
#
# Candidate
#     ↓ HAS_SKILL
# Skill
#     ↓ REQUIRES_SKILL
# Job
#     ↓ OFFERS
# Company
#
# ---------------------------------------------------------

GET_RECOMMENDED_JOBS = """
MATCH (candidate:Candidate {id: $candidate_id})
      -[:HAS_SKILL]->(skill:Skill)
      <-[:REQUIRES_SKILL]-(job:Job)
      <-[:OFFERS]-(company:Company)

WITH
    job,
    company,
    count(DISTINCT skill) AS matching_skills

RETURN
    job.id AS job_id,
    job.title AS title,
    job.location AS location,
    job.experience_required AS experience_required,
    company.name AS company,
    matching_skills

ORDER BY matching_skills DESC, job.title
"""


# ---------------------------------------------------------
# 5. Find jobs with missing skills
# ---------------------------------------------------------
#
# This identifies which required skills a candidate does
# not currently have.
#
# ---------------------------------------------------------

GET_SKILL_GAPS = """
MATCH (candidate:Candidate {id: $candidate_id})
      -[:HAS_SKILL]->(candidate_skill:Skill)

WITH candidate, collect(candidate_skill.id) AS candidate_skill_ids

MATCH (job:Job)-[:REQUIRES_SKILL]->(required_skill:Skill)

WHERE NOT required_skill.id IN candidate_skill_ids

RETURN
    job.id AS job_id,
    job.title AS title,
    required_skill.name AS missing_skill

ORDER BY job.title, missing_skill
"""


# ---------------------------------------------------------
# 6. Find companies hiring for matching skills
# ---------------------------------------------------------

GET_MATCHING_COMPANIES = """
MATCH (candidate:Candidate {id: $candidate_id})
      -[:HAS_SKILL]->(skill:Skill)
      <-[:REQUIRES_SKILL]-(job:Job)
      <-[:OFFERS]-(company:Company)

RETURN
    company.id AS company_id,
    company.name AS company,
    company.industry AS industry,
    company.location AS location,
    collect(DISTINCT job.title) AS matching_jobs,
    count(DISTINCT skill) AS matching_skills

ORDER BY matching_skills DESC, company.name
"""


# ---------------------------------------------------------
# 7. Candidate profile with connected information
# ---------------------------------------------------------

GET_CANDIDATE_PROFILE = """
MATCH (candidate:Candidate {id: $candidate_id})

OPTIONAL MATCH (candidate)-[:HAS_SKILL]->(skill:Skill)
OPTIONAL MATCH (candidate)-[:HAS_DEGREE]->(degree:Degree)
OPTIONAL MATCH (candidate)-[:HAS_CERTIFICATION]->(cert:Certification)

RETURN
    candidate.id AS id,
    candidate.name AS name,
    candidate.email AS email,
    candidate.location AS location,
    candidate.experience AS experience,
    collect(DISTINCT skill.name) AS skills,
    collect(DISTINCT degree.name + ' - ' + degree.specialization) AS degrees,
    collect(DISTINCT cert.name) AS certifications
"""


# ---------------------------------------------------------
# Python helper functions
# ---------------------------------------------------------

def get_all_jobs():
    with driver.session() as session:
        result = session.run(GET_ALL_JOBS)
        return [record.data() for record in result]


def get_candidate(candidate_id):
    with driver.session() as session:
        result = session.run(
            GET_CANDIDATE,
            candidate_id=candidate_id
        )
        record = result.single()

        if record is None:
            return None

        return record.data()


def get_candidate_skills(candidate_id):
    with driver.session() as session:
        result = session.run(
            GET_CANDIDATE_SKILLS,
            candidate_id=candidate_id
        )
        return [record.data() for record in result]


def get_recommended_jobs(candidate_id):
    with driver.session() as session:
        result = session.run(
            GET_RECOMMENDED_JOBS,
            candidate_id=candidate_id
        )
        return [record.data() for record in result]


def get_skill_gaps(candidate_id):
    with driver.session() as session:
        result = session.run(
            GET_SKILL_GAPS,
            candidate_id=candidate_id
        )
        return [record.data() for record in result]


def get_matching_companies(candidate_id):
    with driver.session() as session:
        result = session.run(
            GET_MATCHING_COMPANIES,
            candidate_id=candidate_id
        )
        return [record.data() for record in result]


def get_candidate_profile(candidate_id):
    with driver.session() as session:
        result = session.run(
            GET_CANDIDATE_PROFILE,
            candidate_id=candidate_id
        )

        record = result.single()

        if record is None:
            return None

        return record.data()

# ---------------------------------------------------------
# Get job details
# ---------------------------------------------------------

GET_JOB_DETAILS = """
MATCH (company:Company)-[:OFFERS]->(job:Job {id: $job_id})

OPTIONAL MATCH (job)-[:REQUIRES_SKILL]->(skill:Skill)

OPTIONAL MATCH (job)-[:PREFERS_DEGREE]->(degree:Degree)

RETURN
    job.id AS job_id,
    job.title AS title,
    job.location AS location,
    job.experience_required AS experience_required,
    job.description AS description,
    company.name AS company,
    company.industry AS industry,
    collect(DISTINCT skill.name) AS required_skills,
    collect(DISTINCT degree.name + ' - ' + degree.specialization) AS preferred_degrees
"""


def get_job_details(job_id):
    with driver.session() as session:
        result = session.run(
            GET_JOB_DETAILS,
            job_id=job_id
        )

        record = result.single()

        if record is None:
            return None

        return record.data()