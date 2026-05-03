import './styles/App.css'
import { useEffect, useState } from 'react'
import { SensorCard } from './components/SensorCard'
import { SensorChart } from './components/SensorChart'
import { CameraFeed } from './components/CameraFeed'
import { useSensorWebSocket } from './hooks/useSensorWebSocket'
import { useSensorHistory } from './hooks/useSensorHistory'
import type { SensorReading } from './types/sensors'

export default function App() {
  const { latest, history: liveHistory } = useSensorWebSocket()
  const seedHistory = useSensorHistory(60)
  const [history, setHistory] = useState<SensorReading[]>([])

  useEffect(() => {
    if (seedHistory.length > 0 && liveHistory.length === 0) {
      setHistory(seedHistory)
    }
  }, [seedHistory, liveHistory.length])

  useEffect(() => {
    if (liveHistory.length > 0) {
      setHistory(liveHistory)
    }
  }, [liveHistory])

  const r = latest

  return (
    <div className="app">
      <header className="app__header">
        <h1 className="app__title">Zima Lab</h1>
        <span className="app__status">
          {r ? `Last update: ${new Date(r.recorded_at).toLocaleTimeString()}` : 'Connecting…'}
        </span>
      </header>

      <div className="dashboard">
        <div className="cameras">
          <CameraFeed src="/api/cameras/picam" label="Pi Camera" />
          <CameraFeed src="/api/cameras/usb" label="USB Camera" />
        </div>

        <div className="sensor-cards">
          <SensorCard label="pH" value={r?.ph} unit="" decimals={2}
            warn={(v) => v < 5.5 || v > 7.0} />
          <SensorCard label="TDS" value={r?.tds} unit="ppm" decimals={0}
            warn={(v) => v > 1500} />
          <SensorCard label="Water Temp" value={r?.water_temp} unit="°C"
            warn={(v) => v > 26} />
          <SensorCard label="Air Temp" value={r?.air_temp} unit="°C" />
          <SensorCard label="Humidity" value={r?.humidity} unit="%" decimals={0}
            warn={(v) => v > 80} />
          <SensorCard label="Water Level" value={r?.water_level_cm} unit="cm" />
        </div>

        <div className="charts">
          <SensorChart data={history} dataKey="ph" label="pH" unit="" color="#4ade80" />
          <SensorChart data={history} dataKey="tds" label="TDS" unit="ppm" color="#60a5fa" />
          <SensorChart data={history} dataKey="water_temp" label="Water Temp" unit="°C" color="#f97316" />
          <SensorChart data={history} dataKey="humidity" label="Humidity" unit="%" color="#c084fc" />
        </div>
      </div>
    </div>
  )
}
