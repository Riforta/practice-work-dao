import React, { useEffect, useState } from 'react'
import reportesService from '../../services/reportes.service'
import { Reserva, Cliente } from '../../types/reportes'

export default function ListadoPorCliente() {
  const [clientes, setClientes] = useState<Cliente[]>([])
  const [reservas, setReservas] = useState<Reserva[]>([])
  const [selectedCliente, setSelectedCliente] = useState<number | 'all'>('all')

  useEffect(() => {
    reportesService.fetchClientes().then(setClientes)
    reportesService.fetchReservas().then(setReservas)
  }, [])

  const filtered = reservas.filter(r => selectedCliente === 'all' ? true : r.clienteId === selectedCliente)

  return (
    <div>
      <h2 className="text-lg font-medium">Listado de reservas por cliente</h2>
      <div className="mt-3 flex items-center gap-3">
        <label className="text-sm">Cliente:</label>
        <select value={selectedCliente} onChange={e => setSelectedCliente(e.target.value === 'all' ? 'all' : Number(e.target.value))} className="rounded-md bg-gray-800 px-2 py-1">
          <option value="all">Todos</option>
          {clientes.map(c => <option key={c.id} value={c.id}>{c.nombre}</option>)}
        </select>
      </div>

      <div className="mt-4 overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead>
            <tr className="text-gray-400">
              <th className="px-2 py-2">ID</th>
              <th className="px-2 py-2">Cliente</th>
              <th className="px-2 py-2">Cancha</th>
              <th className="px-2 py-2">Inicio</th>
              <th className="px-2 py-2">Fin</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map(r => (
              <tr key={r.id} className="border-t border-gray-800">
                <td className="px-2 py-2">{r.id}</td>
                <td className="px-2 py-2">{r.clienteNombre}</td>
                <td className="px-2 py-2">{r.canchaNombre}</td>
                <td className="px-2 py-2">{new Date(r.fechaInicio).toLocaleString()}</td>
                <td className="px-2 py-2">{new Date(r.fechaFin).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
