export interface PlantReading {
  recorded_at: string
  plant_id: number
  ph: number | null
  tds: number | null
  water_temp: number | null
  water_level_cm: number | null
  air_temp: number | null
  humidity: number | null
}

export interface SensorFrame {
  recorded_at: string
  air_temp: number | null
  humidity: number | null
  plants: PlantReading[]
}
