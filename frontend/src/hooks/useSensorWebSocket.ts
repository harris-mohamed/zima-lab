import { useEffect, useRef, useState } from 'react'
import type { SensorReading } from '../types/sensors'

const WS_URL = `ws://${window.location.host}/ws/sensors`
const MAX_BACKOFF_MS = 30_000

export function useSensorWebSocket() {
  const [latest, setLatest] = useState<SensorReading | null>(null)
  const [history, setHistory] = useState<SensorReading[]>([])
  const wsRef = useRef<WebSocket | null>(null)
  const backoffRef = useRef(1_000)

  useEffect(() => {
    let cancelled = false

    function connect() {
      if (cancelled) return
      const ws = new WebSocket(WS_URL)
      wsRef.current = ws

      ws.onmessage = (evt) => {
        const reading: SensorReading = JSON.parse(evt.data)
        setLatest(reading)
        setHistory((prev) => {
          const next = [...prev, reading]
          // Keep 60 minutes of data at ~1 reading/s
          return next.slice(-3600)
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

  return { latest, history }
}
