import { useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { useAuth } from '../../contexts/AuthContext'
import { useModal } from '../../contexts/ModalContext'
import turnosApi, { type Turno } from '../../services/turnos.service'
import serviciosApi, { type ServicioAdicional } from '../../services/servicios.service'

interface Cancha {
  id: number
  nombre: string
  tipo_deporte?: string
  descripcion?: string
  precio_hora?: number
  activa: number
}

/**
 * Vista pública: Muestra todas las canchas y sus turnos disponibles
 * Accesible sin login
 */
export default function CanchasPublicas() {
  const { user } = useAuth()
  const { openModal } = useModal()
  const navigate = useNavigate()
  const [canchas, setCanchas] = useState<Cancha[]>([])
  const [turnosPorCancha, setTurnosPorCancha] = useState<Record<number, Turno[]>>({})
  const [serviciosDisponibles, setServiciosDisponibles] = useState<ServicioAdicional[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [deporteFilter, setDeporteFilter] = useState<string>('todos')
  const [fechaFilter, setFechaFilter] = useState<string>('')
  const [fechaAplicada, setFechaAplicada] = useState<string>('') // Fecha realmente aplicada

  const isAuthenticated = !!user

  useEffect(() => {
    cargarDatos()
  }, [fechaAplicada]) // Solo recargar cuando se aplique el filtro

  const cargarDatos = async () => {
    try {
      setLoading(true)
      setError('')

      // Obtener todas las canchas activas
      const response = await fetch('http://127.0.0.1:8000/api/canchas/')
      const canchasData = await response.json()
      const canchasActivas = canchasData.filter((c: Cancha) => c.activa === 1)
      setCanchas(canchasActivas)

      // Cargar servicios adicionales disponibles
      const servicios = await serviciosApi.list()
      setServiciosDisponibles(servicios.filter(s => s.activo))

      // Obtener turnos disponibles para cada cancha
      const turnosMap: Record<number, Turno[]> = {}
      for (const cancha of canchasActivas) {
        try {
          let turnosCancha = await turnosApi.listByCancha(cancha.id)
          
          // Filtrar por fecha si hay filtro activo
          if (fechaAplicada) {
            const fechaInicio = new Date(fechaAplicada + 'T00:00:00')
            const fechaFin = new Date(fechaAplicada + 'T23:59:59')
            
            turnosCancha = turnosCancha.filter(t => {
              const fechaTurno = new Date(t.fecha_hora_inicio)
              return fechaTurno >= fechaInicio && fechaTurno <= fechaFin
            })
          }
          
          // Filtrar solo turnos disponibles
          turnosMap[cancha.id] = turnosCancha
            .filter(t => t.estado === 'disponible')
            .slice(0, 10) // Mostrar los próximos 10
        } catch (err) {
          turnosMap[cancha.id] = []
        }
      }
      setTurnosPorCancha(turnosMap)
    } catch (err) {
      console.error('Error cargando datos:', err)
      setError('No se pudieron cargar las canchas. Intenta nuevamente.')
    } finally {
      setLoading(false)
    }
  }

  // Función para normalizar strings (quita tildes, espacios extra, etc.)
  const normalizarTexto = (texto?: string) => {
    if (!texto) return ''
    return texto
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '') // Quitar tildes
      .trim()
  }

  const canchasFiltradas = deporteFilter === 'todos' 
    ? canchas 
    : canchas.filter(c => normalizarTexto(c.tipo_deporte) === normalizarTexto(deporteFilter))

  const formatearFecha = (isoString: string) => {
    const fecha = new Date(isoString)
    return fecha.toLocaleDateString('es-AR', { 
      weekday: 'short', 
      day: 'numeric', 
      month: 'short',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const handleReservar = (turno: Turno, cancha: Cancha) => {
    if (!user) {
      openModal('login')
      return
    }
    // Navegar a la página de pago con los datos del turno, cancha y servicios disponibles
    navigate('/reservas/pago', { 
      state: { 
        turno, 
        cancha,
        serviciosDisponibles
      } 
    })
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center">
        <div className="text-white text-xl">Cargando canchas disponibles...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Canchas Disponibles</h1>
          <p className="text-slate-300">Explora nuestras canchas y horarios disponibles</p>
        </div>

        {error && (
          <div className="mb-6 bg-red-500/10 border border-red-500/50 rounded-lg p-4 text-red-200">
            {error}
          </div>
        )}

        {/* Filtros */}
        <div className="mb-6 space-y-4">
          {/* Filtros de deporte */}
          <div className="flex gap-3 flex-wrap">
            <button
              onClick={() => setDeporteFilter('todos')}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                deporteFilter === 'todos'
                  ? 'bg-emerald-500 text-white'
                  : 'bg-white/10 text-white/70 hover:bg-white/20'
              }`}
            >
              Todas
            </button>
            <button
              onClick={() => setDeporteFilter('futbol')}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                deporteFilter === 'futbol'
                  ? 'bg-emerald-500 text-white'
                  : 'bg-white/10 text-white/70 hover:bg-white/20'
              }`}
            >
              Fútbol
            </button>
            <button
              onClick={() => setDeporteFilter('basquet')}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                deporteFilter === 'basquet'
                  ? 'bg-emerald-500 text-white'
                  : 'bg-white/10 text-white/70 hover:bg-white/20'
              }`}
            >
              Básquet
            </button>
            <button
              onClick={() => setDeporteFilter('padel')}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                deporteFilter === 'padel'
                  ? 'bg-emerald-500 text-white'
                  : 'bg-white/10 text-white/70 hover:bg-white/20'
              }`}
            >
              Pádel
            </button>
          </div>
          
          {/* Filtro de fecha */}
          <div className="flex gap-3 items-center">
            <label className="text-sm font-medium text-slate-300">
              Filtrar por fecha:
            </label>
            <input
              type="date"
              value={fechaFilter}
              onChange={(e) => setFechaFilter(e.target.value)}
              className="px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
            />
            <button
              onClick={() => setFechaAplicada(fechaFilter)}
              className="px-4 py-2 rounded-lg bg-emerald-500 hover:bg-emerald-600 text-white font-medium transition-all"
            >
              Buscar
            </button>
            {fechaAplicada && (
              <button
                onClick={() => {
                  setFechaFilter('')
                  setFechaAplicada('')
                }}
                className="px-4 py-2 rounded-lg bg-white/10 text-white/70 hover:bg-white/20 font-medium transition-all"
              >
                Limpiar
              </button>
            )}
          </div>
        </div>

        {/* Grid de Canchas */}
        {canchasFiltradas.length === 0 ? (
          <div className="text-center py-12 bg-white/5 rounded-xl">
            <p className="text-slate-400 text-lg">No hay canchas disponibles en esta categoría</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {canchasFiltradas.map((cancha) => (
              <div
                key={cancha.id}
                className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/10 hover:border-emerald-500/50 transition-all"
              >
                {/* Info de la cancha */}
                <div className="mb-4">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <h3 className="text-2xl font-bold text-white">{cancha.nombre}</h3>
                      <p className="text-emerald-400 font-medium">
                        {cancha.tipo_deporte || 'Deporte no especificado'}
                      </p>
                    </div>
                    {cancha.precio_hora && (
                      <div className="bg-emerald-500/20 border border-emerald-500/50 rounded-lg px-3 py-1">
                        <span className="text-emerald-300 font-bold">${cancha.precio_hora}</span>
                        <span className="text-emerald-200 text-sm">/hora</span>
                      </div>
                    )}
                  </div>
                  {cancha.descripcion && (
                    <p className="text-slate-300 text-sm">{cancha.descripcion}</p>
                  )}
                </div>

                {/* Turnos disponibles */}
                <div>
                  <h4 className="text-sm font-semibold text-slate-300 mb-3 uppercase tracking-wide">
                    Próximos Turnos Disponibles
                  </h4>
                  {!turnosPorCancha[cancha.id] || turnosPorCancha[cancha.id].length === 0 ? (
                    <p className="text-slate-400 text-sm italic">No hay turnos disponibles</p>
                  ) : (
                    <div className="space-y-2">
                      {turnosPorCancha[cancha.id].map((turno) => (
                        <div
                          key={turno.id}
                          className="bg-slate-800/50 rounded-lg p-3 border border-slate-700/50 hover:border-slate-600 transition-all"
                        >
                          <div className="flex items-center justify-between">
                            <div className="flex-1">
                              <p className="text-white font-medium text-sm">
                                {formatearFecha(turno.fecha_hora_inicio)}
                              </p>
                              <p className="text-slate-400 text-xs">
                                {new Date(turno.fecha_hora_inicio).toLocaleTimeString('es-AR', { 
                                  hour: '2-digit', 
                                  minute: '2-digit' 
                                })} - {new Date(turno.fecha_hora_fin).toLocaleTimeString('es-AR', { 
                                  hour: '2-digit', 
                                  minute: '2-digit' 
                                })}
                              </p>
                            </div>
                            <div className="flex items-center gap-3">
                              <div className="text-right">
                                <p className="text-emerald-400 font-bold">${turno.precio_final}</p>
                              </div>
                              {isAuthenticated && (
                                <button
                                  onClick={() => handleReservar(turno, cancha)}
                                  className="bg-emerald-500 hover:bg-emerald-600 text-white text-xs font-medium px-3 py-1.5 rounded-lg transition-colors"
                                >
                                  Reservar
                                </button>
                              )}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {/* Call to action */}
                {!isAuthenticated && (
                  <div className="mt-4 pt-4 border-t border-white/10">
                    <p className="text-sm text-slate-400 text-center">
                      <button 
                        onClick={() => openModal('login')} 
                        className="text-emerald-400 hover:text-emerald-300 font-medium underline-offset-2 hover:underline cursor-pointer bg-transparent border-none"
                      >
                        Inicia sesión
                      </button>{' '}
                      para reservar turnos
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
