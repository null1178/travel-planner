from fastapi import APIRouter, Depends, HTTPException, status, Body
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from ..database import get_db
from ..user_models import User, SavedPlan
from ..auth import hash_password, verify_password, create_access_token, get_current_user, require_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class SavePlanRequest(BaseModel):
    destination: str
    total_days: int
    budget_level: str
    plan_data: dict
    request_data: dict | None = None
    rating: int | None = None
    comment: str | None = None


@router.post("/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    if len(req.username) < 2 or len(req.username) > 50:
        raise HTTPException(status_code=400, detail="用户名长度需在2-50字符之间")
    if len(req.password) < 6:
        raise HTTPException(status_code=400, detail="密码长度至少6位")

    existing = db.query(User).filter(
        (User.email == req.email) | (User.username == req.username)
    ).first()
    if existing:
        if existing.email == req.email:
            raise HTTPException(status_code=400, detail="该邮箱已被注册")
        raise HTTPException(status_code=400, detail="该用户名已被使用")

    user = User(
        username=req.username,
        email=req.email,
        hashed_password=hash_password(req.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(data={"sub": user.id})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": user.id, "username": user.username, "email": user.email}
    }


@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="邮箱或密码错误")

    token = create_access_token(data={"sub": user.id})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": user.id, "username": user.username, "email": user.email}
    }


@router.get("/me")
def get_profile(current_user: User = Depends(require_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None
    }


@router.get("/plans")
def get_my_plans(current_user: User = Depends(require_user), db: Session = Depends(get_db)):
    plans = db.query(SavedPlan).filter(
        SavedPlan.user_id == current_user.id
    ).order_by(SavedPlan.created_at.desc()).all()

    return {
        "plans": [
            {
                "id": p.id,
                "destination": p.destination,
                "total_days": p.total_days,
                "budget_level": p.budget_level,
                "plan_data": p.plan_data,
                "rating": p.rating,
                "comment": p.comment,
                "created_at": p.created_at.isoformat() if p.created_at else None
            }
            for p in plans
        ]
    }


@router.post("/plans/save")
def save_plan(
    req: SavePlanRequest,
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db)
):
    saved = SavedPlan(
        user_id=current_user.id,
        destination=req.destination,
        total_days=req.total_days,
        budget_level=req.budget_level,
        plan_data=req.plan_data,
        request_data=req.request_data,
        rating=req.rating,
        comment=req.comment
    )
    db.add(saved)
    db.commit()
    db.refresh(saved)

    return {"message": "计划已保存", "plan_id": saved.id}


@router.delete("/plans/{plan_id}")
def delete_plan(
    plan_id: int,
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db)
):
    plan = db.query(SavedPlan).filter(
        SavedPlan.id == plan_id,
        SavedPlan.user_id == current_user.id
    ).first()
    if not plan:
        raise HTTPException(status_code=404, detail="计划不存在")

    db.delete(plan)
    db.commit()
    return {"message": "计划已删除"}
