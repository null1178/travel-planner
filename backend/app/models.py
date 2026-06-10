from pydantic import BaseModel, Field
from typing import List, Optional

CompanionType = str

class BudgetBreakdown(BaseModel):
    accommodation: Optional[int] = None
    food: Optional[int] = None
    attractions: Optional[int] = None
    shopping: Optional[int] = None

class PlanRequest(BaseModel):
    destination: str
    days: int
    budget: str
    interests: Optional[List[str]] = []
    departure_city: Optional[str] = None
    travel_date: Optional[str] = None
    companions: Optional[CompanionType] = None
    budget_breakdown: Optional[BudgetBreakdown] = None
    dietary_restrictions: Optional[List[str]] = None
    walking_intensity: Optional[str] = None
    accommodation_types: Optional[List[str]] = None
    attraction_types: Optional[List[str]] = None
    special_needs: Optional[List[str]] = None
    language_preference: Optional[bool] = None
    daily_start_time: Optional[str] = None
    daily_end_time: Optional[str] = None
    need_lunch_break: Optional[bool] = None
    flexibility: Optional[str] = None

class Activity(BaseModel):
    time: str
    activity: str
    notes: Optional[str] = None

class Meal(BaseModel):
    meal_type: str
    suggestion: str
    estimated_cost: int

class BudgetItem(BaseModel):
    category: str
    amount: int
    description: Optional[str] = None

class DailyPlan(BaseModel):
    day: int
    theme: str
    activities: List[Activity]
    meals: List[Meal]
    accommodation_note: Optional[str] = None
    daily_budget: int
    transport_guide: Optional[str] = None
    attraction_tips: Optional[List[str]] = None
    weather_alert: Optional[str] = None
    budget_details: Optional[List[BudgetItem]] = None
    walking_estimate: Optional[str] = None
    alternative_plan: Optional[str] = None
    map_link: Optional[str] = None

class TransportOption(BaseModel):
    mode: str
    mode_label: str
    route: str
    departure_station: str
    arrival_station: str
    departure_time: str
    arrival_time: str
    duration: str
    estimated_price: str
    tips: Optional[str] = None

class TripPlan(BaseModel):
    destination: str
    total_days: int
    budget_level: str
    daily_plans: List[DailyPlan]
    overall_tips: List[str]
    packing_list: Optional[List[str]] = None
    cultural_tips: Optional[List[str]] = None
    total_budget: Optional[int] = None
    departure_coords: Optional[List[float]] = None
    destination_coords: Optional[List[float]] = None
    transportation: Optional[List[TransportOption]] = None
    return_transportation: Optional[List[TransportOption]] = None

class PlanHistory(BaseModel):
    id: str
    request: PlanRequest
    plan: TripPlan
    created_at: str
    rating: Optional[int] = None

class FeedbackRequest(BaseModel):
    plan_id: str
    rating: int
    comment: Optional[str] = None
