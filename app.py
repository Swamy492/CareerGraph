from flask import Flask, render_template, request

from database.queries import (
    get_all_jobs,
    get_candidate,
    get_candidate_skills,
    get_recommended_jobs,
    get_skill_gaps,
    get_matching_companies,
    get_candidate_profile,
    get_job_details
)

app = Flask(__name__)


@app.route("/")
def index():
    """Home page."""
    try:
        jobs = get_all_jobs()

        return render_template(
            "index.html",
            jobs=jobs
        )

    except Exception as error:
        print("Database error:", error)

        return render_template(
            "index.html",
            jobs=[],
            error="Unable to connect to the database. Please try again later."
        ), 503


@app.route("/jobs")
def jobs():
    """Display all available jobs."""
    try:
        all_jobs = get_all_jobs()

        return render_template(
            "jobs.html",
            jobs=all_jobs
        )

    except Exception as error:
        print("Database error:", error)

        return render_template(
            "jobs.html",
            jobs=[],
            error="Unable to load jobs."
        ), 503


@app.route("/job/<job_id>")
def job_details(job_id):
    """Display details for a specific job."""
    try:
        job = get_job_details(job_id)

        if job is None:
            return render_template(
                "job.html",
                job=None,
                error="Job not found."
            ), 404

        return render_template(
            "job.html",
            job=job
        )

    except Exception as error:
        print("Database error:", error)

        return render_template(
            "job.html",
            job=None,
            error="Unable to load job details."
        ), 503

@app.route("/candidate/<candidate_id>")
def candidate(candidate_id):
    """Display candidate profile and recommendations."""
    try:
        profile = get_candidate_profile(candidate_id)

        if profile is None:
            return render_template(
                "candidate.html",
                profile=None,
                recommendations=[],
                skill_gaps=[],
                companies=[],
                error="Candidate not found."
            ), 404

        recommendations = get_recommended_jobs(candidate_id)
        skill_gaps = get_skill_gaps(candidate_id)
        companies = get_matching_companies(candidate_id)

        return render_template(
            "candidate.html",
            profile=profile,
            recommendations=recommendations,
            skill_gaps=skill_gaps,
            companies=companies
        )

    except Exception as error:
        print("Database error:", error)

        return render_template(
            "candidate.html",
            profile=None,
            recommendations=[],
            skill_gaps=[],
            companies=[],
            error="Unable to load candidate information."
        ), 503


@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        "base.html",
        error="The page you requested was not found."
    ), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template(
        "base.html",
        error="Something went wrong. Please try again."
    ), 500


if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )