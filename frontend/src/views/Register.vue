<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuth } from "../stores/auth"

const router = useRouter()
const { register } = useAuth()

const username = ref("")
const email = ref("")
const password = ref("")
const confirmPassword = ref("")
const errorMsg = ref("")
const isLoading = ref(false)

async function onRegister() {
  errorMsg.value = ""
  if (!username.value || !email.value || !password.value) {
    errorMsg.value = "请填写所有字段"
    return
  }
  if (password.value !== confirmPassword.value) {
    errorMsg.value = "两次密码输入不一致"
    return
  }
  if (password.value.length < 6) {
    errorMsg.value = "密码长度至少6位"
    return
  }
  isLoading.value = true
  try {
    await register(username.value, email.value, password.value)
    router.push("/")
  } catch (e: any) {
    errorMsg.value = e.message || "注册失败"
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-card">
      <h2>注册</h2>
      <p class="auth-sub">创建账号，保存你的旅行计划</p>
      <div v-if="errorMsg" class="auth-error">{{ errorMsg }}</div>
      <form @submit.prevent="onRegister">
        <div class="form-group">
          <label>用户名</label>
          <input v-model="username" type="text" placeholder="请输入用户名" class="form-input" autocomplete="username" />
        </div>
        <div class="form-group">
          <label>邮箱</label>
          <input v-model="email" type="email" placeholder="请输入邮箱" class="form-input" autocomplete="email" />
        </div>
        <div class="form-group">
          <label>密码</label>
          <input v-model="password" type="password" placeholder="至少6位密码" class="form-input" autocomplete="new-password" />
        </div>
        <div class="form-group">
          <label>确认密码</label>
          <input v-model="confirmPassword" type="password" placeholder="再次输入密码" class="form-input" autocomplete="new-password" />
        </div>
        <button type="submit" class="btn btn-submit auth-btn" :disabled="isLoading">
          {{ isLoading ? "注册中..." : "注册" }}
        </button>
      </form>
      <p class="auth-switch">
        已有账号？<router-link to="/login">立即登录</router-link>
      </p>
    </div>
  </div>
</template>
