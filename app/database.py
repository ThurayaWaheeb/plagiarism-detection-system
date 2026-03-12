from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# مسار قاعدة البيانات
DATABASE_URL = "sqlite:///./plagiarism.db"

# إنشاء المحرك
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# إنشاء جلسة اتصال
SessionLocal = sessionmaker(bind=engine)

# الأساس اللي راح تبنى عليه الجداول
Base = declarative_base()