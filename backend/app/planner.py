import json
import uuid
from datetime import datetime
from openai import OpenAI
from .config import get_api_key
from .models import PlanRequest, TripPlan

client = OpenAI(
    api_key=get_api_key(),
    base_url="https://api.deepseek.com"
)

# 内存存储历史记录（实际生产环境应使用数据库）
plan_history = {}

def build_prompt(req: PlanRequest):
    # 构建用户提示词
    user_parts = []
    
    # 基础信息
    user_parts.append(f"目的地：{req.destination}")
    user_parts.append(f"天数：{req.days}")
    user_parts.append(f"预算等级：{req.budget}")
    
    # 兴趣偏好
    if req.interests:
        user_parts.append(f"兴趣偏好：{', '.join(req.interests)}")
    
    # 基础信息扩展
    if req.departure_city:
        user_parts.append(f"出发地：{req.departure_city}")
    
    if req.travel_date:
        user_parts.append(f"出行日期：{req.travel_date}")
    
    # 同行人员映射
    companions_map = {
        "alone": "独自旅行",
        "couple": "情侣",
        "family_with_kids": "家庭（有小孩）",
        "family_with_elderly": "家庭（有老人）",
        "friends": "朋友"
    }
    if req.companions and req.companions in companions_map:
        user_parts.append(f"同行人员：{companions_map[req.companions]}")
    
    # 预算细分
    if req.budget_breakdown:
        budget_parts = []
        if req.budget_breakdown.accommodation:
            budget_parts.append(f"住宿¥{req.budget_breakdown.accommodation}/天")
        if req.budget_breakdown.food:
            budget_parts.append(f"餐饮¥{req.budget_breakdown.food}/天")
        if req.budget_breakdown.attractions:
            budget_parts.append(f"门票¥{req.budget_breakdown.attractions}/天")
        if req.budget_breakdown.shopping:
            budget_parts.append(f"购物¥{req.budget_breakdown.shopping}/天")
        if budget_parts:
            user_parts.append(f"每日预算细分：{', '.join(budget_parts)}")
    
    # 偏好与限制
    if req.dietary_restrictions:
        user_parts.append(f"饮食限制：{', '.join(req.dietary_restrictions)}")
    
    # 步行强度映射
    walking_map = {
        "easy": "轻松（＜5k步）",
        "moderate": "适中（5-15k步）",
        "intense": "特种兵（＞15k步）"
    }
    if req.walking_intensity and req.walking_intensity in walking_map:
        user_parts.append(f"步行强度：{walking_map[req.walking_intensity]}")
    
    if req.accommodation_types:
        user_parts.append(f"住宿类型偏好：{', '.join(req.accommodation_types)}")
    
    if req.attraction_types:
        user_parts.append(f"景点类型偏好：{', '.join(req.attraction_types)}")
    
    if req.special_needs:
        user_parts.append(f"特殊需求：{', '.join(req.special_needs)}")
    
    if req.language_preference:
        user_parts.append("需要中文导游/讲解器")
    
    # 时间与节奏
    if req.daily_start_time:
        user_parts.append(f"每日开始时间：{req.daily_start_time}")
    
    if req.daily_end_time:
        user_parts.append(f"每日结束时间：{req.daily_end_time}")
    
    if req.need_lunch_break:
        user_parts.append("需要午休")
    
    # 灵活度映射
    flexibility_map = {
        "strict": "严格按计划",
        "adjustable": "可调整30%",
        "casual": "随意"
    }
    if req.flexibility and req.flexibility in flexibility_map:
        user_parts.append(f"灵活度：{flexibility_map[req.flexibility]}")
    
    user_prompt = "\n".join(user_parts)
    
    # 系统提示词 - 精简版，加快生成速度
    system = """你是一个专业的旅行规划师。请返回JSON格式：
{
  "destination": "目的地",
  "total_days": 天数,
  "budget_level": "预算等级",
  "daily_plans": [
    {
      "day": 1,
      "theme": "当日主题",
      "activities": [
        {"time": "09:00", "activity": "活动名称", "notes": "备注"}
      ],
      "meals": [
        {"meal_type": "lunch", "suggestion": "餐厅推荐", "estimated_cost": 80}
      ],
      "accommodation_note": "住宿建议",
      "daily_budget": 800,
      "transport_guide": "交通方式说明"
    }
  ],
  "overall_tips": ["实用建议1", "建议2"],
  "total_budget": 2400
}
要求：
- 每天3-4个活动，时间合理
- 提供午餐和晚餐建议
- 每日预算基于当地消费水平（人民币）
- 只输出JSON，不要其他解释
"""
    
    return system, user_prompt

def generate_plan(req: PlanRequest) -> TripPlan:
    sys_prompt, user_prompt = build_prompt(req)
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        response_format={"type": "json_object"}
    )
    content = response.choices[0].message.content
    plan_dict = json.loads(content)
    
    # 计算总预算
    if "total_budget" not in plan_dict or plan_dict["total_budget"] is None:
        plan_dict["total_budget"] = sum(day.get("daily_budget", 0) for day in plan_dict.get("daily_plans", []))
    
    # 保存到历史记录
    plan_id = str(uuid.uuid4())
    plan = TripPlan(**plan_dict)
    plan_history[plan_id] = {
        "id": plan_id,
        "request": req,
        "plan": plan,
        "created_at": datetime.now().isoformat()
    }
    
    return plan

def get_history(plan_id: str = None):
    if plan_id:
        return plan_history.get(plan_id)
    return list(plan_history.values())

def add_feedback(plan_id: str, rating: int, comment: str = None):
    if plan_id in plan_history:
        plan_history[plan_id]["rating"] = rating
        plan_history[plan_id]["comment"] = comment
        return True
    return False