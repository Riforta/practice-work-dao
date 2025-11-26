import React, { useState, useRef } from 'react'
import ListadoPorCliente from './ListadoPorCliente'
import ReservasPorCanchaPeriodo from './ReservasPorCanchaPeriodo'
import TopCanchas from './TopCanchas'
import GraficoMensual from './GraficoMensual'
import pdfService from '../../services/pdf.service'

export default function Reportes() {
  const [view, setView] = useState<'listado'|'porCancha'|'top'|'grafico'>('listado')
  const contentRef = useRef<HTMLDivElement | null>(null)

  return (
    <div className="min-h-screen bg-slate-950 text-white px-4 py-10">
      <div className="max-w-5xl mx-auto space-y-6">
        <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <p className="text-sm uppercase tracking-widest text-emerald-200">Reportes</p>
            <h1 className="text-3xl font-bold">Panel de reportes</h1>
          </div>
            <div className="flex gap-3">
              <button
                onClick={() => { /* recargar datos si fuera necesario */ }}
                className="rounded-lg bg-white/10 px-4 py-2 text-sm font-semibold text-emerald-100 hover:bg-white/20"
              >
                Refrescar
              </button>
              <button
                  onClick={async () => {
                    const el = contentRef.current
                    if (!el) {
                      alert('Elemento de reporte no disponible. Intenta recargar la página.')
                      return
                    }

                    const filename = `reportes_${view}.pdf`
                    try {
                      await pdfService.exportElementToPdf(el, filename)
                    } catch (err: any) {
                      // mostrar mensaje más descriptivo al usuario y loguear en consola
                      // eslint-disable-next-line no-console
                      console.error('Error exportando PDF', err)
                      const msg = err?.message || String(err) || 'Error desconocido'
                      alert(`No se pudo exportar el PDF: ${msg}`)
                    }
                  }}
                  className="rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400"
                >
                  Exportar
                </button>
            </div>
        </header>

        <section className="bg-white/10 backdrop-blur-md rounded-2xl p-4 shadow-lg border border-white/10">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex flex-wrap gap-3">
              <button
                onClick={()=>setView('listado')}
                className={`rounded-lg px-4 py-2 text-sm font-semibold ${view==='listado' ? 'bg-emerald-500 text-slate-950' : 'bg-white/10 text-emerald-100 hover:bg-white/20'}`}
              >
                Listado por cliente
              </button>
              <button
                onClick={()=>setView('porCancha')}
                className={`rounded-lg px-4 py-2 text-sm font-semibold ${view==='porCancha' ? 'bg-emerald-500 text-slate-950' : 'bg-white/10 text-emerald-100 hover:bg-white/20'}`}
              >
                Reservas por cancha
              </button>
              <button
                onClick={()=>setView('top')}
                className={`rounded-lg px-4 py-2 text-sm font-semibold ${view==='top' ? 'bg-emerald-500 text-slate-950' : 'bg-white/10 text-emerald-100 hover:bg-white/20'}`}
              >
                Top canchas
              </button>
              <button
                onClick={()=>setView('grafico')}
                className={`rounded-lg px-4 py-2 text-sm font-semibold ${view==='grafico' ? 'bg-emerald-500 text-slate-950' : 'bg-white/10 text-emerald-100 hover:bg-white/20'}`}
              >
                Gráfico mensual
              </button>
            </div>
            <div>
              {/* botón para limpiar filtros si se implementan filtros globales */}
            </div>
          </div>
        </section>

        <section className="bg-white/5 backdrop-blur-md rounded-2xl border border-white/10 shadow-xl overflow-hidden p-4">
          <div className="space-y-6" ref={contentRef}>
            {view === 'listado' && <ListadoPorCliente />}
            {view === 'porCancha' && <ReservasPorCanchaPeriodo />}
            {view === 'top' && <TopCanchas />}
            {view === 'grafico' && <GraficoMensual />}
          </div>
        </section>
      </div>
    </div>
  )
}
