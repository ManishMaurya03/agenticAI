import os

SUPPORTED_EXTENSIONS = [".pdf", ".docx"]

def get_resume_files(folder_path):
    files = []
    
    for file in os.listdir(folder_path):
        if any(file.lower().endswith(ext) for ext in SUPPORTED_EXTENSIONS):
            files.append(os.path.join(folder_path, file))
    
    return files
def read_job_description(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()