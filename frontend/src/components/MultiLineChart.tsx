import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import type { PlantReading } from '../types/sensors'

const PLANT_COLORS = ['#4ade80', '#60a5fa', '#f97316', '#c084fc', '#f43f5e']

interface MultiLineChartProps {
  history: PlantReading[]
  dataKey: keyof PlantReading
  label: string
  unit: string
  numPlants: number
}

export function MultiLineChart({ history, dataKey, label, unit, numPlants }: MultiLineChartProps) {
  // Pivot: one entry per timestamp, keyed by plant_id
  const byTime = new Map<string, Record<string, number | null>>()
  for (const r of history) {
    const time = new Date(r.recorded_at).toLocaleTimeString()
    if (!byTime.has(time)) byTime.set(time, { time })
    byTime.get(time)![`p${r.plant_id}`] = r[dataKey] as number | null
  }
  const chartData = Array.from(byTime.values())

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
            formatter={(v, name) => [`${Number(v).toFixed(2)} ${unit}`, name]}
          />
          <Legend wrapperStyle={{ fontSize: 10, color: '#94a3b8' }} />
          {Array.from({ length: numPlants }, (_, i) => (
            <Line
              key={i}
              type="monotone"
              dataKey={`p${i}`}
              name={`Plant ${i + 1}`}
              stroke={PLANT_COLORS[i]}
              dot={false}
              strokeWidth={2}
              connectNulls
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
