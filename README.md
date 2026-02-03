# AI Resume Screening Agent

An AI-powered Resume Screening Agent built using Python and OpenAI GPT model that helps automatically analyze uploaded resumes and evaluate candidates against job requirements.
The system allows users to upload resumes from a UI and receive structured insights such as skill match, experience summary, and hiring recommendation.

# Features
	•	Resume upload via UI (PDF/Text)
	•	AI-based resume analysis using OpenAI GPT model
	• Extracts:
	•	Candidate skills
	•	Work experience summary
	•	Strengths & gaps
	•	Job match score
	•	Structured evaluation output
	• Fast and easy screening for recruiters
	•	Secure API-based processing

# Architecture Overview
UI (Resume Upload)
        |
        v
Python Backend (FastAPI / Flask)
        |
        v
OpenAI GPT Model (Resume Analysis)
        |
        v
Structured Result (JSON / UI Display)
