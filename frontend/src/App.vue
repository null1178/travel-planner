<script setup lang="ts">
import { onMounted } from "vue"
import { useRouter } from "vue-router"
import { useAuth } from "./stores/auth"

const { user, init, logout } = useAuth()
const router = useRouter()

onMounted(() => {
  init()
})

function onLogout() {
  logout()
  router.push("/")
}
</script>

<template>
  <div class="app">
    <nav class="navbar">
      <router-link to="/" class="nav-brand">AI 旅行规划师</router-link>
      <div class="nav-links">
        <router-link to="/" class="nav-link">首页</router-link>
        <template v-if="user">
          <router-link to="/user" class="nav-link">我的计划</router-link>
          <span class="nav-user">{{ user.username }}</span>
          <button class="nav-btn" @click="onLogout">退出</button>
        </template>
        <template v-else>
          <router-link to="/login" class="nav-link">登录</router-link>
          <router-link to="/register" class="nav-link">注册</router-link>
        </template>
      </div>
    </nav>
    <router-view />
    <footer class="footer">
      <p>AI 旅行规划师 - 让旅行更简单</p>
    </footer>
  </div>
</template>
