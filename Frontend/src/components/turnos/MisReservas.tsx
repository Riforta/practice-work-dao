import { useEffect, useState } from 'react'
import { useAuth } from '../../contexts/AuthContext'
import turnosApi, { type Turno } from '../../services/turnos.service'

const currency = new Intl.NumberFormat('es-AR', { 
  style: 'currency', 
  currency: 'ARS', 
  maximumFractionDigits: 0 
})

/**
 * Componente para que los clientes vean y gestionen sus propias reservas
 */
export default function MisReservas() {
  const { user } = useAuth()
  const [reservas, setReservas] = useState<Turno[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  // Obtener el ID del cliente desde el usuario autenticado
  const clienteId = user?.id_cliente ?? null

  useEffect(() => {
    if (clienteId) {
      cargarReservas()
    } else if (!user) {
      setError('Debes iniciar sesión para ver tus reservas')
      setLoading(false)
    } else {
      setError('Tu usuario no tiene un perfil de cliente asociado. Contacta al administrador.')
      setLoading(false)
    }
  }, [clienteId, user])

  const cargarReservas = async () => {
    if (!clienteId) return
    
    try {
      setLoading(true)
      setError('')
      const res = await turnosApi.listByCliente(clienteId)
      setReservas(res)
    } catch (err) {
      console.error('Error cargando reservas:', err)
      setError('No se pudieron cargar tus reservas')
    } finally {
      setLoading(false)
    }
  }

  const cancelarReserva = async (turnoId: number) => {
    const confirmacion = window.confirm(
      '¿Estás seguro de que deseas cancelar esta reserva? Esta acción no se puede deshacer.'
    )
    
    if (!confirmacion) return

    try {
      setLoading(true)
      setError('')
      await turnosApi.cancelarReserva(turnoId)
      await cargarReservas() // Recargar lista después de cancelar
    } catch (err) {
      console.error('Error cancelando reserva:', err)
      setError('No se pudo cancelar la reserva. Intenta nuevamente.')
    } finally {
      setLoading(false)
    }
  }

  const formatearFecha = (isoString: string) => {
    const fecha = new Date(isoString)
    return fecha.toLocaleDateString('es-AR', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    })
  }

  const formatearHora = (isoString: string) => {
    const fecha = new Date(isoString)
    return fecha.toLocaleTimeString('es-AR', {
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  const obtenerColorEstado = (estado: string) => {
    switch (estado) {
      case 'disponible':
        return 'bg-emerald-500/20 text-emerald-300 border-emerald-500/50'
      case 'reservado':
        return 'bg-blue-500/20 text-blue-300 border-blue-500/50'
      case 'confirmado':
        return 'bg-green-500/20 text-green-300 border-green-500/50'
      case 'cancelado':
        return 'bg-red-500/20 text-red-300 border-red-500/50'
      case 'pendiente_pago':
        return 'bg-yellow-500/20 text-yellow-300 border-yellow-500/50'
      default:
        return 'bg-slate-500/20 text-slate-300 border-slate-500/50'
    }
  }

  const puedeModificar = (estado: string) => {
    return estado === 'pendiente_pago' || estado === 'reservado'
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center">
        <div className="text-white text-xl">Cargando tus reservas...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Mis Reservas</h1>
          <p className="text-slate-300">
            Gestiona tus reservas activas y revisa tu historial
          </p>
        </div>

        {error && (
          <div className="mb-6 bg-red-500/10 border border-red-500/50 rounded-lg p-4 text-red-200">
            {error}
          </div>
        )}

        {/* Lista de reservas */}
        {reservas.length === 0 ? (
          <div className="text-center py-12 bg-white/5 rounded-xl">
            <p className="text-slate-400 text-lg mb-4">No tienes reservas</p>
            <a
              href="/canchas-publicas"
              className="inline-block bg-emerald-500 hover:bg-emerald-600 text-white font-medium px-6 py-3 rounded-lg transition-colors"
            >
              Explorar canchas disponibles
            </a>
          </div>
        ) : (
          <div className="space-y-4">
            {reservas.map((reserva) => (
              <div
                key={reserva.id}
                className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/10 hover:border-emerald-500/50 transition-all"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-xl font-bold">
                        Cancha #{reserva.id_cancha}
                      </h3>
                      <span
                        className={`px-3 py-1 rounded-full text-xs font-medium border ${obtenerColorEstado(
                          reserva.estado
                        )}`}
                      >
                        {reserva.estado.replace('_', ' ').toUpperCase()}
                      </span>
                    </div>
                    
                    <div className="space-y-1 text-slate-300">
                      <p className="text-sm">
                        <span className="font-medium">📅 Fecha:</span>{' '}
                        {formatearFecha(reserva.fecha_hora_inicio)}
                      </p>
                      <p className="text-sm">
                        <span className="font-medium">🕐 Horario:</span>{' '}
                        {formatearHora(reserva.fecha_hora_inicio)} -{' '}
                        {formatearHora(reserva.fecha_hora_fin)}
                      </p>
                      {reserva.precio_final && (
                        <p className="text-sm">
                          <span className="font-medium">💰 Precio:</span>{' '}
                          <span className="text-emerald-400 font-bold">
                            {currency.format(reserva.precio_final)}
                          </span>
                        </p>
                      )}
                    </div>
                  </div>

                  {/* Acciones */}
                  <div className="flex flex-col gap-2">
                    {puedeModificar(reserva.estado) && reserva.id && (
                      <button
                        onClick={() => cancelarReserva(reserva.id!)}
                        className="bg-red-500/20 hover:bg-red-500/30 text-red-300 border border-red-500/50 hover:border-red-500 px-4 py-2 rounded-lg text-sm font-medium transition-all"
                        disabled={loading}
                      >
                        Cancelar
                      </button>
                    )}
                  </div>
                </div>

                {/* Información adicional si está pendiente de pago */}
                {reserva.estado === 'pendiente_pago' && (
                  <div className="mt-4 pt-4 border-t border-white/10">
                    <p className="text-sm text-yellow-300">
                      ⚠️ Esta reserva está pendiente de pago. Completa el pago
                      para confirmarla.
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Botón para recargar */}
        <div className="mt-8 text-center">
          <button
            onClick={cargarReservas}
            disabled={loading}
            className="bg-white/10 hover:bg-white/20 text-white border border-white/20 px-6 py-3 rounded-lg font-medium transition-all disabled:opacity-50"
          >
            {loading ? 'Cargando...' : 'Actualizar lista'}
          </button>
        </div>
      </div>
    </div>
  )
}
