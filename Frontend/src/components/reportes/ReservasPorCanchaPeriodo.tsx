import React, { useEffect, useState } from 'react'
import reportesService from '../../services/reportes.service'
import { Reserva, Cancha } from '../../types/reportes'

export default function ReservasPorCanchaPeriodo() {
  const [canchas, setCanchas] = useState<Cancha[]>([])
  const [reservas, setReservas] = useState<Reserva[]>([])
  const [selectedCancha, setSelectedCancha] = useState<number | 'all'>('all')
  const [from, setFrom] = useState<string>('2025-01-01')
  const [to, setTo] = useState<string>('2025-12-31')

  useEffect(() => {
    reportesService.fetchCanchas().then(setCanchas)
    reportesService.fetchReservas().then(setReservas)
  }, [])

  const filtered = reservas.filter(r => {
    const t = new Date(r.fechaInicio).getTime()
    const fromT = new Date(from).getTime()
    const toT = new Date(to).getTime() + 24*60*60*1000 - 1
    const matchCancha = selectedCancha === 'all' ? true : r.canchaId === selectedCancha
    return matchCancha && t >= fromT && t <= toT
  })

  return (
    <div>
      <h2 className="text-lg font-medium">Reservas por cancha en un período</h2>
      <div className="mt-3 flex flex-wrap items-center gap-3">
        <label className="text-sm">Cancha:</label>
        <select value={selectedCancha} onChange={e => setSelectedCancha(e.target.value === 'all' ? 'all' : Number(e.target.value))} className="rounded-md bg-gray-800 px-2 py-1">
          <option value="all">Todas</option>
          {canchas.map(c => <option key={c.id} value={c.id}>{c.nombre}</option>)}
        </select>
        <label className="text-sm">Desde:</label>
        <input type="date" value={from} onChange={e=>setFrom(e.target.value)} className="rounded-md bg-gray-800 px-2 py-1" />
        <label className="text-sm">Hasta:</label>
        <input type="date" value={to} onChange={e=>setTo(e.target.value)} className="rounded-md bg-gray-800 px-2 py-1" />
      </div>

      <div className="mt-4 overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead>
            <tr className="text-gray-400">
              <th className="px-2 py-2">ID</th>
              <th className="px-2 py-2">Cliente</th>
              <th className="px-2 py-2">Cancha</th>
              <th className="px-2 py-2">Inicio</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map(r => (
              <tr key={r.id} className="border-t border-gray-800">
                <td className="px-2 py-2">{r.id}</td>
                <td className="px-2 py-2">{r.clienteNombre}</td>
                <td className="px-2 py-2">{r.canchaNombre}</td>
                <td className="px-2 py-2">{new Date(r.fechaInicio).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
