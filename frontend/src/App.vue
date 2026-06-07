<script setup lang="ts">
import { ref, reactive } from 'vue'

interface FormData {
  destination: string
  days: number
  budget: string
  interests: string[]
  departureCity: string
  travelDate: string
  companions: string
  budgetBreakdown: {
    accommodation: string
    food: string
    attractions: string
    shopping: string
  }
  dietaryRestrictions: string[]
  walkingIntensity: string
  accommodationTypes: string[]
  attractionTypes: string[]
  specialNeeds: string[]
  languagePreference: boolean
  dailyStartTime: string
  dailyEndTime: string
  needLunchBreak: boolean
  flexibility: string
}

const formData = reactive<FormData>({
  destination: '',
  days: 3,
  budget: 'comfort',
  interests: [],
  departureCity: '',
  travelDate: '',
  companions: '',
  budgetBreakdown: {
    accommodation: '',
    food: '',
    attractions: '',
    shopping: ''
  },
  dietaryRestrictions: [],
  walkingIntensity: '',
  accommodationTypes: [],
  attractionTypes: [],
  specialNeeds: [],
  languagePreference: false,
  dailyStartTime: '09:00',
  dailyEndTime: '20:00',
  needLunchBreak: false,
  flexibility: 'adjustable'
})

const budgetOptions = [
  { value: 'economy', label: '经济型' },
  { value: 'comfort', label: '舒适型' },
  { value: 'luxury', label: '豪华型' }
]

const companionsOptions = [
  { value: 'alone', label: '独自旅行' },
  { value: 'couple', label: '情侣' },
  { value: 'family_with_kids', label: '家庭（有小孩）' },
  { value: 'family_with_elderly', label: '家庭（有老人）' },
  { value: 'friends', label: '朋友' }
]

const interestOptions = [
  '历史文化', '自然风光', '美食探索', '购物休闲',
  '主题乐园', '网红打卡', '博物馆', '户外运动',
  '温泉度假', '海岛沙滩', '古镇风情', '城市观光'
]

const dietaryOptions = [
  { value: 'vegetarian', label: '素食' },
  { value: 'halal', label: '清真' },
  { value: 'seafood_allergy', label: '海鲜过敏' },
  { value: 'love_spicy', label: '无辣不欢' }
]

const walkingOptions = [
  { value: 'easy', label: '轻松（＜5k步）' },
  { value: 'moderate', label: '适中（5-15k步）' },
  { value: 'intense', label: '特种兵（＞15k步）' }
]

const accommodationOptions = [
  { value: 'hotel', label: '酒店' },
  { value: 'bnb', label: '民宿' },
  { value: 'hostel', label: '青旅' },
  { value: 'camping', label: '露营' }
]

const attractionTypeOptions = [
  '网红打卡', '博物馆', '自然风光', '主题乐园',
  '历史古迹', '美食街区', '购物商圈', '文化体验',
  '户外徒步', '温泉养生'
]

const specialNeedsOptions = [
  { value: 'wheelchair', label: '轮椅友好' },
  { value: 'stroller', label: '婴儿车通道' },
  { value: 'accessible', label: '无障碍设施' }
]

const startTimeOptions = ['06:00', '07:00', '08:00', '09:00', '10:00']
const endTimeOptions = ['18:00', '20:00', '22:00', '不限']

const flexibilityOptions = [
  { value: 'strict', label: '严格按计划' },
  { value: 'adjustable', label: '可调整30%' },
  { value: 'casual', label: '随意' }
]

const isSubmitting = ref(false)
const planResult: any = ref(null)
const activeTab = ref('basic')
const tabs = [
  { id: 'basic', label: '基础信息' },
  { id: 'preferences', label: '偏好限制' },
  { id: 'schedule', label: '时间节奏' }
]

function toggleMultiple(option: string, list: string[]) {
  const index = list.indexOf(option)
  if (index > -1) {
    list.splice(index, 1)
  } else {
    list.push(option)
  }
}

function goToPrevTab() {
  const currentIndex = tabs.findIndex(t => t.id === activeTab.value)
  if (currentIndex > 0) {
    activeTab.value = tabs[currentIndex - 1].id
  }
}

function goToNextTab() {
  const currentIndex = tabs.findIndex(t => t.id === activeTab.value)
  if (currentIndex < tabs.length - 1) {
    activeTab.value = tabs[currentIndex + 1].id
  }
}

async function submitForm() {
  if (!formData.destination.trim()) {
    alert('请输入目的地')
    return
  }
  
  isSubmitting.value = true
  
  try {
    const requestData: any = {
      destination: formData.destination,
      days: formData.days,
      budget: formData.budget,
      interests: formData.interests.length > 0 ? formData.interests : []
    }
    
    if (formData.departureCity) {
      requestData.departure_city = formData.departureCity
    }
    if (formData.travelDate) {
      requestData.travel_date = formData.travelDate
    }
    if (formData.companions) {
      requestData.companions = formData.companions
    }
    
    if (formData.budgetBreakdown.accommodation || formData.budgetBreakdown.food ||
        formData.budgetBreakdown.attractions || formData.budgetBreakdown.shopping) {
      requestData.budget_breakdown = {}
      if (formData.budgetBreakdown.accommodation) {
        requestData.budget_breakdown.accommodation = parseInt(formData.budgetBreakdown.accommodation)
      }
      if (formData.budgetBreakdown.food) {
        requestData.budget_breakdown.food = parseInt(formData.budgetBreakdown.food)
      }
      if (formData.budgetBreakdown.attractions) {
        requestData.budget_breakdown.attractions = parseInt(formData.budgetBreakdown.attractions)
      }
      if (formData.budgetBreakdown.shopping) {
        requestData.budget_breakdown.shopping = parseInt(formData.budgetBreakdown.shopping)
      }
    }
    
    if (formData.dietaryRestrictions.length > 0) {
      requestData.dietary_restrictions = formData.dietaryRestrictions
    }
    if (formData.walkingIntensity) {
      requestData.walking_intensity = formData.walkingIntensity
    }
    if (formData.accommodationTypes.length > 0) {
      requestData.accommodation_types = formData.accommodationTypes
    }
    if (formData.attractionTypes.length > 0) {
      requestData.attraction_types = formData.attractionTypes
    }
    if (formData.specialNeeds.length > 0) {
      requestData.special_needs = formData.specialNeeds
    }
    if (formData.languagePreference) {
      requestData.language_preference = formData.languagePreference
    }
    
    requestData.daily_start_time = formData.dailyStartTime
    requestData.daily_end_time = formData.dailyEndTime
    requestData.need_lunch_break = formData.needLunchBreak
    requestData.flexibility = formData.flexibility
    
    const response = await fetch('http://localhost:8000/api/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestData)
    })
    
    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(`生成失败: ${response.status} - ${errorText}`)
    }
    
    planResult.value = await response.json()
  } catch (error) {
    console.error('Error:', error)
    alert(`生成行程时发生错误: ${error instanceof Error ? error.message : String(error)}`)
  } finally {
    isSubmitting.value = false
  }
}

function formatBudgetDetails(details: any[]) {
  const categoryMap: Record<string, string> = {
    accommodation: '住宿',
    food: '餐饮',
    attractions: '门票',
    transport: '交通',
    shopping: '购物'
  }
  return details?.map(item => ({
    ...item,
    category: categoryMap[item.category] || item.category
  })) || []
}

function exportAsText() {
  if (!planResult.value) return
  
  let text = `旅行计划 - ${planResult.value.destination} ${planResult.value.total_days}天\n`
  text += `预算等级：${planResult.value.budget_level}\n\n`
  
  planResult.value.daily_plans.forEach((day: any) => {
    text += `=== 第${day.day}天：${day.theme} ===\n`
    text += `活动安排：\n`
    day.activities.forEach((act: any) => {
      text += ` ${act.time} - ${act.activity}${act.notes ? ` (${act.notes})` : ''}\n`
    })
    text += `餐饮推荐：\n`
    day.meals.forEach((meal: any) => {
      text += ` ${meal.meal_type === 'breakfast' ? '早餐' : meal.meal_type === 'lunch' ? '午餐' : '晚餐'}：${meal.suggestion}（约¥${meal.estimated_cost}）\n`
    })
    if (day.transport_guide) text += `交通指引：${day.transport_guide}\n`
    if (day.walking_estimate) text += `步行预估：${day.walking_estimate}\n`
    if (day.weather_alert) text += `天气提醒：${day.weather_alert}\n`
    text += `每日预算：¥${day.daily_budget}\n\n`
  })
  
  if (planResult.value.packing_list) {
    text += `=== 打包清单 ===\n`
    planResult.value.packing_list.forEach((item: string) => {
      text += ` • ${item}\n`
    })
  }
  
  if (planResult.value.cultural_tips) {
    text += `\n=== 文化礼仪提示 ===\n`
    planResult.value.cultural_tips.forEach((tip: string) => {
      text += ` • ${tip}\n`
    })
  }
  
  text += `\n总预算：¥${planResult.value.total_budget}`
  
  const blob = new Blob([text], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${planResult.value.destination}_${planResult.value.total_days}天行程.txt`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

function exportAsJSON() {
  if (!planResult.value) return
  
  const jsonData = JSON.stringify(planResult.value, null, 2)
  const blob = new Blob([jsonData], { type: 'application/json;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${planResult.value.destination}_${planResult.value.total_days}天行程.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

function exportAsHTML() {
  if (!planResult.value) return
  
  const plan = planResult.value
  let html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${plan.destination}${plan.total_days}天旅行计划</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; padding: 2rem; }
    .container { max-width: 900px; margin: 0 auto; background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }
    .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; text-align: center; }
    .header h1 { font-size: 2rem; margin-bottom: 0.5rem; }
    .header .budget { display: inline-block; padding: 0.4rem 1rem; background: rgba(255,255,255,0.2); border-radius: 20px; margin: 0.3rem; }
    .content { padding: 2rem; }
    .day { background: #f8f9fa; border-radius: 15px; padding: 1.5rem; margin-bottom: 1.5rem; }
    .day h2 { color: #667eea; margin-bottom: 1rem; font-size: 1.3rem; }
    .section { margin-bottom: 1rem; }
    .section h3 { color: #343a40; margin-bottom: 0.5rem; font-size: 1rem; }
    .section ul { list-style: none; padding-left: 0; }
    .section li { padding: 0.5rem 0; border-bottom: 1px solid #e9ecef; }
    .section li:last-child { border-bottom: none; }
    .time { color: #667eea; font-weight: 600; margin-right: 0.5rem; }
    .meal { display: flex; justify-content: space-between; padding: 0.5rem 0; }
    .meal-type { font-weight: 600; color: #667eea; }
    .meal-cost { color: #11998e; font-weight: 600; }
    .tips { background: #fff3cd; padding: 1rem; border-radius: 10px; margin-top: 1rem; }
    .tips h3 { color: #856404; }
    .footer { text-align: center; padding: 2rem; color: #6c757d; font-size: 0.9rem; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>${plan.destination} ${plan.total_days}天旅行计划</h1>
      <span class="budget">💰 预算等级：${plan.budget_level}</span>
      <span class="budget">💵 总预算：¥${plan.total_budget}</span>
    </div>
    <div class="content">
`

  plan.daily_plans.forEach((day: any) => {
    html += `
      <div class="day">
        <h2>📅 第${day.day}天：${day.theme}</h2>
        <div class="section">
          <h3>🚶 活动安排</h3>
          <ul>
`
    day.activities.forEach((act: any) => {
      html += `            <li><span class="time">${act.time}</span> ${act.activity}${act.notes ? ` - ${act.notes}` : ''}</li>\n`
    })
    html += `          </ul>
        </div>
        <div class="section">
          <h3>🍽️ 餐饮推荐</h3>
`
    day.meals.forEach((meal: any) => {
      const mealName = meal.meal_type === 'breakfast' ? '早餐' : meal.meal_type === 'lunch' ? '午餐' : '晚餐'
      html += `          <div class="meal"><span class="meal-type">${mealName}</span><span>${meal.suggestion}</span><span class="meal-cost">¥${meal.estimated_cost}</span></div>\n`
    })
    html += `        </div>
`
    if (day.transport_guide) {
      html += `        <div class="section"><h3>🚗 交通指引</h3><p>${day.transport_guide}</p></div>\n`
    }
    if (day.daily_budget) {
      html += `        <div class="section"><h3>💰 每日预算</h3><p>¥${day.daily_budget}</p></div>\n`
    }
    html += `      </div>\n`
  })

  if (plan.overall_tips && plan.overall_tips.length > 0) {
    html += `
      <div class="tips">
        <h3>💡 实用建议</h3>
        <ul>
`
    plan.overall_tips.forEach((tip: string) => {
      html += `          <li>${tip}</li>\n`
    })
    html += `        </ul>
      </div>
`
  }

  html += `
    </div>
    <div class="footer">
      <p>由 AI 旅行规划师生成 | ${new Date().toLocaleDateString('zh-CN')}</p>
    </div>
  </div>
</body>
</html>`

  const blob = new Blob([html], { type: 'text/html;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${plan.destination}_${plan.total_days}天行程.html`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

function backToForm() {
  planResult.value = null
}
</script>

<template>
  <div class="app">
    <header class="header">
      <h1>AI 旅行规划师</h1>
      <p>智能定制您的完美旅程</p>
    </header>

    <main class="main-content">
      <div v-if="!planResult" class="form-container">
        <div class="tabs">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            :class="['tab', { active: activeTab === tab.id }]"
            @click="activeTab = tab.id"
          >
            {{ tab.label }}
          </button>
        </div>

        <div class="travel-form">
          <div v-show="activeTab === 'basic'" class="form-section">
            <div class="form-group">
              <label>目的地 *</label>
              <input
                v-model="formData.destination"
                type="text"
                placeholder="例如：成都、巴黎、东京"
                class="form-input"
              />
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>旅行天数 *</label>
                <input
                  v-model.number="formData.days"
                  type="number"
                  min="1"
                  max="30"
                  class="form-input"
                />
              </div>

              <div class="form-group">
                <label>预算等级 *</label>
                <select v-model="formData.budget" class="form-select">
                  <option v-for="opt in budgetOptions" :key="opt.value" :value="opt.value">
                    {{ opt.label }}
                  </option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label>出发地</label>
              <input
                v-model="formData.departureCity"
                type="text"
                placeholder="例如：上海"
                class="form-input"
              />
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>出行日期</label>
                <input
                  v-model="formData.travelDate"
                  type="date"
                  class="form-input"
                />
              </div>

              <div class="form-group">
                <label>同行人员</label>
                <select v-model="formData.companions" class="form-select">
                  <option value="">请选择</option>
                  <option v-for="opt in companionsOptions" :key="opt.value" :value="opt.value">
                    {{ opt.label }}
                  </option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label>兴趣偏好</label>
              <div class="checkbox-grid">
                <div
                  v-for="opt in interestOptions"
                  :key="opt"
                  :class="['checkbox-label', { checked: formData.interests.includes(opt) }]"
                  @click="toggleMultiple(opt, formData.interests)"
                >
                  {{ opt }}
                </div>
              </div>
            </div>

            <div class="form-group">
              <label>每日预算细分（元/天）</label>
              <div class="budget-grid">
                <div class="budget-item">
                  <label>住宿</label>
                  <input
                    v-model="formData.budgetBreakdown.accommodation"
                    type="number"
                    placeholder="¥/天"
                    class="budget-input"
                  />
                </div>
                <div class="budget-item">
                  <label>餐饮</label>
                  <input
                    v-model="formData.budgetBreakdown.food"
                    type="number"
                    placeholder="¥/天"
                    class="budget-input"
                  />
                </div>
                <div class="budget-item">
                  <label>门票</label>
                  <input
                    v-model="formData.budgetBreakdown.attractions"
                    type="number"
                    placeholder="¥/天"
                    class="budget-input"
                  />
                </div>
                <div class="budget-item">
                  <label>购物</label>
                  <input
                    v-model="formData.budgetBreakdown.shopping"
                    type="number"
                    placeholder="¥/天"
                    class="budget-input"
                  />
                </div>
              </div>
            </div>
          </div>

          <div v-show="activeTab === 'preferences'" class="form-section">
            <div class="form-group">
              <label>饮食限制</label>
              <div class="checkbox-grid">
                <div
                  v-for="opt in dietaryOptions"
                  :key="opt.value"
                  :class="['checkbox-label', { checked: formData.dietaryRestrictions.includes(opt.value) }]"
                  @click="toggleMultiple(opt.value, formData.dietaryRestrictions)"
                >
                  {{ opt.label }}
                </div>
              </div>
            </div>

            <div class="form-group">
              <label>步行强度</label>
              <select v-model="formData.walkingIntensity" class="form-select">
                <option value="">请选择</option>
                <option v-for="opt in walkingOptions" :key="opt.value" :value="opt.value">
                  {{ opt.label }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>住宿类型偏好</label>
              <div class="checkbox-grid">
                <div
                  v-for="opt in accommodationOptions"
                  :key="opt.value"
                  :class="['checkbox-label', { checked: formData.accommodationTypes.includes(opt.value) }]"
                  @click="toggleMultiple(opt.value, formData.accommodationTypes)"
                >
                  {{ opt.label }}
                </div>
              </div>
            </div>

            <div class="form-group">
              <label>景点类型偏好</label>
              <div class="checkbox-grid">
                <div
                  v-for="opt in attractionTypeOptions"
                  :key="opt"
                  :class="['checkbox-label', { checked: formData.attractionTypes.includes(opt) }]"
                  @click="toggleMultiple(opt, formData.attractionTypes)"
                >
                  {{ opt }}
                </div>
              </div>
            </div>

            <div class="form-group">
              <label>特殊需求</label>
              <div class="checkbox-grid">
                <div
                  v-for="opt in specialNeedsOptions"
                  :key="opt.value"
                  :class="['checkbox-label', { checked: formData.specialNeeds.includes(opt.value) }]"
                  @click="toggleMultiple(opt.value, formData.specialNeeds)"
                >
                  {{ opt.label }}
                </div>
              </div>
            </div>

            <div class="form-group">
              <div
                class="checkbox-label inline"
                :class="{ checked: formData.languagePreference }"
                @click="formData.languagePreference = !formData.languagePreference"
              >
                需要中文导游/讲解器
              </div>
            </div>
          </div>

          <div v-show="activeTab === 'schedule'" class="form-section">
            <div class="form-row">
              <div class="form-group">
                <label>每日开始时间</label>
                <select v-model="formData.dailyStartTime" class="form-select">
                  <option v-for="time in startTimeOptions" :key="time" :value="time">
                    {{ time }}
                  </option>
                </select>
              </div>

              <div class="form-group">
                <label>每日结束时间</label>
                <select v-model="formData.dailyEndTime" class="form-select">
                  <option v-for="time in endTimeOptions" :key="time" :value="time">
                    {{ time }}
                  </option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <div
                class="checkbox-label inline"
                :class="{ checked: formData.needLunchBreak }"
                @click="formData.needLunchBreak = !formData.needLunchBreak"
              >
                需要午休
              </div>
            </div>

            <div class="form-group">
              <label>行程灵活度</label>
              <select v-model="formData.flexibility" class="form-select">
                <option v-for="opt in flexibilityOptions" :key="opt.value" :value="opt.value">
                  {{ opt.label }}
                </option>
              </select>
            </div>
          </div>

          <div class="form-actions">
            <button
              v-if="activeTab !== 'basic'"
              type="button"
              class="btn btn-secondary"
              @click="goToPrevTab"
            >
              上一步
            </button>
            <button
              v-if="activeTab !== 'schedule'"
              type="button"
              class="btn btn-primary"
              @click="goToNextTab"
            >
              下一步
            </button>
            <button
              v-if="activeTab === 'schedule'"
              type="button"
              :disabled="isSubmitting || !formData.destination.trim()"
              class="btn btn-submit"
              @click="submitForm"
            >
              {{ isSubmitting ? '生成中...' : '生成行程' }}
            </button>
          </div>
        </div>
        <!-- 加载遮罩 -->
        <div v-if="isSubmitting" class="loading-overlay">
          <div class="loading-spinner"></div>
          <p class="loading-text">正在为您规划完美行程...</p>
          <p class="loading-subtext">AI正在分析目的地特色，请稍候</p>
        </div>
      </div>

      <div v-else class="result-container">
        <div class="result-header">
          <button class="btn btn-secondary" @click="backToForm">返回修改</button>
          <div class="export-dropdown">
            <button class="btn btn-primary export-btn">导出行程 ▼</button>
            <div class="export-menu">
              <button class="export-option" @click="exportAsText">
                📄 TXT文本
              </button>
              <button class="export-option" @click="exportAsJSON">
                📋 JSON数据
              </button>
              <button class="export-option" @click="exportAsHTML">
                🌐 HTML网页
              </button>
            </div>
          </div>
        </div>

        <div class="result-summary">
          <h2>{{ planResult.destination }} {{ planResult.total_days }}天旅行计划</h2>
          <p class="budget-badge">预算等级：{{ planResult.budget_level }}</p>
          <p class="total-budget">总预算：¥{{ planResult.total_budget }}</p>
        </div>

        <div class="daily-plans">
          <div v-for="day in planResult.daily_plans" :key="day.day" class="daily-plan">
            <div class="day-header">
              <h3>第{{ day.day }}天：{{ day.theme }}</h3>
              <span class="daily-budget">¥{{ day.daily_budget }}</span>
            </div>

            <div v-if="day.weather_alert" class="alert alert-weather">
              ☁️ {{ day.weather_alert }}
            </div>

            <div v-if="day.transport_guide" class="info-card transport">
              <h4>🚗 交通指引</h4>
              <p>{{ day.transport_guide }}</p>
            </div>

            <div class="section">
              <h4>📅 活动安排</h4>
              <div class="activities">
                <div v-for="(act, index) in day.activities" :key="index" class="activity">
                  <span class="time">{{ act.time }}</span>
                  <span class="activity-name">{{ act.activity }}</span>
                  <span v-if="act.notes" class="notes">{{ act.notes }}</span>
                </div>
              </div>
            </div>

            <div v-if="day.walking_estimate" class="info-card walking">
              <h4>🚶 步行预估</h4>
              <p>{{ day.walking_estimate }}</p>
            </div>

            <div class="section">
              <h4>🍽️ 餐饮推荐</h4>
              <div class="meals">
                <div v-for="(meal, index) in day.meals" :key="index" class="meal">
                  <span class="meal-type">
                    {{ meal.meal_type === 'breakfast' ? '早餐' : meal.meal_type === 'lunch' ? '午餐' : '晚餐' }}
                  </span>
                  <span class="meal-suggestion">{{ meal.suggestion }}</span>
                  <span class="meal-cost">约¥{{ meal.estimated_cost }}</span>
                </div>
              </div>
            </div>

            <div v-if="day.budget_details && day.budget_details.length > 0" class="section">
              <h4>💰 预算明细</h4>
              <div class="budget-details">
                <div v-for="(item, index) in formatBudgetDetails(day.budget_details)" :key="index" class="budget-item">
                  <span>{{ item.category }}</span>
                  <span>¥{{ item.amount }}</span>
                  <span v-if="item.description" class="budget-desc">{{ item.description }}</span>
                </div>
              </div>
            </div>

            <div v-if="day.attraction_tips && day.attraction_tips.length > 0" class="info-card tips">
              <h4>💡 景点贴士</h4>
              <ul>
                <li v-for="(tip, index) in day.attraction_tips" :key="index">{{ tip }}</li>
              </ul>
            </div>

            <div v-if="day.alternative_plan" class="info-card alternative">
              <h4>🌧️ 备选方案</h4>
              <p>{{ day.alternative_plan }}</p>
            </div>

            <div v-if="day.accommodation_note" class="info-card accommodation">
              <h4>🏨 住宿提示</h4>
              <p>{{ day.accommodation_note }}</p>
            </div>
          </div>
        </div>

        <div v-if="planResult.overall_tips && planResult.overall_tips.length > 0" class="section">
          <h3>💬 整体建议</h3>
          <ul class="tips-list">
            <li v-for="(tip, index) in planResult.overall_tips" :key="index">{{ tip }}</li>
          </ul>
        </div>

        <div v-if="planResult.packing_list && planResult.packing_list.length > 0" class="section">
          <h3>🎒 打包清单</h3>
          <ul class="packing-list">
            <li v-for="(item, index) in planResult.packing_list" :key="index">• {{ item }}</li>
          </ul>
        </div>

        <div v-if="planResult.cultural_tips && planResult.cultural_tips.length > 0" class="section">
          <h3>🙏 文化礼仪提示</h3>
          <ul class="tips-list">
            <li v-for="(tip, index) in planResult.cultural_tips" :key="index">{{ tip }}</li>
          </ul>
        </div>
      </div>
    </main>

    <footer class="footer">
      <p>AI 旅行规划师 - 让旅行更简单</p>
    </footer>
  </div>
</template>
