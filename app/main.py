from fastapi import FastAPI

from .database import engine
from .models import Base
from .routers.project_router import router as project_router
from .routers.plagiarism_router import router as plagiarism_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(project_router)

app.include_router(plagiarism_router)