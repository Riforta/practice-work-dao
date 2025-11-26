export interface Cliente {
  id: number
  nombre: string
  email?: string
}

export interface Cancha {
  id: number
  nombre: string
}

export interface Reserva {
  id: number
  clienteId: number
  clienteNombre: string
  canchaId: number
  canchaNombre: string
  fechaInicio: string // ISO
  fechaFin: string // ISO
}

export type Reservas = Reserva[]
