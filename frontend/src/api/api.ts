import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
})

export interface PlanRequest {
  destination: string
  days: number
  budget: string
  interests: string[]
}

export interface Activity {
  time: string
  activity: string
  notes: string | null
}

export interface Meal {
  meal_type: string
  suggestion: string
  estimated_cost: number
}

export interface DailyPlan {
  day: number
  theme: string
  activities: Activity[]
  meals: Meal[]
  accommodation_note: string | null
  daily_budget: number
}

export interface TripPlan {
  destination: string
  total_days: number
  budget_level: string
  daily_plans: DailyPlan[]
  overall_tips: string[]
}

export const generateTripPlan = async (request: PlanRequest): Promise<TripPlan> => {
  const response = await apiClient.post<TripPlan>('/api/generate', request)
  return response.data
}
