from fastapi import FastAPI, UploadFile, File
import os
import shutil
from reader import read_job_description
from extractor import extract_resume_text
from prompt import build_resume_screening_prompt
from evaluator import evaluate_resume
from fastapi.responses import HTMLResponse
from typing import List

app = FastAPI()

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

JD_FILE = "./job_description.txt"
job_desc = read_job_description(JD_FILE)

@app.get("/")
def health_check():
    return {"status": "Resume Screening API is running"}

@app.post("/evaluate")
async def evaluate_resumes_api(files: List[UploadFile] = File(...)):
    results = []

    for file in files:
        file_path = f"{UPLOAD_DIR}/{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        resume_text = extract_resume_text(file_path)
        prompt = build_resume_screening_prompt(resume_text, job_desc)

        evaluation = evaluate_resume(prompt)

        if evaluation:
            formatted_result = {
                "candidate_name": evaluation.get("candidate_name", ""),
                "match_score": evaluation.get("match_score", ""),
                "classification": evaluation.get("classification", ""),
                "matched_skills": ",".join(evaluation.get("matched_skills", [])),
                "missing_skills": ", ".join(evaluation.get("missing_skills", [])),
                "recommendation": evaluation.get("recommendation", ""),
                "file_name": file.filename
            }
            results.append(formatted_result)

    return results

@app.get("/resume", response_class=HTMLResponse)
def ui():
    return """
    <html>
    <head>
        <title>Resume Screening AI</title>
        <style>
            body { font-family: Arial; margin: 40px; }
            table { border-collapse: collapse; width: 90%; }
            th, td { border: 1px solid #ddd; padding: 8px; }
            th { background-color: #f2f2f2; }
            input, button { padding: 10px; margin: 10px 0; }
            #loading { color: blue; font-weight: bold; display: none; }
        </style>
    </head>
    <body>
        <h2>AI Powered Resume Screening</h2>

        <form id="uploadForm">
            <input type="file" id="files" name="files" multiple required />
            <br/>
            <button id="submitBtn" type="submit">Evaluate Resumes</button>
        </form>

        <p id="loading">⏳ Processing resumes, please wait...</p>

        <h3>Results</h3>
        <table id="resultTable" style="display:none;">
            <thead>
                <tr>
                    <th>File</th>
                    <th>Candidate Name</th>
                    <th>Match Score</th>
                    <th>Classification</th>
                    <th>Matched Skills</th>
                    <th>Missing Skills</th>
                    <th>Recommendation</th>
                </tr>
            </thead>
            <tbody id="resultBody"></tbody>
        </table>

        <script>
            document.getElementById("uploadForm").onsubmit = async function(e) {
                e.preventDefault();

                let files = document.getElementById("files").files;
                let formData = new FormData();

                for (let i = 0; i < files.length; i++) {
                    formData.append("files", files[i]);
                }

                document.getElementById("loading").style.display = "block";
                document.getElementById("submitBtn").disabled = true;
                document.getElementById("resultTable").style.display = "none";

                let response = await fetch("/evaluate", {
                    method: "POST",
                    body: formData
                });

                let data = await response.json();

                document.getElementById("loading").style.display = "none";
                document.getElementById("submitBtn").disabled = false;

                let tbody = document.getElementById("resultBody");
                tbody.innerHTML = "";

                data.forEach(row => {
                    let tr = document.createElement("tr");

                    tr.innerHTML = `
                        <td>${row.file_name}</td>
                        <td>${row.candidate_name}</td>
                        <td>${row.match_score}</td>
                        <td>${row.classification}</td>
                        <td>${row.matched_skills}</td>
                        <td>${row.missing_skills}</td>
                        <td>${row.recommendation}</td>
                    `;

                    tbody.appendChild(tr);
                });

                document.getElementById("resultTable").style.display = "table";
            }
        </script>
    </body>
    </html>
    """