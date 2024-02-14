# routes/sayings.py

from fastapi import APIRouter, HTTPException, status, Depends, Path
from sqlmodel import select, delete
from typing import List, Dict
from datetime import datetime, timedelta

from models.sayings import Saying, SayingUpdate
from models.category import Category

from database.connection import get_session


saying_router = APIRouter(tags=["Sayings"])


## CRUD START ############################################################################################## 
@saying_router.get("/", response_model=Dict[str, List[Saying]])
async def retrieve_all_sayings(session=Depends(get_session)) -> Dict[str, List[Saying]]:
    """
    저장된 명언 데이터들 조회
    """
    statement = select(Saying).order_by(Saying.id.desc()).limit(100)
    sayings = session.exec(statement).all()  # 데이터 테이블의 모든 값을 sayings에 리스트로 불러옴
    return {"content": sayings}


@saying_router.get("/{id}", response_model=Saying)
async def retrieve_saying(id: int, session=Depends(get_session)) -> Saying:
    """
    데이터 조회
    """
    saying = session.get(Saying, id)
    if saying:
        return saying
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="선택한 ID를 가진 데이터이 존재하지 않습니다."
    )


@saying_router.post("/new", response_model=Saying)
async def create_new_saying(new_saying: Saying, session=Depends(get_session)) -> Saying:
    """
    데이터 새로 생성
    """
    category_name = new_saying.category

    statement = select(Category).where(Category.name == category_name)
    category = session.exec(statement).one()

    if not category:
        category = Category(name=category_name)
        session.add(category)
        session.commit()
        session.refresh(category)

    session.add(new_saying)
    session.commit()
    session.refresh(new_saying)  # 캐시 데이터 업데이트
    return new_saying


@saying_router.put("/edit/{id}", response_model=Saying)
async def update_saying(id: int, new_data: SayingUpdate, session=Depends(get_session)) -> Saying:
    """
    데이터 수정
    """
    saying = session.get(Saying, id)
    if saying:
        saying_data = new_data.model_dump(exclude_unset=True)  # 클라이언트가 작성한 데이터만 변경하는 dict 생성
        saying_data["updated_at"] = (datetime.utcnow() + timedelta(hours=9)).replace(microsecond=0)  # updated_at 컬럼에 업데이트 시간을 작성
        for key, value in saying_data.items():
            setattr(saying, key, value)  # setattr(object, name, value) >>> object에 존재하는 속성의 값을 바꾸거나, 새로운 속성을 생성하여 값을 부여한다.
        session.add(saying)
        session.commit()
        session.refresh(saying)
        return saying
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="선택한 ID를 가진 데이터이 존재하지 않습니다."
    )

@saying_router.delete("/delete/{id}")
async def delete_saying(id: int, session=Depends(get_session)) -> dict:
    """
    데이터 삭제
    """
    saying = session.get(Saying, id)
    if saying:
        session.delete(saying)
        session.commit()
        return {
            "message": "데이터을 삭제했습니다."
        }
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="선택한 ID를 가진 데이터가 존재하지 않습니다."
    )
## CRUD END ##############################################################################################

# 필터링