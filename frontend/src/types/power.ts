export interface OutletReading {
  outlet_id: number
  outlet_name: string
  watts: number | null
  voltage: number | null
  current_a: number | null
  total_kwh: number | null
  recorded_at: string
}

export interface PowerPoint {
  time: string
  outlet_id: string
  outlet_name: string
  watts: number | null
}
