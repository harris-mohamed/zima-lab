interface SensorCardProps {
  label: string
  value: number | null | undefined
  unit: string
  decimals?: number
  warn?: (v: number) => boolean
}

export function SensorCard({ label, value, unit, decimals = 1, warn }: SensorCardProps) {
  const isError = value === null || value === undefined
  const isWarn = !isError && warn ? warn(value!) : false

  return (
    <div className={`sensor-card ${isError ? 'sensor-card--error' : ''} ${isWarn ? 'sensor-card--warn' : ''}`}>
      <span className="sensor-card__label">{label}</span>
      <span className="sensor-card__value">
        {isError ? '—' : value!.toFixed(decimals)}
      </span>
      <span className="sensor-card__unit">{unit}</span>
    </div>
  )
}
