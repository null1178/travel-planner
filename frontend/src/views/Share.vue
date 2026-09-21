<script setup lang="ts">
import { ref, onMounted, computed } from "vue"
import { useRoute } from "vue-router"
import { getShare } from "../api"
import MapView from "../components/MapView.vue"

const route = useRoute()
const token = route.params.token as string

const planData = ref<any>(null)
const loading = ref(true)
const error = ref("")
const destination = ref("")
const totalDays = ref(0)

const transportModeIcons: Record<string, string> = {
  high_speed_rail: "🚄",
  flight: "✈️",
  normal_train: "🚂",
  bus: "🚌",
  self_drive: "🚗"
}

const departureCity = computed(() => {
  if (planData.value?.transportation?.[0]?.departure_station)
    return planData.value.transportation[0].departure_station
  return "出发地"
})

onMounted(async () => {
  try {
    const data = await getShare(token)
    planData.value = data.plan_data
    destination.value = data.destination
    totalDays.value = data.total_days
  } catch (e: any) {
    error.value = "分享链接不存在或已失效"
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div>
    <header class="header">
      <h1>AI 旅行规划师</h1>
      <p>分享的旅程</p>
    </header>

    <main class="main-content">
      <div v-if="loading" class="loading-overlay">
        <div class="loading-spinner"></div>
        <p class="loading-text">加载中...</p>
      </div>

      <div v-else-if="error" class="result-container">
        <div class="result-summary">
          <h2>😕 {{ error }}</h2>
        </div>
      </div>

      <div v-else class="result-container">
        <div class="result-summary">
          <h2>{{ destination }} {{ totalDays }}天旅行计划</h2>
          <p class="budget-badge">预算等级：{{ planData.budget_level }}</p>
          <p class="total-budget">总预算：¥{{ planData.total_budget }}</p>
        </div>

        <div style="padding: 0 2rem">
          <MapView
            v-if="planData.departure_coords && planData.destination_coords"
            :departureCoords="planData.departure_coords"
            :destinationCoords="planData.destination_coords"
            :departureLabel="departureCity"
            :destinationLabel="destination"
          />
        </div>

        <!-- Transportation -->
        <div v-if="planData.transportation && planData.transportation.length > 0" class="transport-section">
          <h3>🚅 交通推荐</h3>
          <div class="transport-cards">
            <div v-for="(opt, idx) in planData.transportation" :key="idx" class="transport-card">
              <div class="tc-header">
                <span class="tc-icon">{{ transportModeIcons[opt.mode] || "🚄" }}</span>
                <span class="tc-mode">{{ opt.mode_label }}</span>
                <span class="tc-route">{{ opt.route }}</span>
              </div>
              <div class="tc-body">
                <div class="tc-stations">
                  <div class="tc-station">
                    <span class="tc-label">出发</span>
                    <span class="tc-station-name">{{ opt.departure_station }}</span>
                    <span class="tc-time">{{ opt.departure_time }}</span>
                  </div>
                  <div class="tc-arrow">→</div>
                  <div class="tc-station">
                    <span class="tc-label">到达</span>
                    <span class="tc-station-name">{{ opt.arrival_station }}</span>
                    <span class="tc-time">{{ opt.arrival_time }}</span>
                  </div>
                </div>
                <div class="tc-meta">
                  <span>⏱ {{ opt.duration }}</span>
                  <span>💰 {{ opt.estimated_price }}</span>
                </div>
                <div v-if="opt.tips" class="tc-tips">💡 {{ opt.tips }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Return transportation -->
        <div v-if="planData.return_transportation && planData.return_transportation.length > 0" class="transport-section">
          <h3>🔙 回程交通推荐</h3>
          <div class="transport-cards">
            <div v-for="(opt, idx) in planData.return_transportation" :key="idx" class="transport-card">
              <div class="tc-header">
                <span class="tc-icon">{{ transportModeIcons[opt.mode] || "🚄" }}</span>
                <span class="tc-mode">{{ opt.mode_label }}</span>
                <span class="tc-route">{{ opt.route }}</span>
              </div>
              <div class="tc-body">
                <div class="tc-stations">
                  <div class="tc-station">
                    <span class="tc-label">出发</span>
                    <span class="tc-station-name">{{ opt.departure_station }}</span>
                    <span class="tc-time">{{ opt.departure_time }}</span>
                  </div>
                  <div class="tc-arrow">→</div>
                  <div class="tc-station">
                    <span class="tc-label">到达</span>
                    <span class="tc-station-name">{{ opt.arrival_station }}</span>
                    <span class="tc-time">{{ opt.arrival_time }}</span>
                  </div>
                </div>
                <div class="tc-meta">
                  <span>⏱ {{ opt.duration }}</span>
                  <span>💰 {{ opt.estimated_price }}</span>
                </div>
                <div v-if="opt.tips" class="tc-tips">💡 {{ opt.tips }}</div>
              </div>
            </div>
          </div>
        </div>

        <div class="daily-plans">
          <div v-for="day in planData.daily_plans" :key="day.day" class="daily-plan">
            <div class="day-header">
              <h3>第{{ day.day }}天：{{ day.theme }}</h3>
              <span class="daily-budget">¥{{ day.daily_budget }}</span>
            </div>
            <div v-if="day.weather_alert" class="alert alert-weather">⚠️ {{ day.weather_alert }}</div>
            <div v-if="day.transport_guide" class="info-card transport">
              <h4>🚫 交通指引</h4><p>{{ day.transport_guide }}</p>
            </div>
            <div class="section">
              <h4>📮 活动安排</h4>
              <div class="activities">
                <div v-for="(act, index) in day.activities" :key="index" class="activity">
                  <span class="time">{{ act.time }}</span>
                  <span class="activity-name">{{ act.activity }}</span>
                  <span v-if="act.notes" class="notes">{{ act.notes }}</span>
                </div>
              </div>
            </div>
            <div v-if="day.walking_estimate" class="info-card walking">
              <h4>🚶 步行预估</h4><p>{{ day.walking_estimate }}</p>
            </div>
            <div class="section">
              <h4>🍽️ 餐饮推荐</h4>
              <div class="meals">
                <div v-for="(meal, index) in day.meals" :key="index" class="meal">
                  <span class="meal-type">{{ meal.meal_type === "breakfast" ? "早餐" : meal.meal_type === "lunch" ? "午餐" : "晚餐" }}</span>
                  <span class="meal-suggestion">{{ meal.suggestion }}</span>
                  <span class="meal-cost">约¥{{ meal.estimated_cost }}</span>
                </div>
              </div>
            </div>
            <div v-if="day.accommodation_note" class="info-card accommodation">
              <h4>🏣 住宿提示</h4><p>{{ day.accommodation_note }}</p>
            </div>
          </div>
        </div>

        <div v-if="planData.overall_tips && planData.overall_tips.length > 0" class="section">
          <h3>💰 整体建议</h3>
          <ul class="tips-list"><li v-for="(tip, idx) in planData.overall_tips" :key="idx">{{ tip }}</li></ul>
        </div>
      </div>
    </main>

    <footer class="footer">
      <p>AI 旅行规划师 - 让旅行更简单</p>
    </footer>
  </div>
</template>
