<script setup lang="ts">
import { ref, onMounted, watch } from "vue"
import { useRouter } from "vue-router"
import { useAuth } from "../stores/auth"
import { getMyPlans, deletePlan } from "../api"

const router = useRouter()
const { user, isAuthReady } = useAuth()

const plans = ref<any[]>([])
const isLoading = ref(true)
const errorMsg = ref("")
const expandedPlan = ref<number | null>(null)

onMounted(() => {
  if (!user.value && isAuthReady.value) {
    router.push("/login")
    return
  }
  fetchPlans()
})

watch(isAuthReady, (ready) => {
  if (ready && !user.value) {
    router.push("/login")
  }
})

async function fetchPlans() {
  isLoading.value = true
  try {
    const data = await getMyPlans()
    plans.value = data.plans
  } catch (e: any) {
    errorMsg.value = e.message || "加载失败"
  } finally {
    isLoading.value = false
  }
}

async function onDelete(planId: number) {
  if (!confirm("确定要删除这个计划吗？")) return
  try {
    await deletePlan(planId)
    plans.value = plans.value.filter(p => p.id !== planId)
  } catch (e: any) {
    alert(e.message || "删除失败")
  }
}

function toggleExpand(planId: number) {
  expandedPlan.value = expandedPlan.value === planId ? null : planId
}

function formatDate(iso: string) {
  if (!iso) return ""
  return new Date(iso).toLocaleDateString("zh-CN")
}

function exportPlanAsText(plan: any) {
  const p = plan.plan_data
  let text = `旅行计划 - ${p.destination} ${p.total_days}天\n`
  text += `预算等级：${p.budget_level}\n\n`
  p.daily_plans?.forEach((day: any) => {
    text += `=== 第${day.day}天：${day.theme} ===\n`
    day.activities?.forEach((act: any) => text += ` ${act.time} - ${act.activity}${act.notes ? ` (${act.notes})` : ""}\n`)
    day.meals?.forEach((meal: any) => {
      const mn = meal.meal_type === "breakfast" ? "早餐" : meal.meal_type === "lunch" ? "午餐" : "晚餐"
      text += ` ${mn}：${meal.suggestion}（约¥${meal.estimated_cost}）\n`
    })
    text += `每日预算：¥${day.daily_budget}\n\n`
  })
  text += `总预算：¥${p.total_budget}`
  const blob = new Blob([text], { type: "text/plain;charset=utf-8" })
  const a = document.createElement("a")
  a.href = URL.createObjectURL(blob)
  a.download = `${p.destination}_${p.total_days}天行程.txt`
  a.click()
}
</script>

<template>
  <div class="user-center">
    <div class="uc-header">
      <h2>我的旅行计划</h2>
      <router-link to="/" class="btn btn-primary">创建新计划</router-link>
    </div>

    <div v-if="isLoading" class="uc-loading">加载中...</div>

    <div v-else-if="errorMsg" class="auth-error">{{ errorMsg }}</div>

    <div v-else-if="plans.length === 0" class="uc-empty">
      <p>还没有保存任何旅行计划</p>
      <router-link to="/" class="btn btn-submit">去创建第一个计划</router-link>
    </div>

    <div v-else class="plans-list">
      <div v-for="plan in plans" :key="plan.id" class="plan-card">
        <div class="plan-card-header" @click="toggleExpand(plan.id)">
          <div class="plan-card-info">
            <h3>{{ plan.destination }}</h3>
            <span class="plan-meta">{{ plan.total_days }}天 · {{ plan.budget_level }} · {{ formatDate(plan.created_at) }}</span>
            <span v-if="plan.rating" class="plan-rating">评分：{{ plan.rating }}/5</span>
          </div>
          <div class="plan-card-actions">
            <button class="btn-small btn-text" @click.stop="exportPlanAsText(plan)">导出</button>
            <button class="btn-small btn-danger" @click.stop="onDelete(plan.id)">删除</button>
          </div>
        </div>
        <div v-if="expandedPlan === plan.id" class="plan-card-body">
          <div class="result-summary">
            <p class="budget-badge">预算等级：{{ plan.plan_data.budget_level }}</p>
            <p class="total-budget">总预算：¥{{ plan.plan_data.total_budget }}</p>
          </div>
          <div class="daily-plans">
            <div v-for="day in plan.plan_data.daily_plans" :key="day.day" class="daily-plan">
              <div class="day-header">
                <h3>第{{ day.day }}天：{{ day.theme }}</h3>
                <span class="daily-budget">¥{{ day.daily_budget }}</span>
              </div>
              <div class="section">
                <h4>活动安排</h4>
                <div class="activities">
                  <div v-for="(act, idx) in day.activities" :key="idx" class="activity">
                    <span class="time">{{ act.time }}</span>
                    <span class="activity-name">{{ act.activity }}</span>
                  </div>
                </div>
              </div>
              <div class="section">
                <h4>餐饮推荐</h4>
                <div class="meals">
                  <div v-for="(meal, idx) in day.meals" :key="idx" class="meal">
                    <span class="meal-type">{{ meal.meal_type === "breakfast" ? "早餐" : meal.meal_type === "lunch" ? "午餐" : "晚餐" }}</span>
                    <span class="meal-suggestion">{{ meal.suggestion }}</span>
                    <span class="meal-cost">约¥{{ meal.estimated_cost }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
