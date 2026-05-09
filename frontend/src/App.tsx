import './styles/App.css'
import { useEffect, useState } from 'react'
import { SensorCard } from './components/SensorCard'
import { SensorChart } from './components/SensorChart'
import { useSensorWebSocket } from './hooks/useSensorWebSocket'
import { useSensorHistory } from './hooks/useSensorHistory'
import type { PlantReading } from './types/sensors'

export default function App() {
  const { frame, historyByPlant: liveHistory } = useSensorWebSocket()
  const seedHistory = useSensorHistory(60)
  const [history, setHistory] = useState<PlantReading[]>([])

  // Seed from REST on mount, then hand off to live WebSocket data
  useEffect(() => {
    if (seedHistory.length === 0 || (liveHistory[0]?.length ?? 0) > 0) return
    setHistory(seedHistory.filter((r) => r.plant_id === 0))
  }, [seedHistory, liveHistory])

  useEffect(() => {
    if ((liveHistory[0]?.length ?? 0) > 0) setHistory(liveHistory[0])
  }, [liveHistory])

  const latest = history[history.length - 1]

  // Live values: prefer the fresh WS frame, fall back to last DB row
  const airTemp = frame?.air_temp ?? latest?.air_temp ?? null
  const humidity = frame?.humidity ?? latest?.humidity ?? null
  const tds      = frame?.plants?.[0]?.tds ?? latest?.tds ?? null

  const lastUpdate = (frame ?? latest)?.recorded_at
    ? new Date((frame ?? latest)!.recorded_at).toLocaleTimeString()
    : null

  return (
    <div className="app">
      <header className="app__header">
        <h1 className="app__title">Zima Lab</h1>
        <span className="app__status">
          {lastUpdate ? `Last update: ${lastUpdate}` : 'Connecting…'}
        </span>
      </header>

      <div className="dashboard">
        <div className="sensor-cards">
          <SensorCard label="Air Temp" value={airTemp}  unit="°F"  decimals={1} />
          <SensorCard label="Humidity" value={humidity} unit="%"   decimals={0} warn={(v) => v > 80} />
          <SensorCard label="TDS"      value={tds}      unit="ppm" decimals={0} />
        </div>

        <div className="charts">
          <SensorChart data={history} dataKey="air_temp" label="Air Temp" unit="°F"  color="#60a5fa" />
          <SensorChart data={history} dataKey="humidity" label="Humidity" unit="%"   color="#c084fc" />
          <SensorChart data={history} dataKey="tds"      label="TDS"      unit="ppm" color="#4ade80" />
        </div>
      </div>
    </div>
  )
}
