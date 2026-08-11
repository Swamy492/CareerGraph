from database.queries import (
    get_recommended_jobs,
    get_skill_gaps,
    get_matching_companies
)


candidate_id = "C001"

print("\n--- RECOMMENDED JOBS ---")

jobs = get_recommended_jobs(candidate_id)

for job in jobs:
    print(job)


print("\n--- SKILL GAPS ---")

gaps = get_skill_gaps(candidate_id)

for gap in gaps:
    print(gap)


print("\n--- MATCHING COMPANIES ---")

companies = get_matching_companies(candidate_id)

for company in companies:
    print(company)