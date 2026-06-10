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

plan_history = {}

def build_prompt(req: PlanRequest):
    user_parts = []

    user_parts.append(f"目的地：{req.destination}")
    user_parts.append(f"天数：{req.days}")
    user_parts.append(f"预算等级：{req.budget}")

    if req.interests:
        user_parts.append(f"兴趣爱好：{', '.join(req.interests)}")

    if req.departure_city:
        user_parts.append(f"出发地：{req.departure_city}")

    if req.travel_date:
        user_parts.append(f"出行日期：{req.travel_date}")

    companions_map = {
        "alone": "独自旅行",
        "couple": "情侣",
        "family_with_kids": "家庭（有小孩）",
        "family_with_elderly": "家庭（有老人）",
        "friends": "朋友"
    }
    if req.companions and req.companions in companions_map:
        user_parts.append(f"同行人员：{companions_map[req.companions]}")

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

    if req.dietary_restrictions:
        user_parts.append(f"饮食限制：{', '.join(req.dietary_restrictions)}")

    walking_map = {
        "easy": "轻松（<5k步）",
        "moderate": "适中（5-15k步）",
        "intense": "特种兵（>15k步）"
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

    if req.daily_start_time:
        user_parts.append(f"每日开始时间：{req.daily_start_time}")

    if req.daily_end_time:
        user_parts.append(f"每日结束时间：{req.daily_end_time}")

    if req.need_lunch_break:
        user_parts.append("需要午休")

    flexibility_map = {
        "strict": "严格按计划",
        "adjustable": "可调整30%",
        "casual": "随意"
    }
    if req.flexibility and req.flexibility in flexibility_map:
        user_parts.append(f"灵活度：{flexibility_map[req.flexibility]}")

    user_prompt = "\n".join(user_parts)

    transport_section = ""
    if req.departure_city:
        transport_section = f"""
- "transportation": 从{req.departure_city}到{req.destination}的去程交通推荐数组
- "return_transportation": 从{req.destination}返回{req.departure_city}的回程交通推荐数组
  每项包含：
    mode（类型英文：high_speed_rail/flight/normal_train/bus/self_drive）,
    mode_label（中文如"高铁"/"飞机"）,
    route（车次/航班号如"G123"）,
    departure_station, arrival_station, departure_time, arrival_time,
    duration（如"约4小时30分"）,
    estimated_price（如"二等座 ¥550"或"经济舱 ¥800-1200"）,
    tips（订票建议）
  去程和回程各提供2-3种推荐方式
- "departure_coords": [{req.departure_city}的经度, 纬度]（数字数组）
- "destination_coords": [{req.destination}的经度, 纬度]（数字数组）
"""

    system = f"""你是一个专业的旅行规划师。请返回JSON格式：
{{
  "destination": "目的地",
  "total_days": 天数,
  "budget_level": "预算等级",
  "daily_plans": [
    {{
      "day": 1,
      "theme": "当日主题",
      "activities": [
        {{"time": "09:00", "activity": "活动名称", "notes": "备注"}}
      ],
      "meals": [
        {{"meal_type": "lunch", "suggestion": "餐厅推荐", "estimated_cost": 80}}
      ],
      "accommodation_note": "住宿建议",
      "daily_budget": 800,
      "transport_guide": "交通方式说明"
    }}
  ],
  "overall_tips": ["实用建议1", "建议2"],
  "total_budget": 2400{transport_section}
}}
要求：
- 每天3-4个活动，时间合理
- 提供午餐和晚餐建议
- 每日预算基于当地消费水平（人民币）
- 只输出JSON，不要其他解释"""

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

    if "total_budget" not in plan_dict or plan_dict["total_budget"] is None:
        plan_dict["total_budget"] = sum(day.get("daily_budget", 0) for day in plan_dict.get("daily_plans", []))

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
