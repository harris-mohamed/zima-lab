import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'
import type { PlantReading } from '../types/sensors'

interface SensorChartProps {
  data: PlantReading[]
  dataKey: keyof PlantReading
  label: string
  unit: string
  color?: string
}

export function SensorChart({
  data,
  dataKey,
  label,
  unit,
  color = '#4ade80',
}: SensorChartProps) {
  const chartData = data.map((r) => ({
    time: new Date(r.recorded_at).toLocaleTimeString(),
    value: r[dataKey] as number | null,
  }))

  return (
    <div className="chart-card">
      <h3 className="chart-card__title">{label}</h3>
      <ResponsiveContainer width="100%" height={180}>
        <LineChart data={chartData} margin={{ top: 4, right: 8, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="time" tick={{ fontSize: 10, fill: '#94a3b8' }} interval="preserveStartEnd" />
          <YAxis tick={{ fontSize: 10, fill: '#94a3b8' }} unit={unit} width={45} />
          <Tooltip
            contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 6 }}
            labelStyle={{ color: '#94a3b8' }}
            formatter={(v) => [`${Number(v).toFixed(2)} ${unit}`, label]}
          />
          <Line
            type="monotone"
            dataKey="value"
            stroke={color}
            dot={false}
            strokeWidth={2}
            connectNulls
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
