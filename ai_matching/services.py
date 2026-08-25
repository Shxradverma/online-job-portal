from decimal import Decimal

from jobs.models import Job
from candidates.models import CandidateProfile

from .models import JobMatch


def normalize_skills(skills_text):
    if not skills_text:
        return set()

    return {
        skill.strip().lower()
        for skill in skills_text.split(",")
        if skill.strip()
    }


def calculate_job_match(candidate_profile, job):
    candidate_skills = normalize_skills(
        candidate_profile.skills
    )

    job_skills = normalize_skills(
        job.skills
    )

    if not job_skills:
        return {
            "score": Decimal("0.00"),
            "matched_skills": [],
            "missing_skills": [],
            "recommendation": "Job skills are not specified.",
        }

    matched = candidate_skills.intersection(job_skills)
    missing = job_skills - candidate_skills

    score = (len(matched) / len(job_skills)) * 100

    if score >= 80:
        recommendation = "Excellent match. You should apply."
    elif score >= 60:
        recommendation = "Good match. Consider improving the missing skills."
    elif score >= 40:
        recommendation = "Moderate match. Some important skills are missing."
    else:
        recommendation = "Low match. Consider developing more required skills."

    return {
        "score": Decimal(str(round(score, 2))),
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "recommendation": recommendation,
    }


def create_or_update_job_match(candidate_profile, job):
    result = calculate_job_match(
        candidate_profile,
        job,
    )

    job_match, created = JobMatch.objects.update_or_create(
        candidate=candidate_profile.user,
        job=job,
        defaults={
            "match_score": result["score"],
            "matched_skills": result["matched_skills"],
            "missing_skills": result["missing_skills"],
            "recommendation": result["recommendation"],
        },
    )

    return job_match