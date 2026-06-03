<template>
  <div class="travel-form">
    <el-card class="form-card" :class="{ 'loading-card': loading }">
      <template #header>
        <div class="card-header">
          <h2>🗺️ 开始规划你的旅程</h2>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-width="100px"
        label-position="left"
      >
        <el-form-item label="目的地" prop="destination">
          <el-input
            v-model="formData.destination"
            placeholder="例如：东京、巴黎、丽江"
            size="large"
          />
        </el-form-item>

        <el-form-item label="旅行天数" prop="days">
          <el-input-number
            v-model="formData.days"
            :min="1"
            :max="15"
            size="large"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="预算等级" prop="budget">
          <el-radio-group v-model="formData.budget" size="large">
            <el-radio-button value="economy">经济</el-radio-button>
            <el-radio-button value="comfort">舒适</el-radio-button>
            <el-radio-button value="luxury">豪华</el-radio-button>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="兴趣偏好" prop="interests">
          <el-checkbox-group v-model="formData.interests">
            <el-checkbox value="美食">🍜 美食</el-checkbox>
            <el-checkbox value="历史">🏛️ 历史</el-checkbox>
            <el-checkbox value="自然">🌿 自然</el-checkbox>
            <el-checkbox value="购物">🛍️ 购物</el-checkbox>
            <el-checkbox value="夜生活">🌃 夜生活</el-checkbox>
          </el-checkbox-group>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            @click="submitForm"
            style="width: 100%"
          >
            {{ loading ? 'AI 规划中...' : '✨ 生成行程' }}
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed } from 'vue'
import { useTravelStore } from '../stores/travel'
import type { FormInstance, FormRules } from 'element-plus'

interface FormData {
  destination: string
  days: number
  budget: string
  interests: string[]
}

const travelStore = useTravelStore()
const formRef = ref<FormInstance>()

const formData = reactive<FormData>({
  destination: '',
  days: 3,
  budget: 'comfort',
  interests: []
})

const rules: FormRules = {
  destination: [
    { required: true, message: '请输入目的地', trigger: 'blur' },
    { min: 2, message: '目的地至少2个字符', trigger: 'blur' }
  ],
  days: [
    { required: true, message: '请选择天数', trigger: 'change' }
  ],
  budget: [
    { required: true, message: '请选择预算等级', trigger: 'change' }
  ],
  interests: [
    { type: 'array', required: true, message: '请至少选择一个兴趣偏好', trigger: 'change' }
  ]
}

const loading = computed(() => travelStore.loading)

const submitForm = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      await travelStore.generatePlan({
        destination: formData.destination,
        days: formData.days,
        budget: formData.budget,
        interests: formData.interests
      })
    }
  })
}
</script>

<style scoped>
.travel-form {
  max-width: 600px;
  margin: 0 auto;
}

.form-card {
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.form-card.loading-card {
  pointer-events: none;
  opacity: 0.7;
}

.form-card.loading-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.3), transparent);
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

.card-header h2 {
  margin: 0;
  font-size: 24px;
  color: #303133;
  text-align: center;
}

:deep(.el-checkbox) {
  margin-right: 20px;
  margin-bottom: 8px;
}
</style>
