from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid
from .models import PlanRequest, TripPlan, FeedbackRequest
from .planner import generate_plan, get_history, add_feedback
from .database import init_db, get_db
from .routers import auth_router
from .auth import get_current_user
from .user_models import User, ShareLink
from .weather import get_weather, format_weather_alert

app = FastAPI(title="AI 旅行规划师 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"message": "旅行规划师后端已启动"}


@app.post("/api/generate", response_model=TripPlan)
async def generate_trip(request: PlanRequest):
    try:
        plan = generate_plan(request)
        return plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history")
async def get_plan_history():
    try:
        history = get_history()
        return {"plans": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history/{plan_id}")
async def get_plan_by_id(plan_id: str):
    try:
        plan_data = get_history(plan_id)
        if not plan_data:
            raise HTTPException(status_code=404, detail="计划不存在")
        return plan_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    try:
        success = add_feedback(feedback.plan_id, feedback.rating, feedback.comment)
        if not success:
            raise HTTPException(status_code=404, detail="计划不存在")
        return {"message": "反馈提交成功"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----- Weather -----


@app.get("/api/weather")
def weather(city: str):
    try:
        data = get_weather(city)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----- Share -----

class ShareRequest(BaseModel):
    plan_data: dict
    destination: str
    total_days: int


@app.post("/api/share")
def create_share(req: ShareRequest, db: Session = Depends(get_db)):
    token = uuid.uuid4().hex
    share = ShareLink(
        token=token,
        plan_data=req.plan_data,
        destination=req.destination,
        total_days=req.total_days,
    )
    db.add(share)
    db.commit()
    db.refresh(share)
    return {"token": token, "share_url": f"/share/{token}"}


@app.get("/api/share/{token}")
def get_share(token: str, db: Session = Depends(get_db)):
    share = db.query(ShareLink).filter(
        ShareLink.token == token,
        ShareLink.is_active == True
    ).first()
    if not share:
        raise HTTPException(status_code=404, detail="分享链接不存在或已失效")
    return {
        "destination": share.destination,
        "total_days": share.total_days,
        "plan_data": share.plan_data,
        "created_at": share.created_at.isoformat() if share.created_at else None,
    }
