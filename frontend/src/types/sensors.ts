export interface SensorReading {
  id?: number
  recorded_at: string
  ph: number | null
  tds: number | null
  water_temp: number | null
  air_temp: number | null
  humidity: number | null
  water_level_cm: number | null
}
