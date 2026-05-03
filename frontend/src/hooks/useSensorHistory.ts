import { useEffect, useState } from 'react'
import type { PlantReading } from '../types/sensors'

export function useSensorHistory(minutes = 60): PlantReading[] {
  const [history, setHistory] = useState<PlantReading[]>([])

  useEffect(() => {
    fetch(`/api/sensors/history?minutes=${minutes}`)
      .then((r) => r.json())
      .then((data: PlantReading[]) => setHistory(data))
      .catch(console.error)
  }, [minutes])

  return history
}
