import { Reservas, Reserva, Cliente, Cancha } from '../types/reportes'

// Cambiar a false para usar la API real (cuando esté disponible)
const USE_MOCK = true

const mockReservas: Reservas = [
  { id: 1, clienteId: 1, clienteNombre: 'Juan Perez', canchaId: 1, canchaNombre: 'Cancha A', fechaInicio: '2025-01-15T10:00:00', fechaFin: '2025-01-15T11:00:00' },
  { id: 2, clienteId: 2, clienteNombre: 'María López', canchaId: 2, canchaNombre: 'Cancha B', fechaInicio: '2025-02-20T14:00:00', fechaFin: '2025-02-20T15:00:00' },
  { id: 3, clienteId: 1, clienteNombre: 'Juan Perez', canchaId: 1, canchaNombre: 'Cancha A', fechaInicio: '2025-02-25T09:00:00', fechaFin: '2025-02-25T10:00:00' },
  { id: 4, clienteId: 3, clienteNombre: 'Laura Gómez', canchaId: 3, canchaNombre: 'Cancha C', fechaInicio: '2025-03-05T18:00:00', fechaFin: '2025-03-05T19:00:00' },
  { id: 5, clienteId: 2, clienteNombre: 'María López', canchaId: 1, canchaNombre: 'Cancha A', fechaInicio: '2025-03-10T12:00:00', fechaFin: '2025-03-10T13:00:00' },
  { id: 6, clienteId: 4, clienteNombre: 'Carlos Ruiz', canchaId: 2, canchaNombre: 'Cancha B', fechaInicio: '2025-04-01T16:00:00', fechaFin: '2025-04-01T17:00:00' },
  { id: 7, clienteId: 1, clienteNombre: 'Juan Perez', canchaId: 2, canchaNombre: 'Cancha B', fechaInicio: '2025-04-15T10:00:00', fechaFin: '2025-04-15T11:00:00' },
]

export async function fetchReservas(): Promise<Reservas> {
  if (USE_MOCK) return Promise.resolve(mockReservas)

  // Si se habilita la API real en el futuro, actualizar la URL
  const res = await fetch('/api/reservas')
  if (!res.ok) throw new Error('Error fetching reservas')
  return res.json()
}

export async function fetchClientes(): Promise<Cliente[]> {
  if (USE_MOCK) {
    const clientesMap = new Map<number, Cliente>()
    mockReservas.forEach(r => {
      if (!clientesMap.has(r.clienteId)) clientesMap.set(r.clienteId, { id: r.clienteId, nombre: r.clienteNombre })
    })
    return Array.from(clientesMap.values())
  }
  const res = await fetch('/api/clientes')
  if (!res.ok) throw new Error('Error fetching clientes')
  return res.json()
}

export async function fetchCanchas(): Promise<Cancha[]> {
  if (USE_MOCK) {
    const canchasMap = new Map<number, Cancha>()
    mockReservas.forEach(r => {
      if (!canchasMap.has(r.canchaId)) canchasMap.set(r.canchaId, { id: r.canchaId, nombre: r.canchaNombre })
    })
    return Array.from(canchasMap.values())
  }
  const res = await fetch('/api/canchas')
  if (!res.ok) throw new Error('Error fetching canchas')
  return res.json()
}

export default { fetchReservas, fetchClientes, fetchCanchas }
