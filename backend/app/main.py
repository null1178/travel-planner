from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from .models import PlanRequest, TripPlan, FeedbackRequest
from .planner import generate_plan, get_history, add_feedback
from .database import init_db
from .routers import auth_router
from .auth import get_current_user
from .user_models import User

app = FastAPI(title="AI 旅行规划师 API")

# Allow frontend cross-domain access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
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
