import { useEffect, useState } from 'react'
import type { SensorReading } from '../types/sensors'

export function useSensorHistory(minutes = 60): SensorReading[] {
  const [history, setHistory] = useState<SensorReading[]>([])

  useEffect(() => {
    fetch(`/api/sensors/history?minutes=${minutes}`)
      .then((r) => r.json())
      .then((data: SensorReading[]) => setHistory(data))
      .catch(console.error)
  }, [minutes])

  return history
}
