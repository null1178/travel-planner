import { defineConfig, loadEnv } from "vite"
import vue from "@vitejs/plugin-vue"

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "VITE_")
  return {
    plugins: [vue()],
    define: {
      "import.meta.env.VITE_AMAP_KEY": JSON.stringify(env.VITE_AMAP_KEY)
    }
  }
})
