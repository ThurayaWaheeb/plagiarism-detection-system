from ..services.embedding_service import get_embedding
from sqlalchemy.orm import Session
from ..models import Project, Chunk, Vector


def create_project(db: Session, title: str, chunks: list):

    new_project = Project(title=title)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    for chunk_text in chunks:

        new_chunk = Chunk(
            content=chunk_text,
            project_id=new_project.id
        )

        db.add(new_chunk)
        db.commit()
        db.refresh(new_chunk)

        vector = get_embedding(chunk_text)

        new_vector = Vector(
            embedding=str(vector),
            chunk_id=new_chunk.id
        )

        db.add(new_vector)
        db.commit()

    return new_project


def delete_project_by_id(db: Session, project_id: int):

    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        return None

    db.delete(project)
    db.commit()

    return project