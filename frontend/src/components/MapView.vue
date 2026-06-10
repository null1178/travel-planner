<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from "vue"
import AMapLoader from "@amap/amap-jsapi-loader"

const props = defineProps<{
  departureCoords: [number, number] | null  // [lng, lat]
  destinationCoords: [number, number] | null
  departureLabel?: string
  destinationLabel?: string
}>()

const mapContainer = ref<HTMLDivElement>()
const mapReady = ref(false)
const mapError = ref("")
let mapInstance: any = null

async function initMap() {
  const amapKey = import.meta.env.VITE_AMAP_KEY
  if (!amapKey || amapKey === "your_amap_key_here") {
    mapError.value = "请配置高德地图 Key（在 frontend/.env 中设置 VITE_AMAP_KEY）"
    return
  }

  if (!props.departureCoords || !props.destinationCoords) {
    mapError.value = "缺少出发地或目的地坐标"
    return
  }

  try {
    const AMap = await AMapLoader.load({
      key: amapKey,
      version: "1.4.15"
    })

    if (!mapContainer.value) return

    mapInstance = new AMap.Map(mapContainer.value, {
      zoom: 8,
      center: props.departureCoords,
      viewMode: "2D"
    })

    // Markers
    const departureMarker = new AMap.Marker({
      position: props.departureCoords,
      title: props.departureLabel || "出发地",
      label: {
        content: `<div style="background:#667eea;color:#fff;padding:2px 8px;border-radius:4px;font-size:12px;white-space:nowrap">${props.departureLabel || "出发"}</div>`,
        offset: new AMap.Pixel(0, -36)
      }
    })

    const destinationMarker = new AMap.Marker({
      position: props.destinationCoords,
      title: props.destinationLabel || "目的地",
      label: {
        content: `<div style="background:#11998e;color:#fff;padding:2px 8px;border-radius:4px;font-size:12px;white-space:nowrap">${props.destinationLabel || "目的地"}</div>`,
        offset: new AMap.Pixel(0, -36)
      }
    })

    mapInstance.add([departureMarker, destinationMarker])

    // Line between two points
    const polyline = new AMap.Polyline({
      path: [props.departureCoords, props.destinationCoords],
      strokeColor: "#667eea",
      strokeWeight: 4,
      strokeStyle: "dashed",
      strokeDasharray: [10, 5],
      lineJoin: "round"
    })
    mapInstance.add(polyline)

    // Fit bounds to show both markers
    mapInstance.setFitView(null, false, [80, 80, 80, 80])

    mapReady.value = true
  } catch (e: any) {
    mapError.value = `地图加载失败: ${e.message || e}`
  }
}

onMounted(() => {
  nextTick(() => initMap())
})

watch(() => [props.departureCoords, props.destinationCoords], () => {
  if (mapInstance) {
    mapInstance.destroy()
    mapInstance = null
    mapReady.value = false
    mapError.value = ""
  }
  nextTick(() => initMap())
})
</script>

<template>
  <div class="map-section">
    <h4>🗺️ 出发地与目的地</h4>
    <div v-if="mapError" class="map-placeholder">{{ mapError }}</div>
    <div ref="mapContainer" class="map-container" :class="{ hidden: !!mapError }"></div>
  </div>
</template>

<style scoped>
.map-section {
  margin-bottom: 1.5rem;
}
.map-section h4 {
  margin-bottom: 0.8rem;
  color: #343a40;
  font-size: 1.1rem;
}
.map-container {
  width: 100%;
  height: 300px;
  border-radius: 12px;
  overflow: hidden;
  border: 2px solid #e9ecef;
}
.map-container.hidden {
  display: none;
}
.map-placeholder {
  background: #fff8e1;
  color: #856404;
  padding: 1.5rem;
  border-radius: 10px;
  text-align: center;
  font-size: 0.9rem;
}
</style>
