def build_resume_screening_prompt(resume_text, job_description):
    prompt = f"""
You are an expert AI recruiter.

Evaluate the following resume against the job description.

Job Description:
----------------
{job_description}

Resume:
-------
{resume_text}

Your tasks:
1. Identify candidate name from resume
2. Compare skills, experience, and domain relevance
3. List matched and missing skills.
4. Give a match score from 0 to 100
5. Classify candidate as:
   - Strong Fit
   - Moderate Fit
   - Weak Fit
6. Provide a clear recommendation (Shortlist / Consider / Reject)

Return ONLY the following JSON format:

{{
  "candidate_name": "",
  "match_score": 0,
  "classification": "",
  "matched_skills": [],
  "missing_skills": [],
  "recommendation": ""
}}
"""
    return prompt