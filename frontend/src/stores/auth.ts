import { ref } from "vue"
import { getProfile, login as apiLogin, register as apiRegister } from "../api"

interface User {
  id: number
  username: string
  email: string
}

const user = ref<User | null>(null)
const token = ref<string | null>(localStorage.getItem("token"))
const isAuthReady = ref(false)

export function useAuth() {
  async function init() {
    if (token.value) {
      try {
        const profile = await getProfile()
        user.value = profile
      } catch {
        token.value = null
        localStorage.removeItem("token")
      }
    }
    isAuthReady.value = true
  }

  async function loginAction(email: string, password: string) {
    const data = await apiLogin(email, password)
    token.value = data.access_token
    user.value = data.user
    localStorage.setItem("token", data.access_token)
    return data
  }

  async function registerAction(username: string, email: string, password: string) {
    const data = await apiRegister(username, email, password)
    token.value = data.access_token
    user.value = data.user
    localStorage.setItem("token", data.access_token)
    return data
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem("token")
  }

  return {
    user,
    token,
    isAuthReady,
    init,
    login: loginAction,
    register: registerAction,
    logout
  }
}
