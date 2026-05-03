import './styles/App.css'
import { useEffect, useState } from 'react'
import { SensorCard } from './components/SensorCard'
import { PlantRow } from './components/PlantRow'
import { MultiLineChart } from './components/MultiLineChart'
import { CameraFeed } from './components/CameraFeed'
import { PowerStrip } from './components/PowerStrip'
import { useSensorWebSocket } from './hooks/useSensorWebSocket'
import { useSensorHistory } from './hooks/useSensorHistory'
import { usePowerLatest } from './hooks/usePowerLatest'
import { usePowerHistory } from './hooks/usePowerHistory'
import type { PlantReading } from './types/sensors'

const NUM_PLANTS = 5

export default function App() {
  const { frame, historyByPlant: liveHistory } = useSensorWebSocket()
  const seedHistory = useSensorHistory(60)
  const [historyByPlant, setHistoryByPlant] = useState<Record<number, PlantReading[]>>({})

  // Seed from REST on mount, then switch to live WebSocket data
  useEffect(() => {
    if (seedHistory.length === 0 || Object.keys(liveHistory).length > 0) return
    const grouped: Record<number, PlantReading[]> = {}
    for (const r of seedHistory) {
      ;(grouped[r.plant_id] ??= []).push(r)
    }
    setHistoryByPlant(grouped)
  }, [seedHistory, liveHistory])

  useEffect(() => {
    if (Object.keys(liveHistory).length > 0) setHistoryByPlant(liveHistory)
  }, [liveHistory])

  // Flatten history across all plants for multi-line charts
  const flatHistory = Object.values(historyByPlant).flat()

  const outlets = usePowerLatest()
  const powerHistory = usePowerHistory(60)

  const latestByPlant: Record<number, PlantReading> = {}
  for (let i = 0; i < NUM_PLANTS; i++) {
    const arr = historyByPlant[i]
    if (arr?.length) latestByPlant[i] = arr[arr.length - 1]
  }

  const shared = frame ?? latestByPlant[0]
  const lastUpdate = shared?.recorded_at
    ? new Date(shared.recorded_at).toLocaleTimeString()
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
        <div className="cameras">
          <CameraFeed src="/api/cameras/picam" label="Pi Camera" />
          <CameraFeed src="/api/cameras/usb" label="USB Camera" />
        </div>

        <div className="sensor-cards">
          <SensorCard label="Air Temp" value={shared?.air_temp} unit="°C" />
          <SensorCard label="Humidity" value={shared?.humidity} unit="%" decimals={0}
            warn={(v) => v > 80} />
        </div>

        <div className="plant-grid">
          {Array.from({ length: NUM_PLANTS }, (_, i) => (
            <PlantRow key={i} plantId={i} reading={latestByPlant[i]} />
          ))}
        </div>

        <div className="charts">
          <MultiLineChart history={flatHistory} dataKey="ph" label="pH" unit="" numPlants={NUM_PLANTS} />
          <MultiLineChart history={flatHistory} dataKey="tds" label="TDS" unit="ppm" numPlants={NUM_PLANTS} />
          <MultiLineChart history={flatHistory} dataKey="water_temp" label="Water Temp" unit="°C" numPlants={NUM_PLANTS} />
          <MultiLineChart history={flatHistory} dataKey="water_level_cm" label="Water Level" unit="cm" numPlants={NUM_PLANTS} />
        </div>

        <PowerStrip outlets={outlets} history={powerHistory} />
      </div>
    </div>
  )
}
