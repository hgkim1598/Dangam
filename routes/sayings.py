# routes/sayings.py

from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select, delete
from typing import List

from models.sayings import FourChar, FourCharUpdate

from database.connection import get_session


saying_router = APIRouter(tags=["Sayings"])


@saying_router.get("/", response_model=List[FourChar])
async def retrieve_all_sayings(session=Depends(get_session)) -> List[FourChar]:
    statement = select(FourChar)
    sayings = session.exec(statement).all()  # 명언 테이블의 모든 값을 sayings에 리스트로 불러옴
    return sayings


@saying_router.get("/{id}", response_model=FourChar)
async def retrieve_saying(id: int, session=Depends(get_session)) -> FourChar:
    saying = session.get(FourChar, id)
    if saying:
        return saying
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="선택한 ID를 가진 명언이 존재하지 않습니다."
    )


@saying_router.post("/new", response_model=FourChar)
async def create_new_saying(new_saying: FourChar, session=Depends(get_session)) -> FourChar:
    session.add(new_saying)
    session.commit()
    session.refresh(new_saying)  # 캐시 데이터 업데이트
    return new_saying


@saying_router.put("/edit/{id}", response_model=FourChar)
async def update_saying(id: int, new_data: FourCharUpdate, session=Depends(get_session)) -> FourChar:
    saying = session.get(FourChar, id)
    if saying:
        saying_data = new_data.model_dump(exclude_unset=True)  # 클라이언트가 작성한 데이터만 변경하는 dict 생성
        for key, value in saying_data.items():
            setattr(saying, key, value)  # setattr(object, name, value) >>> object에 존재하는 속성의 값을 바꾸거나, 새로운 속성을 생성하여 값을 부여한다.
        session.add(saying)
        session.commit()
        session.refresh(saying)
        return saying
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="선택한 ID를 가진 명언이 존재하지 않습니다."
    )

@saying_router.delete("/delete/{id}")
async def delete_saying(id: int, session=Depends(get_session)) -> dict:
    saying = session.get(FourChar, id)
    if saying:
        session.delete(saying)
        session.commit()
        return {
            "message": "명언을 삭제했습니다."
        }
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="선택한 ID를 가진 명언이 존재하지 않습니다."
    )