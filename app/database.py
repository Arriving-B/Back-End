from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# 데이터베이스 접속 주소
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

DATABASE_URL = f'mysql+pymysql://{os.environ["sql_db_user"]}:{os.environ["sql_db_password"]}@{os.environ["sql_db_address"]}:{os.environ["sql_db_port"]}/{os.environ["sql_db_connect"]}?charset=utf8'

# 데이터베이스 사용 규칙
engine = create_engine(
    DATABASE_URL, pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# 데이터베이스 모델 구성 클래스
Base = declarative_base()