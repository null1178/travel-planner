<script setup lang="ts">
import { ref, reactive, onMounted, nextTick } from "vue"
import { useAuth } from "../stores/auth"
import { generatePlan, savePlan } from "../api"
import MapView from "../components/MapView.vue"
import AMapLoader from "@amap/amap-jsapi-loader"

const { user } = useAuth()

const selectionMap = ref<HTMLDivElement>()
const selectionMode = ref<'departure' | 'destination'>('departure')
const mapLoading = ref(false)


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
  destination: "",
  days: 3,
  budget: "comfort",
  interests: [],
  departureCity: "",
  travelDate: "",
  companions: "",
  budgetBreakdown: { accommodation: "", food: "", attractions: "", shopping: "" },
  dietaryRestrictions: [],
  walkingIntensity: "",
  accommodationTypes: [],
  attractionTypes: [],
  specialNeeds: [],
  languagePreference: false,
  dailyStartTime: "09:00",
  dailyEndTime: "20:00",
  needLunchBreak: false,
  flexibility: "adjustable"
})

const budgetOptions = [
  { value: "economy", label: "经济型" },
  { value: "comfort", label: "舒适型" },
  { value: "luxury", label: "豪华型" }
]

const companionsOptions = [
  { value: "alone", label: "独自旅行" },
  { value: "couple", label: "情侣" },
  { value: "family_with_kids", label: "家庭（有小孩）" },
  { value: "family_with_elderly", label: "家庭（有老人）" },
  { value: "friends", label: "朋友" }
]

const interestOptions = [
  "历史文化", "自然风光", "美食探索", "购物休闲",
  "主题乐园", "网红打卡", "博物馆", "户外运动",
  "温泉度假", "海岛沙滩", "古镇风情", "城市观光"
]

const dietaryOptions = [
  { value: "vegetarian", label: "素食" },
  { value: "halal", label: "清真" },
  { value: "seafood_allergy", label: "海鲜过敏" },
  { value: "love_spicy", label: "无辣不欢" }
]

const walkingOptions = [
  { value: "easy", label: "轻松（<5k步）" },
  { value: "moderate", label: "适中（5-15k步）" },
  { value: "intense", label: "特种兵（>15k步）" }
]

const accommodationOptions = [
  { value: "hotel", label: "酒店" },
  { value: "bnb", label: "民宿" },
  { value: "hostel", label: "青旅" },
  { value: "camping", label: "露营" }
]

const attractionTypeOptions = [
  "网红打卡", "博物馆", "自然风光", "主题乐园",
  "历史古迹", "美食街区", "购物商圈", "文化体验",
  "户外徒步", "温泉养生"
]

const specialNeedsOptions = [
  { value: "wheelchair", label: "轮椅友好" },
  { value: "stroller", label: "婴儿车通道" },
  { value: "accessible", label: "无障碍设施" }
]

const startTimeOptions = ["06:00", "07:00", "08:00", "09:00", "10:00"]
const endTimeOptions = ["18:00", "20:00", "22:00", "不限"]

const flexibilityOptions = [
  { value: "strict", label: "严格按计划" },
  { value: "adjustable", label: "可调整30%" },
  { value: "casual", label: "随意" }
]

const isSubmitting = ref(false)
const isSaving = ref(false)
const planResult: any = ref(null)
const saveMessage = ref("")
const activeTab = ref("basic")
const tabs = [
  { id: "basic", label: "基础信息" },
  { id: "preferences", label: "偏好限制" },
  { id: "schedule", label: "时间节奏" }
]

const transportModeIcons: Record<string, string> = {
  high_speed_rail: "🚄",
  flight: "✈️",
  normal_train: "🚂",
  bus: "🚌",
  self_drive: "🚗"
}

function toggleMultiple(option: string, list: string[]) {
  const index = list.indexOf(option)
  if (index > -1) list.splice(index, 1)
  else list.push(option)
}

function goToPrevTab() {
  const currentIndex = tabs.findIndex(t => t.id === activeTab.value)
  if (currentIndex > 0) activeTab.value = tabs[currentIndex - 1].id
}

function goToNextTab() {
  const currentIndex = tabs.findIndex(t => t.id === activeTab.value)
  if (currentIndex < tabs.length - 1) activeTab.value = tabs[currentIndex + 1].id
}

async function submitForm() {
  if (!formData.destination.trim()) {
    alert("请输入目的地")
    return
  }
  isSubmitting.value = true
  saveMessage.value = ""
  try {
    const requestData: any = {
      destination: formData.destination,
      days: formData.days,
      budget: formData.budget,
      interests: formData.interests.length > 0 ? formData.interests : []
    }
    if (formData.departureCity) requestData.departure_city = formData.departureCity
    if (formData.travelDate) requestData.travel_date = formData.travelDate
    if (formData.companions) requestData.companions = formData.companions
    if (formData.budgetBreakdown.accommodation || formData.budgetBreakdown.food ||
        formData.budgetBreakdown.attractions || formData.budgetBreakdown.shopping) {
      requestData.budget_breakdown = {}
      if (formData.budgetBreakdown.accommodation) requestData.budget_breakdown.accommodation = parseInt(formData.budgetBreakdown.accommodation)
      if (formData.budgetBreakdown.food) requestData.budget_breakdown.food = parseInt(formData.budgetBreakdown.food)
      if (formData.budgetBreakdown.attractions) requestData.budget_breakdown.attractions = parseInt(formData.budgetBreakdown.attractions)
      if (formData.budgetBreakdown.shopping) requestData.budget_breakdown.shopping = parseInt(formData.budgetBreakdown.shopping)
    }
    if (formData.dietaryRestrictions.length > 0) requestData.dietary_restrictions = formData.dietaryRestrictions
    if (formData.walkingIntensity) requestData.walking_intensity = formData.walkingIntensity
    if (formData.accommodationTypes.length > 0) requestData.accommodation_types = formData.accommodationTypes
    if (formData.attractionTypes.length > 0) requestData.attraction_types = formData.attractionTypes
    if (formData.specialNeeds.length > 0) requestData.special_needs = formData.specialNeeds
    if (formData.languagePreference) requestData.language_preference = formData.languagePreference
    requestData.daily_start_time = formData.dailyStartTime
    requestData.daily_end_time = formData.dailyEndTime
    requestData.need_lunch_break = formData.needLunchBreak
    requestData.flexibility = formData.flexibility

    planResult.value = await generatePlan(requestData)
  } catch (error) {
    console.error("Error:", error)
    alert(`生成行程时发生错误: ${error instanceof Error ? error.message : String(error)}`)
  } finally {
    isSubmitting.value = false
  }
}

async function onSavePlan() {
  if (!planResult.value || !user.value) return
  isSaving.value = true
  saveMessage.value = ""
  try {
    await savePlan({
      destination: planResult.value.destination,
      total_days: planResult.value.total_days,
      budget_level: planResult.value.budget_level,
      plan_data: planResult.value
    })
    saveMessage.value = "已保存到我的计划"
  } catch (error) {
    saveMessage.value = `保存失败: ${error instanceof Error ? error.message : "未知错误"}`
  } finally {
    isSaving.value = false
  }
}

function formatBudgetDetails(details: any[]) {
  const categoryMap: Record<string, string> = {
    accommodation: "住宿", food: "餐饮", attractions: "门票",
    transport: "交通", shopping: "购物"
  }
  return details?.map(item => ({ ...item, category: categoryMap[item.category] || item.category })) || []
}

function exportAsText() {
  if (!planResult.value) return
  let text = `旅行计划 - ${planResult.value.destination} ${planResult.value.total_days}天\n`
  text += `预算等级：${planResult.value.budget_level}\n\n`
  planResult.value.daily_plans.forEach((day: any) => {
    text += `=== 第${day.day}天：${day.theme} ===\n`
    text += "活动安排：\n"
    day.activities.forEach((act: any) => text += ` ${act.time} - ${act.activity}${act.notes ? ` (${act.notes})` : ""}\n`)
    text += "餐饮推荐：\n"
    day.meals.forEach((meal: any) => {
      const mn = meal.meal_type === "breakfast" ? "早餐" : meal.meal_type === "lunch" ? "午餐" : "晚餐"
      text += ` ${mn}：${meal.suggestion}（约¥${meal.estimated_cost}）\n`
    })
    if (day.transport_guide) text += `交通指引：${day.transport_guide}\n`
    if (day.walking_estimate) text += `步行预估：${day.walking_estimate}\n`
    text += `每日预算：¥${day.daily_budget}\n\n`
  })
  if (planResult.value.total_budget) text += `\n总预算：¥${planResult.value.total_budget}`
  const blob = new Blob([text], { type: "text/plain;charset=utf-8" })
  const a = document.createElement("a")
  a.href = URL.createObjectURL(blob)
  a.download = `${planResult.value.destination}_${planResult.value.total_days}天行程.txt`
  a.click()
}

function exportAsJSON() {
  if (!planResult.value) return
  const blob = new Blob([JSON.stringify(planResult.value, null, 2)], { type: "application/json;charset=utf-8" })
  const a = document.createElement("a")
  a.href = URL.createObjectURL(blob)
  a.download = `${planResult.value.destination}_${planResult.value.total_days}天行程.json`
  a.click()
}


async function initSelectionMap() {
  const key = import.meta.env.VITE_AMAP_KEY
  if (!key || key === 'your_amap_key_here' || !selectionMap.value) { mapLoading.value = false; return }

  mapLoading.value = true
  try {
    // Pre-load Geocoder plugin
    const AMap = await AMapLoader.load({
      key,
      version: '1.4.15',
      plugins: ['AMap.Geocoder']
    })

    const map = new AMap.Map(selectionMap.value, {
      zoom: 5,
      center: [116.397, 39.908],
      resizeEnable: true
    })

    mapLoading.value = false

    let departureMarker: any = null
    let destinationMarker: any = null
    const geocoder = new AMap.Geocoder({})

    // Bind click
    map.on('click', function(e: any) {
      const lng = e.lnglat.getLng()
      const lat = e.lnglat.getLat()

      // Remove old marker for current mode only (keep the other)
      if (selectionMode.value === 'departure') {
        if (departureMarker) { departureMarker.setMap(null); departureMarker = null }
        departureMarker = new AMap.Marker({ position: [lng, lat] })
        departureMarker.setMap(map)
      } else {
        if (destinationMarker) { destinationMarker.setMap(null); destinationMarker = null }
        destinationMarker = new AMap.Marker({ position: [lng, lat] })
        destinationMarker.setMap(map)
      }

      // Reverse geocode via plugin
      geocoder.getAddress([lng, lat], function(status: string, result: any) {
        console.log('[Map] geocoder status:', status, 'result:', result)
        if (status === 'complete' && result.regeocode) {
          const comp = result.regeocode.addressComponent
          let city = ''
          if (comp.city) {
            city = Array.isArray(comp.city) ? comp.city[0] : comp.city
          }
          if (!city && comp.province) {
            city = Array.isArray(comp.province) ? comp.province[0] : comp.province
          }
          console.log('[Map] resolved city:', city)
          if (city) {
            if (selectionMode.value === 'departure') formData.departureCity = city
            else formData.destination = city
          }
        } else {
          // Fallback: use REST API
          console.log('[Map] plugin geocoder failed, trying REST API')
          fetch('https://restapi.amap.com/v3/geocode/regeo?key=' + key + '&location=' + lng + ',' + lat)
            .then(function(r) { return r.json() })
            .then(function(data: any) {
              console.log('[Map] REST API result:', data)
              if (data.status === '1' && data.regeocode) {
                const comp = data.regeocode.addressComponent
                let city = ''
                if (comp.city) {
                  city = Array.isArray(comp.city) ? comp.city[0] : comp.city
                }
                if (!city && comp.province) {
                  city = Array.isArray(comp.province) ? comp.province[0] : comp.province
                }
                console.log('[Map] REST resolved city:', city)
                if (city) {
                  if (selectionMode.value === 'departure') formData.departureCity = city
                  else formData.destination = city
                }
              }
            })
            .catch(function(err: any) { console.error('[Map] REST API error:', err) })
        }
      })
    })
  } catch (e: any) {
    console.error('[Map] init failed:', e)
    mapLoading.value = false
  }
}

onMounted(() => {
  nextTick(() => initSelectionMap())
})

function backToForm() {
  planResult.value = null
  saveMessage.value = ""
}
</script>

<template>
  <div>
    <header class="header">
      <h1>AI 旅行规划师</h1>
      <p>智能定制您的完美旅程</p>
    </header>

    <main class="main-content">
      <div v-if="!planResult" class="form-container">
        <div class="tabs">
          <button v-for="tab in tabs" :key="tab.id" :class="['tab', { active: activeTab === tab.id }]" @click="activeTab = tab.id">
            {{ tab.label }}
          </button>
        </div>
        <div class="travel-form">
          <div v-show="activeTab === 'basic'" class="form-section">
            <div class="form-row">
              <div class="form-group">
                <label>出发地</label>
                <input v-model="formData.departureCity" type="text" placeholder="可输入或点击地图选择" class="form-input" autocomplete="off" />
              </div>
              <div class="form-group">
                <label>目的地 *</label>
                <input v-model="formData.destination" type="text" placeholder="可输入或点击地图选择" class="form-input" autocomplete="off" />
              </div>
            </div>
            <!-- Map selector -->
            <div class="form-group">
              <div class="map-mode-toggle">
                <button :class="['mode-btn', { active: selectionMode === 'departure' }]" @click="selectionMode = 'departure'">选出发地</button>
                <button :class="['mode-btn', { active: selectionMode === 'destination' }]" @click="selectionMode = 'destination'">选目的地</button>
                <span class="mode-hint">点击地图即可选中城市</span>
              </div>
              <div ref="selectionMap" class="selection-map"></div>
              <div v-if="mapLoading" class="map-loading">地图加载中...</div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>旅行天数 *</label>
                <input v-model.number="formData.days" type="number" min="1" max="30" class="form-input" />
              </div>
              <div class="form-group">
                <label>预算等级 *</label>
                <select v-model="formData.budget" class="form-select">
                  <option v-for="opt in budgetOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
                </select>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>出行日期</label>
                <input v-model="formData.travelDate" type="date" class="form-input" />
              </div>
              <div class="form-group">
                <label>同行人员</label>
                <select v-model="formData.companions" class="form-select">
                  <option value="">请选择</option>
                  <option v-for="opt in companionsOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <label>兴趣爱好</label>
              <div class="checkbox-grid">
                <div v-for="opt in interestOptions" :key="opt" :class="['checkbox-label', { checked: formData.interests.includes(opt) }]" @click="toggleMultiple(opt, formData.interests)">
                  {{ opt }}
                </div>
              </div>
            </div>
            <div class="form-group">
              <label>每日预算细分（元/天）</label>
              <div class="budget-grid">
                <div class="budget-item"><label>住宿</label><input v-model="formData.budgetBreakdown.accommodation" type="number" placeholder="¥/天" class="budget-input" /></div>
                <div class="budget-item"><label>餐饮</label><input v-model="formData.budgetBreakdown.food" type="number" placeholder="¥/天" class="budget-input" /></div>
                <div class="budget-item"><label>门票</label><input v-model="formData.budgetBreakdown.attractions" type="number" placeholder="¥/天" class="budget-input" /></div>
                <div class="budget-item"><label>购物</label><input v-model="formData.budgetBreakdown.shopping" type="number" placeholder="¥/天" class="budget-input" /></div>
              </div>
            </div>
          </div>

          <div v-show="activeTab === 'preferences'" class="form-section">
            <div class="form-group">
              <label>饮食限制</label>
              <div class="checkbox-grid">
                <div v-for="opt in dietaryOptions" :key="opt.value" :class="['checkbox-label', { checked: formData.dietaryRestrictions.includes(opt.value) }]" @click="toggleMultiple(opt.value, formData.dietaryRestrictions)">
                  {{ opt.label }}
                </div>
              </div>
            </div>
            <div class="form-group">
              <label>步行强度</label>
              <select v-model="formData.walkingIntensity" class="form-select">
                <option value="">请选择</option>
                <option v-for="opt in walkingOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>住宿类型偏好</label>
              <div class="checkbox-grid">
                <div v-for="opt in accommodationOptions" :key="opt.value" :class="['checkbox-label', { checked: formData.accommodationTypes.includes(opt.value) }]" @click="toggleMultiple(opt.value, formData.accommodationTypes)">
                  {{ opt.label }}
                </div>
              </div>
            </div>
            <div class="form-group">
              <label>景点类型偏好</label>
              <div class="checkbox-grid">
                <div v-for="opt in attractionTypeOptions" :key="opt" :class="['checkbox-label', { checked: formData.attractionTypes.includes(opt) }]" @click="toggleMultiple(opt, formData.attractionTypes)">
                  {{ opt }}
                </div>
              </div>
            </div>
            <div class="form-group">
              <label>特殊需求</label>
              <div class="checkbox-grid">
                <div v-for="opt in specialNeedsOptions" :key="opt.value" :class="['checkbox-label', { checked: formData.specialNeeds.includes(opt.value) }]" @click="toggleMultiple(opt.value, formData.specialNeeds)">
                  {{ opt.label }}
                </div>
              </div>
            </div>
            <div class="form-group">
              <div class="checkbox-label inline" :class="{ checked: formData.languagePreference }" @click="formData.languagePreference = !formData.languagePreference">
                需要中文导游/讲解器
              </div>
            </div>
          </div>

          <div v-show="activeTab === 'schedule'" class="form-section">
            <div class="form-row">
              <div class="form-group">
                <label>每日开始时间</label>
                <select v-model="formData.dailyStartTime" class="form-select">
                  <option v-for="time in startTimeOptions" :key="time" :value="time">{{ time }}</option>
                </select>
              </div>
              <div class="form-group">
                <label>每日结束时间</label>
                <select v-model="formData.dailyEndTime" class="form-select">
                  <option v-for="time in endTimeOptions" :key="time" :value="time">{{ time }}</option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <div class="checkbox-label inline" :class="{ checked: formData.needLunchBreak }" @click="formData.needLunchBreak = !formData.needLunchBreak">
                需要午休
              </div>
            </div>
            <div class="form-group">
              <label>行程灵活度</label>
              <select v-model="formData.flexibility" class="form-select">
                <option v-for="opt in flexibilityOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
              </select>
            </div>
          </div>

          <div class="form-actions">
            <button v-if="activeTab !== 'basic'" type="button" class="btn btn-secondary" @click="goToPrevTab">上一步</button>
            <button v-if="activeTab !== 'schedule'" type="button" class="btn btn-primary" @click="goToNextTab">下一步</button>
            <button v-if="activeTab === 'schedule'" type="button" :disabled="isSubmitting || !formData.destination.trim()" class="btn btn-submit" @click="submitForm">
              {{ isSubmitting ? "生成中..." : "生成行程" }}
            </button>
          </div>
        </div>
        <div v-if="isSubmitting" class="loading-overlay">
          <div class="loading-spinner"></div>
          <p class="loading-text">正在为您规划完美行程...</p>
          <p class="loading-subtext">AI正在分析目的地特色，请稍候</p>
        </div>
      </div>

      <div v-else class="result-container">
        <div class="result-header">
          <button class="btn btn-secondary" @click="backToForm">返回修改</button>
          <div style="display:flex;gap:0.75rem;align-items:center">
            <button v-if="user" class="btn btn-save" :disabled="isSaving" @click="onSavePlan">
              {{ isSaving ? "保存中..." : "保存到我的计划" }}
            </button>
            <span v-if="saveMessage" class="save-msg">{{ saveMessage }}</span>
            <span v-if="!user" class="save-hint">登录后可保存计划</span>
            <div class="export-dropdown">
              <button class="btn btn-primary export-btn">导出行程 ▼</button>
              <div class="export-menu">
                <button class="export-option" @click="exportAsText">📫 TXT文本</button>
                <button class="export-option" @click="exportAsJSON">📵 JSON数据</button>
              </div>
            </div>
          </div>
        </div>

        <div class="result-summary">
          <h2>{{ planResult.destination }} {{ planResult.total_days }}天旅行计划</h2>
          <p class="budget-badge">预算等级：{{ planResult.budget_level }}</p>
          <p class="total-budget">总预算：¥{{ planResult.total_budget }}</p>
        </div>

        <!-- Map -->
        <div style="padding: 0 2rem">
          <MapView
            v-if="planResult.departure_coords && planResult.destination_coords"
            :departureCoords="planResult.departure_coords"
            :destinationCoords="planResult.destination_coords"
            :departureLabel="formData.departureCity || '出发地'"
            :destinationLabel="planResult.destination"
          />
        </div>

        <!-- Transportation recommendations -->
        <div v-if="planResult.transportation && planResult.transportation.length > 0" class="transport-section">
          <h3>🚅 交通推荐</h3>
          <div class="transport-cards">
            <div v-for="(opt, idx) in planResult.transportation" :key="idx" class="transport-card">
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
        <div v-if="planResult.return_transportation && planResult.return_transportation.length > 0" class="transport-section">
          <h3>🔙 回程交通推荐</h3>
          <div class="transport-cards">
            <div v-for="(opt, idx) in planResult.return_transportation" :key="idx" class="transport-card">
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
          <div v-for="day in planResult.daily_plans" :key="day.day" class="daily-plan">
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
            <div v-if="day.budget_details && day.budget_details.length > 0" class="section">
              <h4>💰 预算明细</h4>
              <div class="budget-details">
                <div v-for="(item, index) in formatBudgetDetails(day.budget_details)" :key="index" class="budget-item">
                  <span>{{ item.category }}</span><span>¥{{ item.amount }}</span>
                  <span v-if="item.description" class="budget-desc">{{ item.description }}</span>
                </div>
              </div>
            </div>
            <div v-if="day.attraction_tips && day.attraction_tips.length > 0" class="info-card tips">
              <h4>💡 景点贴士</h4>
              <ul><li v-for="(tip, idx) in day.attraction_tips" :key="idx">{{ tip }}</li></ul>
            </div>
            <div v-if="day.alternative_plan" class="info-card alternative">
              <h4>🔄 备选方案</h4><p>{{ day.alternative_plan }}</p>
            </div>
            <div v-if="day.accommodation_note" class="info-card accommodation">
              <h4>🏣 住宿提示</h4><p>{{ day.accommodation_note }}</p>
            </div>
          </div>
        </div>

        <div v-if="planResult.overall_tips && planResult.overall_tips.length > 0" class="section">
          <h3>💰 整体建议</h3>
          <ul class="tips-list"><li v-for="(tip, idx) in planResult.overall_tips" :key="idx">{{ tip }}</li></ul>
        </div>
      </div>
    </main>
  </div>
</template>
