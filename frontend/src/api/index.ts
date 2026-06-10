const API_BASE = "http://localhost:8000"

function getToken(): string | null {
  return localStorage.getItem("token")
}

async function request(path: string, options: RequestInit = {}): Promise<any> {
  const token = getToken()
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string> || {})
  }
  if (token) {
    headers["Authorization"] = `Bearer ${token}`
  }

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers })
  const data = await res.json()

  if (!res.ok) {
    throw new Error(data.detail || `请求失败 (${res.status})`)
  }
  return data
}

// Auth
export function login(email: string, password: string) {
  return request("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password })
  })
}

export function register(username: string, email: string, password: string) {
  return request("/api/auth/register", {
    method: "POST",
    body: JSON.stringify({ username, email, password })
  })
}

export function getProfile() {
  return request("/api/auth/me")
}

// Plans
export function getMyPlans() {
  return request("/api/auth/plans")
}

export function savePlan(planData: any) {
  return request("/api/auth/plans/save", {
    method: "POST",
    body: JSON.stringify(planData)
  })
}

export function deletePlan(planId: number) {
  return request(`/api/auth/plans/${planId}`, {
    method: "DELETE"
  })
}

// Generate (no auth needed)
export function generatePlan(requestData: any) {
  return fetch(`${API_BASE}/api/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(requestData)
  }).then(res => {
    if (!res.ok) return res.text().then(t => { throw new Error(t) })
    return res.json()
  })
}
