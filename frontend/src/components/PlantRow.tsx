import { SensorCard } from './SensorCard'
import type { PlantReading } from '../types/sensors'

interface PlantRowProps {
  plantId: number
  reading: PlantReading | undefined
}

export function PlantRow({ plantId, reading }: PlantRowProps) {
  const r = reading
  return (
    <div className="plant-row">
      <span className="plant-row__label">Plant {plantId + 1}</span>
      <div className="plant-row__cards">
        <SensorCard label="pH" value={r?.ph} unit="" decimals={2}
          warn={(v) => v < 5.5 || v > 7.0} />
        <SensorCard label="TDS" value={r?.tds} unit="ppm" decimals={0}
          warn={(v) => v > 1500} />
        <SensorCard label="Water Temp" value={r?.water_temp} unit="°C"
          warn={(v) => v > 26} />
        <SensorCard label="Water Level" value={r?.water_level_cm} unit="cm" />
      </div>
    </div>
  )
}
