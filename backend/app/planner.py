import json
from openai import OpenAI
from .config import get_api_key
from .models import PlanRequest, TripPlan

client = OpenAI(
    api_key=get_api_key(),
    base_url="https://api.deepseek.com"
)

def build_prompt(req: PlanRequest):
    system = """你是一个专业的旅行规划师。必须返回严格的JSON，结构如下：
{
  "destination": "string",
  "total_days": int,
  "budget_level": "string",
  "daily_plans": [
    {
      "day": int,
      "theme": "string",
      "activities": [
        {"time": "HH:MM", "activity": "string", "notes": "string(可为空)"}
      ],
      "meals": [
        {"meal_type": "breakfast|lunch|dinner", "suggestion": "string", "estimated_cost": int}
      ],
      "accommodation_note": "string",
      "daily_budget": int
    }
  ],
  "overall_tips": ["string"]
}
要求：
- 每天安排3-5个活动，时间从09:00到20:00合理分布。
- 餐饮至少提供午餐和晚餐建议，均为当地真实特色。
- 每日预算基于当地消费水平估算（人民币）。
- 只输出JSON，不要有其他解释。
"""
    user = f"目的地：{req.destination}\n天数：{req.days}\n预算等级：{req.budget}\n兴趣偏好：{', '.join(req.interests)}"
    return system, user

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
    # 自动校验并转换为 TripPlan 对象
    return TripPlan(**plan_dict)