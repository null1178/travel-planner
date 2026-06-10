<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuth } from "../stores/auth"

const router = useRouter()
const { login } = useAuth()

const email = ref("")
const password = ref("")
const errorMsg = ref("")
const isLoading = ref(false)

async function onLogin() {
  errorMsg.value = ""
  if (!email.value || !password.value) {
    errorMsg.value = "请填写邮箱和密码"
    return
  }
  isLoading.value = true
  try {
    await login(email.value, password.value)
    router.push("/")
  } catch (e: any) {
    errorMsg.value = e.message || "登录失败"
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-card">
      <h2>登录</h2>
      <p class="auth-sub">登录以查看和管理你的旅行计划</p>
      <div v-if="errorMsg" class="auth-error">{{ errorMsg }}</div>
      <form @submit.prevent="onLogin">
        <div class="form-group">
          <label>邮箱</label>
          <input v-model="email" type="email" placeholder="请输入邮箱" class="form-input" autocomplete="email" />
        </div>
        <div class="form-group">
          <label>密码</label>
          <input v-model="password" type="password" placeholder="请输入密码" class="form-input" autocomplete="current-password" />
        </div>
        <button type="submit" class="btn btn-submit auth-btn" :disabled="isLoading">
          {{ isLoading ? "登录中..." : "登录" }}
        </button>
      </form>
      <p class="auth-switch">
        还没有账号？<router-link to="/register">立即注册</router-link>
      </p>
    </div>
  </div>
</template>
