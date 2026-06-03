import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { TripPlan, PlanRequest } from '../api/api'
import { generateTripPlan } from '../api/api'

export const useTravelStore = defineStore('travel', () => {
  const tripPlan = ref<TripPlan | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const generatePlan = async (request: PlanRequest) => {
    loading.value = true
    error.value = null
    tripPlan.value = null

    try {
      tripPlan.value = await generateTripPlan(request)
    } catch (err: any) {
      error.value = err.response?.data?.detail || err.message || '生成行程失败，请稍后重试'
    } finally {
      loading.value = false
    }
  }

  const reset = () => {
    tripPlan.value = null
    error.value = null
    loading.value = false
  }

  return {
    tripPlan,
    loading,
    error,
    generatePlan,
    reset
  }
})
