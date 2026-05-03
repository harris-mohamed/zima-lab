import { useEffect, useState } from 'react'
import type { OutletReading } from '../types/power'

export function usePowerLatest(intervalMs = 10_000): OutletReading[] {
  const [outlets, setOutlets] = useState<OutletReading[]>([])

  useEffect(() => {
    const poll = () =>
      fetch('/api/power/latest')
        .then((r) => r.json())
        .then(setOutlets)
        .catch(console.error)

    poll()
    const id = setInterval(poll, intervalMs)
    return () => clearInterval(id)
  }, [intervalMs])

  return outlets
}
