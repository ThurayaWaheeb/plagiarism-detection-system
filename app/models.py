from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # علاقة عكسية مع Chunk + Cascade
    chunks = relationship(
        "Chunk",
        back_populates="project",
        cascade="all, delete-orphan"
    )


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))

    project = relationship("Project", back_populates="chunks")

    # علاقة عكسية مع Vector + Cascade
    vectors = relationship(
        "Vector",
        back_populates="chunk",
        cascade="all, delete-orphan"
    )


class Vector(Base):
    __tablename__ = "vectors"

    id = Column(Integer, primary_key=True, index=True)
    embedding = Column(Text, nullable=False)
    chunk_id = Column(Integer, ForeignKey("chunks.id", ondelete="CASCADE"))

    chunk = relationship("Chunk", back_populates="vectors")