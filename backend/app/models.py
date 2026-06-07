from pydantic import BaseModel, Field
from typing import List, Optional

# 同行人员类型
CompanionType = str  # "alone" | "couple" | "family_with_kids" | "family_with_elderly" | "friends"

# 预算细分
class BudgetBreakdown(BaseModel):
    accommodation: Optional[int] = None  # 住宿预算/天
    food: Optional[int] = None  # 餐饮预算/天
    attractions: Optional[int] = None  # 门票预算/天
    shopping: Optional[int] = None  # 购物预算/天

# 用户请求体 - 扩展版
class PlanRequest(BaseModel):
    destination: str
    days: int
    budget: str  # "economy", "comfort", "luxury"
    interests: Optional[List[str]] = []  # 兴趣偏好，可选
    
    # 基础信息扩展
    departure_city: Optional[str] = None  # 出发地
    travel_date: Optional[str] = None  # 出行日期 YYYY-MM-DD
    companions: Optional[CompanionType] = None  # 同行人员
    budget_breakdown: Optional[BudgetBreakdown] = None  # 每日预算细分
    
    # 偏好与限制
    dietary_restrictions: Optional[List[str]] = None  # 饮食限制：素食/清真/海鲜过敏/无辣不欢
    walking_intensity: Optional[str] = None  # 步行强度：easy/moderate/intense
    accommodation_types: Optional[List[str]] = None  # 住宿类型：酒店/民宿/青旅/露营
    attraction_types: Optional[List[str]] = None  # 景点类型：网红打卡/博物馆/自然风光/主题乐园等
    special_needs: Optional[List[str]] = None  # 特殊需求：轮椅友好/婴儿车通道/无障碍设施
    language_preference: Optional[bool] = None  # 是否需要中文导游
    
    # 时间与节奏
    daily_start_time: Optional[str] = None  # 每日开始时间
    daily_end_time: Optional[str] = None  # 每日结束时间
    need_lunch_break: Optional[bool] = None  # 是否需要午休
    flexibility: Optional[str] = None  # 灵活度：strict/adjustable/casual

# 每日活动
class Activity(BaseModel):
    time: str
    activity: str
    notes: Optional[str] = None

# 餐饮推荐
class Meal(BaseModel):
    meal_type: str  # "breakfast", "lunch", "dinner"
    suggestion: str
    estimated_cost: int

# 预算明细
class BudgetItem(BaseModel):
    category: str  # "accommodation", "food", "attractions", "transport", "shopping"
    amount: int
    description: Optional[str] = None

# 每日计划 - 扩展版
class DailyPlan(BaseModel):
    day: int
    theme: str
    activities: List[Activity]
    meals: List[Meal]
    accommodation_note: Optional[str] = None
    daily_budget: int
    
    # 扩展输出字段
    transport_guide: Optional[str] = None  # 交通指引
    attraction_tips: Optional[List[str]] = None  # 景点小贴士
    weather_alert: Optional[str] = None  # 天气提醒
    budget_details: Optional[List[BudgetItem]] = None  # 预算明细表
    walking_estimate: Optional[str] = None  # 步行/运动量预估
    alternative_plan: Optional[str] = None  # 替代方案
    map_link: Optional[str] = None  # 地图链接

# 完整行程响应 - 扩展版
class TripPlan(BaseModel):
    destination: str
    total_days: int
    budget_level: str
    daily_plans: List[DailyPlan]
    overall_tips: List[str]
    
    # 扩展输出字段
    packing_list: Optional[List[str]] = None  # 打包清单
    cultural_tips: Optional[List[str]] = None  # 文化礼仪提示
    total_budget: Optional[int] = None  # 总预算

# 历史记录模型
class PlanHistory(BaseModel):
    id: str
    request: PlanRequest
    plan: TripPlan
    created_at: str
    rating: Optional[int] = None  # 1-5分评价

# 反馈请求
class FeedbackRequest(BaseModel):
    plan_id: str
    rating: int  # 1-5
    comment: Optional[str] = None