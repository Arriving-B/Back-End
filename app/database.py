from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# 데이터베이스 접속 주소
SQLALCHEMY_DATABASE_URL = ""

# 데이터베이스 사용 규칙
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_sam_thread": False}
)
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# 데이터베이스 모델 구성 클래스
Base = declarative_base()