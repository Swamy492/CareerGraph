# CareerGraph

CareerGraph is a graph-powered career recommendation application built using Flask and CognoDB.

The application connects candidates, skills, jobs, companies, degrees, and certifications using a graph database. It provides job recommendations based on candidate skills and identifies skill gaps and matching companies.

## Features

- View available jobs
- View detailed job information
- View candidate profiles
- Recommend jobs based on candidate skills
- Identify missing skills for job opportunities
- Find companies hiring for matching skills
- View required skills for jobs
- View preferred degrees for jobs
- Graph-based relationship traversal using CognoDB

## Technology Stack

- Python
- Flask
- CognoDB
- Neo4j Python Driver
- Cypher
- HTML
- CSS
- JavaScript
- Bootstrap
- python-dotenv

## Project Structure

```text
CareerGraph/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── database/
│   ├── queries.py
│   ├── schema.py
│   └── seed.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── jobs.html
│   ├── candidate.html
│   └── job.html
│
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── app.js