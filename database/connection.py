# database/connection.py

from sqlmodel import SQLModel, Session, create_engine
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

# # 데이터베이스 접속 환경설정
class Settings(BaseSettings):
    DATABASE_CONNECTION_STRING: Optional[str] = None  # DB 연결주소, .env파일에서 불러온다.
    connect_args: dict = {"check_same_thread": False}  # False: 여러 쓰레드에서 동일한 연결을 공유

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()  # 환경변수
engine_url = create_engine(url=settings.DATABASE_CONNECTION_STRING, connect_args=settings.connect_args, echo=True)  # DB 엔진 생성


def conn():
    SQLModel.metadata.create_all(engine_url)  # DB 연결 및 초기화


# 세션을 관리하는 함수. FastAPI의 Depends()와 함께 사용하면 관리가 용이
def get_session():
    with Session(engine_url) as session:  # 세션을 종료하면 세션이 닫히도록 with문으로 작성
        yield session  # 각 작업마다 독립된 세션을 연결하기 위해 제너레이터 형태로 반환