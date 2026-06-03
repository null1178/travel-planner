from pydantic import BaseModel
from typing import List, Optional

# 用户请求体
class PlanRequest(BaseModel):
    destination: str
    days: int
    budget: str   # "economy", "comfort", "luxury"
    interests: List[str]

# 每日活动
class Activity(BaseModel):
    time: str
    activity: str
    notes: Optional[str] = None

# 餐饮推荐
class Meal(BaseModel):
    meal_type: str   # "breakfast", "lunch", "dinner"
    suggestion: str
    estimated_cost: int

# 每日计划
class DailyPlan(BaseModel):
    day: int
    theme: str
    activities: List[Activity]
    meals: List[Meal]
    accommodation_note: Optional[str] = None
    daily_budget: int

# 完整行程响应
class TripPlan(BaseModel):
    destination: str
    total_days: int
    budget_level: str
    daily_plans: List[DailyPlan]
    overall_tips: List[str]