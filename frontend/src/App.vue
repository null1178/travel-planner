<template>
  <div class="app-container">
    <header class="app-header">
      <div class="header-content">
        <h1>✈️ AI 旅行行程规划师</h1>
        <p>智能规划你的完美旅程</p>
      </div>
    </header>

    <main class="app-main">
      <Transition name="fade" mode="out-in">
        <TravelForm v-if="!tripPlan" />
        <TripResult v-else />
      </Transition>

      <el-alert
        v-if="error"
        :title="error"
        type="error"
        show-icon
        closable
        class="error-alert"
        @close="handleCloseError"
      />
    </main>

    <footer class="app-footer">
      <p>Powered by DeepSeek AI · Vue 3 + FastAPI</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useTravelStore } from './stores/travel'
import TravelForm from './components/TravelForm.vue'
import TripResult from './components/TripResult.vue'

const travelStore = useTravelStore()
const tripPlan = computed(() => travelStore.tripPlan)
const error = computed(() => travelStore.error)

const handleCloseError = () => {
  travelStore.reset()
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  padding: 40px 20px;
  text-align: center;
  color: white;
}

.header-content h1 {
  font-size: 36px;
  margin-bottom: 8px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.header-content p {
  font-size: 18px;
  opacity: 0.9;
}

.app-main {
  flex: 1;
  padding: 0 20px 40px;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}

.error-alert {
  margin-top: 20px;
}

.app-footer {
  padding: 20px;
  text-align: center;
  color: white;
  opacity: 0.8;
}

.app-footer p {
  font-size: 14px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
