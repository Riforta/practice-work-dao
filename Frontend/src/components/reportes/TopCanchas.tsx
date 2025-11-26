import React, { useEffect, useState } from 'react'
import reportesService from '../../services/reportes.service'
import { Reserva } from '../../types/reportes'

export default function TopCanchas() {
  const [reservas, setReservas] = useState<Reserva[]>([])

  useEffect(() => {
    reportesService.fetchReservas().then(setReservas)
  }, [])

  const counts = reservas.reduce<Record<string, number>>((acc, r) => {
    acc[r.canchaNombre] = (acc[r.canchaNombre] || 0) + 1
    return acc
  }, {})

  const items = Object.entries(counts).sort((a,b) => b[1]-a[1])

  return (
    <div>
      <h2 className="text-lg font-medium">Canchas más utilizadas</h2>
      <div className="mt-4 overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead className="bg-white/10 text-emerald-100 uppercase text-xs tracking-wider">
            <tr>
              <th className="px-4 py-3 text-left">Cancha</th>
              <th className="px-4 py-3 text-left">Reservas</th>
            </tr>
          </thead>
          <tbody>
            {items.map(([cancha, cnt]) => (
              <tr key={cancha} className="border-t border-white/5 hover:bg-white/5">
                <td className="px-4 py-3">{cancha}</td>
                <td className="px-4 py-3 font-medium">{cnt}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
