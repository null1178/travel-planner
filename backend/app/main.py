from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import PlanRequest, TripPlan
from .planner import generate_plan

app = FastAPI(title="AI 旅行规划师 API")

# 允许前端跨域访问（开发时 Vue 运行在 5173 端口）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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