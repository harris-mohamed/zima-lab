import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'
import type { OutletReading, PowerPoint } from '../types/power'

interface PowerStripProps {
  outlets: OutletReading[]
  history: PowerPoint[]
}

function outletColor(watts: number | null): string {
  if (watts === null) return 'sensor-card--error'
  if (watts > 300) return 'sensor-card--warn'
  return ''
}

function totalByMinute(history: PowerPoint[]): { time: string; watts: number }[] {
  const map = new Map<string, number>()
  for (const p of history) {
    map.set(p.time, (map.get(p.time) ?? 0) + (p.watts ?? 0))
  }
  return Array.from(map.entries())
    .map(([time, watts]) => ({ time: new Date(time).toLocaleTimeString(), watts }))
    .sort((a, b) => a.time.localeCompare(b.time))
}

export function PowerStrip({ outlets, history }: PowerStripProps) {
  const chartData = totalByMinute(history)
  const totalWatts = outlets.reduce((sum, o) => sum + (o.watts ?? 0), 0)

  return (
    <div className="power-section">
      <div className="power-section__header">
        <span className="power-section__title">Power Strip</span>
        <span className="power-section__total">{totalWatts.toFixed(0)} W total</span>
      </div>

      <div className="power-outlets">
        {outlets.length === 0 ? (
          <span className="power-section__empty">No data — check KASA_HOST</span>
        ) : (
          outlets.map((o) => (
            <div key={o.outlet_id} className={`sensor-card ${outletColor(o.watts)}`}>
              <span className="sensor-card__label">{o.outlet_name || `Outlet ${o.outlet_id}`}</span>
              <span className="sensor-card__value">
                {o.watts !== null ? o.watts.toFixed(1) : '—'}
              </span>
              <span className="sensor-card__unit">W</span>
            </div>
          ))
        )}
      </div>

      {chartData.length > 0 && (
        <div className="chart-card">
          <h3 className="chart-card__title">Total Power</h3>
          <ResponsiveContainer width="100%" height={180}>
            <LineChart data={chartData} margin={{ top: 4, right: 8, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="time" tick={{ fontSize: 10, fill: '#94a3b8' }} interval="preserveStartEnd" />
              <YAxis tick={{ fontSize: 10, fill: '#94a3b8' }} unit="W" width={50} />
              <Tooltip
                contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 6 }}
                labelStyle={{ color: '#94a3b8' }}
                formatter={(v) => [`${Number(v).toFixed(1)} W`, 'Total']}
              />
              <Line
                type="monotone"
                dataKey="watts"
                stroke="#facc15"
                dot={false}
                strokeWidth={2}
                connectNulls
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}
