import React, { useEffect, useState } from 'react'
import { Bar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'
import reportesService from '../../services/reportes.service'
import { Reserva } from '../../types/reportes'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

export default function GraficoMensual() {
  const [reservas, setReservas] = useState<Reserva[]>([])

  useEffect(() => {
    reportesService.fetchReservas().then(setReservas)
  }, [])

  // Agrupar por mes (año actual)
  const months = Array.from({length:12}).map((_,i)=>i)
  const counts = months.map(m => 0)
  const nowYear = new Date().getFullYear()
  reservas.forEach(r => {
    const d = new Date(r.fechaInicio)
    if (d.getFullYear() === nowYear) {
      counts[d.getMonth()] = (counts[d.getMonth()] || 0) + 1
    }
  })

  const data = {
    labels: ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'],
    datasets: [
      {
        label: 'Reservas',
        data: counts,
        backgroundColor: 'rgba(99,102,241,0.8)'
      }
    ]
  }

  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'top' as const },
      title: { display: true, text: `Utilización mensual (${nowYear})` }
    }
  }

  return (
    <div>
      <h2 className="text-lg font-medium">Gráfico: utilización mensual de canchas</h2>
      <div className="mt-4">
        <Bar options={options} data={data} />
      </div>
    </div>
  )
}
