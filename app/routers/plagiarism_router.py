from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import Chunk, Project

from ..services.file_service import extract_text_from_file
from ..services.text_cleaner import optimal_arabic_cleaner, remove_unwanted_sections
from ..services.chunking import chunk_text_with_overlap
from ..services.similarity_service import check_similarity
from ..services.report_service import generate_plagiarism_report

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/check_plagiarism")
def check_plagiarism(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    raw_text = extract_text_from_file(file)

    cleaned_text = optimal_arabic_cleaner(raw_text)
    cleaned_text = remove_unwanted_sections(cleaned_text)

    student_chunks = chunk_text_with_overlap(cleaned_text, 20, 5)

    db_chunks = []
    db_metadata = []

    chunks = db.query(Chunk).all()

    for chunk in chunks:

        db_chunks.append(chunk.content)

        project = db.query(Project).filter(Project.id == chunk.project_id).first()

        db_metadata.append({
            "id": project.id,
            "title": project.title
        })

    doc_matches, detailed_report = check_similarity(
        student_chunks,
        db_chunks,
        db_metadata
    )

    # -----------------------------------
    # حساب نسبة الانتحال
    # -----------------------------------

    total_student_chunks = len(student_chunks)

    total_matches = sum(doc_matches.values())

    overall_similarity = 0

    if total_student_chunks > 0:
        overall_similarity = (total_matches / total_student_chunks) * 100

    # -----------------------------------
    # حساب المشاريع الأكثر تشابهًا
    # -----------------------------------

    top_projects = []

    for proj_id, count in doc_matches.items():

        project = db.query(Project).filter(Project.id == proj_id).first()

        similarity = (count / total_student_chunks) * 100

        top_projects.append({
            "project_title": project.title,
            "similarity": round(similarity, 2)
        })

    # -----------------------------------
    # التقرير النهائي
    # -----------------------------------

    report = generate_plagiarism_report(
    file.filename,
    overall_similarity,
    top_projects
)       

    return report

