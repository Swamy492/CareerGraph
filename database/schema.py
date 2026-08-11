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


CONSTRAINTS = [
    """
    CREATE CONSTRAINT candidate_id_unique IF NOT EXISTS
    FOR (c:Candidate)
    REQUIRE c.id IS UNIQUE
    """,
    """
    CREATE CONSTRAINT skill_id_unique IF NOT EXISTS
    FOR (s:Skill)
    REQUIRE s.id IS UNIQUE
    """,
    """
    CREATE CONSTRAINT job_id_unique IF NOT EXISTS
    FOR (j:Job)
    REQUIRE j.id IS UNIQUE
    """,
    """
    CREATE CONSTRAINT company_id_unique IF NOT EXISTS
    FOR (c:Company)
    REQUIRE c.id IS UNIQUE
    """,
    """
    CREATE CONSTRAINT degree_id_unique IF NOT EXISTS
    FOR (d:Degree)
    REQUIRE d.id IS UNIQUE
    """,
    """
    CREATE CONSTRAINT certification_id_unique IF NOT EXISTS
    FOR (c:Certification)
    REQUIRE c.id IS UNIQUE
    """
]


def create_constraints():
    with driver.session() as session:
        for query in CONSTRAINTS:
            session.run(query)


if __name__ == "__main__":
    try:
        create_constraints()
        print("Graph constraints created successfully.")
    except Exception as error:
        print("Failed to create constraints:")
        print(error)
    finally:
        driver.close()