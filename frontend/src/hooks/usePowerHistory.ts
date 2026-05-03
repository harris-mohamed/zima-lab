import { useEffect, useState } from 'react'
import type { PowerPoint } from '../types/power'

export function usePowerHistory(minutes = 60, intervalMs = 30_000): PowerPoint[] {
  const [history, setHistory] = useState<PowerPoint[]>([])

  useEffect(() => {
    const poll = () =>
      fetch(`/api/power/history?minutes=${minutes}`)
        .then((r) => r.json())
        .then(setHistory)
        .catch(console.error)

    poll()
    const id = setInterval(poll, intervalMs)
    return () => clearInterval(id)
  }, [minutes, intervalMs])

  return history
}
