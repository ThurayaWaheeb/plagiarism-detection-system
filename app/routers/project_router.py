from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..services.file_service import extract_text_from_file
from ..services.text_cleaner import optimal_arabic_cleaner
from ..services.chunking import chunk_text_with_overlap
from ..crud.project_crud import create_project, delete_project_by_id
from ..models import Project


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/add_project")
def add_project(
    title: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    raw_text = extract_text_from_file(file)

    if not raw_text:
        return {"error": "No text extracted from file."}

    cleaned_text = optimal_arabic_cleaner(raw_text)
    chunks = chunk_text_with_overlap(cleaned_text, 20, 5)

    project = create_project(db, title, chunks)

    return {
        "message": "Project stored successfully",
        "total_chunks": len(chunks),
        "project_id": project.id
    }


@router.delete("/delete_project/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):

    project = delete_project_by_id(db, project_id)

    if not project:
        return {"error": "Project not found"}

    return {"message": f"Project {project_id} deleted successfully"}


@router.get("/projects")
def get_projects(db: Session = Depends(get_db)):

    projects = db.query(Project).all()

    results = []

    for project in projects:
        results.append({
            "id": project.id,
            "title": project.title,
            "created_at": project.created_at
        })

    return results