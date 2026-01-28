from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from backend.file_scanner import scan_folders, find_file_by_name
from backend.file_qa import answer_from_file

app = FastAPI(title="KnowSync – Smart Data Companion")

templates = Jinja2Templates(directory="frontend")

# -------------------------------
# CONFIG
# -------------------------------
FOLDERS = [
    "C:/Users/admin/OneDrive/Documents",
    "C:/Users/admin/OneDrive/Desktop"
]

FILES_INDEX = None


# -------------------------------
# LAZY FILE SCAN
# -------------------------------
def get_files_index():
    global FILES_INDEX
    if FILES_INDEX is None:
        FILES_INDEX = scan_folders(FOLDERS)
    return FILES_INDEX


# -------------------------------
# HOME PAGE
# -------------------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# -------------------------------
# MAIN QUESTION HANDLER
# -------------------------------
@app.post("/ask", response_class=HTMLResponse)
def ask(request: Request, question: str = Form(...)):
    q = question.lower()
    files_index = get_files_index()

    # -------- INTENT 1: FILE LOCATION --------
    if any(w in q for w in ["where", "find", "path", "location"]):

        if "resume" in q:
            keyword = "resume"
        elif "certificate" in q:
            keyword = "certificate"
        elif "offer" in q:
            keyword = "offer"
        elif "memo" in q:
            keyword = "memo"
        else:
            keyword = q

        results = find_file_by_name(files_index, keyword)

        if results:
            answer = "<ul class='results'>"
            for r in results:
                file_path = r["file_path"].replace("\\", "/")
                answer += (
                    "<li>"
                    f"<strong>{r['file_name']}</strong><br>"
                    f"<a class='path' href='file:///{file_path}' target='_blank'>"
                    f"{r['file_path']}</a>"
                    "</li>"
                )
            answer += "</ul>"
        else:
            answer = "<p>No matching file found.</p>"

    # -------- INTENT 2: FILE SUMMARY --------
    elif any(w in q for w in ["summarize", "summary", "what is inside", "content", "explain"]):

        resume_files = find_file_by_name(files_index, "resume")

        if not resume_files:
            answer = "<p>Resume file not found.</p>"
        else:
            summary = answer_from_file(
                resume_files[0]["file_path"],
                question
            )
            answer = f"<p>{summary}</p>"

    # -------- INTENT 3: SMART PERSONAL FALLBACK --------
    else:
        personal_keywords = [
            "my name", "my skills", "my education", "my cgpa",
            "my projects", "my experience", "about me", "who am i"
        ]

        resume_files = find_file_by_name(files_index, "resume")

        if resume_files and any(k in q for k in personal_keywords):
            try:
                response = answer_from_file(
                    resume_files[0]["file_path"],
                    question
                )

                if response and response.strip():
                    answer = f"<p>{response}</p>"
                else:
                    answer = (
                        "<p>I looked into your resume but couldn't find a clear answer.</p>"
                    )

            except Exception:
                answer = (
                    "<p>An error occurred while reading your resume.</p>"
                )

        else:
            answer = (
                "<p>I couldn't clearly understand your request.</p>"
                "<p>Try asking:</p>"
                "<ul>"
                "<li>Where is my resume?</li>"
                "<li>Summarize my resume</li>"
                "<li>What is inside my resume?</li>"
                "<li>What is my name?</li>"
                "</ul>"
            )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "answer": answer
        }
    )
