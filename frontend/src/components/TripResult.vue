<template>
  <div class="trip-result">
    <el-card class="result-header">
      <div class="trip-summary">
        <h2>📍 {{ tripPlan.destination }} - {{ tripPlan.total_days }}天行程</h2>
        <el-tag :type="budgetTagType" size="large">
          {{ budgetLabel }}
        </el-tag>
      </div>
    </el-card>

    <div class="daily-plans">
      <el-card
        v-for="day in tripPlan.daily_plans"
        :key="day.day"
        class="day-card"
        shadow="hover"
      >
        <template #header>
          <div class="day-header">
            <span class="day-title">Day {{ day.day }}</span>
            <el-tag type="info">{{ day.theme }}</el-tag>
            <span class="day-budget">¥{{ day.daily_budget }}/天</span>
          </div>
        </template>

        <div class="day-content">
          <div class="activities">
            <h4>🗓️ 活动安排</h4>
            <el-timeline>
              <el-timeline-item
                v-for="activity in day.activities"
                :key="activity.time"
                :timestamp="activity.time"
                placement="top"
              >
                <el-card>
                  <p class="activity-name">{{ activity.activity }}</p>
                  <p v-if="activity.notes" class="activity-notes">{{ activity.notes }}</p>
                </el-card>
              </el-timeline-item>
            </el-timeline>
          </div>

          <div class="meals">
            <h4>🍽️ 餐饮推荐</h4>
            <div class="meal-list">
              <div
                v-for="meal in day.meals"
                :key="meal.meal_type"
                class="meal-item"
              >
                <span class="meal-type">{{ mealIcon(meal.meal_type) }}</span>
                <span class="meal-suggestion">{{ meal.suggestion }}</span>
                <span class="meal-cost">¥{{ meal.estimated_cost }}</span>
              </div>
            </div>
          </div>

          <div v-if="day.accommodation_note" class="accommodation">
            <h4>🏨 住宿提示</h4>
            <p>{{ day.accommodation_note }}</p>
          </div>
        </div>
      </el-card>
    </div>

    <el-card class="tips-card">
      <template #header>
        <h3>💡 温馨提示</h3>
      </template>
      <el-ul>
        <li v-for="(tip, index) in tripPlan.overall_tips" :key="index">
          {{ tip }}
        </li>
      </el-ul>
    </el-card>

    <div class="actions">
      <el-button size="large" @click="handleReset">重新规划</el-button>
      <el-button type="primary" size="large" @click="handleSave">保存行程</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useTravelStore } from '../stores/travel'
import { ElMessage } from 'element-plus'

const travelStore = useTravelStore()
const tripPlan = computed(() => travelStore.tripPlan!)

const budgetLabel = computed(() => {
  const map: Record<string, string> = {
    economy: '经济',
    comfort: '舒适',
    luxury: '豪华'
  }
  return map[tripPlan.value.budget_level] || tripPlan.value.budget_level
})

const budgetTagType = computed(() => {
  const map: Record<string, string> = {
    economy: 'success',
    comfort: 'warning',
    luxury: 'danger'
  }
  return map[tripPlan.value.budget_level] || 'info'
})

const mealIcon = (mealType: string) => {
  const icons: Record<string, string> = {
    breakfast: '🌅 早餐',
    lunch: '☀️ 午餐',
    dinner: '🌙 晚餐'
  }
  return icons[mealType] || mealType
}

const handleReset = () => {
  travelStore.reset()
}

const handleSave = () => {
  const dataStr = JSON.stringify(tripPlan.value, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(dataBlob)
  const link = document.createElement('a')
  link.href = url
  link.download = `${tripPlan.value.destination}_${tripPlan.value.total_days}天行程.json`
  link.click()
  URL.revokeObjectURL(url)
  ElMessage.success('行程已保存')
}
</script>

<style scoped>
.trip-result {
  max-width: 900px;
  margin: 0 auto;
}

.result-header {
  margin-bottom: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
}

.result-header :deep(.el-card__body) {
  color: white;
}

.trip-summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.trip-summary h2 {
  margin: 0;
  font-size: 24px;
}

.day-card {
  margin-bottom: 20px;
  border-radius: 12px;
}

.day-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.day-title {
  font-size: 18px;
  font-weight: bold;
  color: #409eff;
}

.day-budget {
  margin-left: auto;
  font-weight: bold;
  color: #67c23a;
}

.day-content h4 {
  margin: 16px 0 12px;
  color: #303133;
}

.activity-name {
  margin: 0;
  font-weight: 500;
}

.activity-notes {
  margin: 4px 0 0;
  color: #909399;
  font-size: 13px;
}

.meal-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.meal-item {
  display: flex;
  align-items: center;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 8px;
}

.meal-type {
  min-width: 70px;
  font-weight: 500;
}

.meal-suggestion {
  flex: 1;
}

.meal-cost {
  color: #67c23a;
  font-weight: 500;
}

.accommodation {
  margin-top: 16px;
  padding: 12px;
  background: #fdf6ec;
  border-radius: 8px;
  border-left: 4px solid #e6a23c;
}

.accommodation p {
  margin: 0;
  color: #865a21;
}

.tips-card {
  margin-bottom: 20px;
  background: #f0f9eb;
  border: none;
}

.tips-card h3 {
  margin: 0;
}

.tips-card li {
  margin: 8px 0;
  color: #606266;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 24px;
}
</style>
