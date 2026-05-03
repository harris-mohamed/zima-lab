import { useEffect, useRef, useState } from 'react'
import type { PlantReading, SensorFrame } from '../types/sensors'

const WS_URL = `ws://${window.location.host}/ws/sensors`
const MAX_BACKOFF_MS = 30_000
const MAX_HISTORY = 3600 // ~1 reading/s for 60 min

export function useSensorWebSocket() {
  const [frame, setFrame] = useState<SensorFrame | null>(null)
  const [historyByPlant, setHistoryByPlant] = useState<Record<number, PlantReading[]>>({})
  const wsRef = useRef<WebSocket | null>(null)
  const backoffRef = useRef(1_000)

  useEffect(() => {
    let cancelled = false

    function connect() {
      if (cancelled) return
      const ws = new WebSocket(WS_URL)
      wsRef.current = ws

      ws.onmessage = (evt) => {
        const incoming: SensorFrame = JSON.parse(evt.data)
        setFrame(incoming)
        setHistoryByPlant((prev) => {
          const next = { ...prev }
          for (const plant of incoming.plants) {
            const existing = next[plant.plant_id] ?? []
            next[plant.plant_id] = [...existing, plant].slice(-MAX_HISTORY)
          }
          return next
        })
        backoffRef.current = 1_000
      }

      ws.onclose = () => {
        if (cancelled) return
        const delay = backoffRef.current
        backoffRef.current = Math.min(delay * 2, MAX_BACKOFF_MS)
        setTimeout(connect, delay)
      }
    }

    connect()
    return () => {
      cancelled = true
      wsRef.current?.close()
    }
  }, [])

  return { frame, historyByPlant }
}
