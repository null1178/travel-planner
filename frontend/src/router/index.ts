import { createRouter, createWebHistory } from "vue-router"
import Home from "../views/Home.vue"
import Login from "../views/Login.vue"
import Register from "../views/Register.vue"
import UserCenter from "../views/UserCenter.vue"
import Share from "../views/Share.vue"

const routes = [
  { path: "/", name: "home", component: Home },
  { path: "/login", name: "login", component: Login },
  { path: "/register", name: "register", component: Register },
  { path: "/user", name: "user", component: UserCenter, meta: { requiresAuth: true } },
  { path: "/share/:token", name: "share", component: Share }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
