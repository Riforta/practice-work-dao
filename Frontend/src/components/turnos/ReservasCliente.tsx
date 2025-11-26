import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import turnosApi, { type Turno, type CanchaRef } from '../../services/turnos.service';

type Disponibilidad = {
  turno: Turno;
  cancha: CanchaRef;
};

const currency = new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS', maximumFractionDigits: 0 });

const normalizarDeporte = (v: string | undefined) =>
  (v ?? '')
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .trim();

export default function ReservasCliente() {
  const { user } = useAuth();
  const [deporte, setDeporte] = useState('');
  const [fecha, setFecha] = useState('');
  const [canchas, setCanchas] = useState<CanchaRef[]>([]);
  const [disponibles, setDisponibles] = useState<Disponibilidad[]>([]);
  const [reservas, setReservas] = useState<Turno[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const clienteSesionId = useMemo(() => {
    if (!user) return null;
    return user.id_cliente ?? user.cliente_id ?? null;
  }, [user]);

  useEffect(() => {
    const loadCanchas = async () => {
      try {
        const c = await turnosApi.listCanchas();
        setCanchas(c);
      } catch (err) {
        console.error(err);
        setError('No se pudieron cargar las canchas.');
      }
    };
    void loadCanchas();
  }, []);

  const canchasPorDeporte = useMemo(() => {
    const target = normalizarDeporte(deporte);
    if (!target) return canchas;
    return canchas.filter((c) => normalizarDeporte(c.tipo_deporte).includes(target));
  }, [canchas, deporte]);

  const cargarReservasCliente = async (clienteId: number) => {
    try {
      const res = await turnosApi.listByCliente(clienteId);
      setReservas(res);
    } catch (err) {
      console.error(err);
      setReservas([]);
    }
  };

  const buscar = async () => {
    setError('');
    setDisponibles([]);
    if (!deporte) {
      setError('Selecciona un deporte.');
      return;
    }
    if (!fecha) {
      setError('Selecciona una fecha.');
      return;
    }
    if (canchasPorDeporte.length === 0) {
      setError('No hay canchas para ese deporte.');
      return;
    }
    setLoading(true);
    try {
      const inicio = `${fecha}T00:00`;
      const fin = `${fecha}T23:59`;
      const resultados: Disponibilidad[] = [];
      for (const cancha of canchasPorDeporte) {
        const turnos = await turnosApi.searchDisponibles(cancha.id, inicio, fin);
        turnos
          .filter((t) => t.estado === 'disponible')
          .forEach((t) => resultados.push({ turno: t, cancha }));
      }
      setDisponibles(resultados);
    } catch (err) {
      console.error(err);
      setError('No se pudieron buscar los turnos disponibles.');
    } finally {
      setLoading(false);
    }
  };

  const seleccionarTurno = (item: Disponibilidad) => {
    if (!clienteSesionId) {
      setError('Inicia sesión para reservar turnos.');
      return;
    }
    navigate('/reservas/pago', { state: item });
  };

  const cancelarReserva = async (turnoId?: number) => {
    if (!turnoId) return;
    if (!clienteSesionId) {
      setError('Inicia sesión para gestionar tus reservas.');
      return;
    }
    const ok = window.confirm('Si cancelas no habrá reembolso. ¿Deseas continuar?');
    if (!ok) return;
    setLoading(true);
    setError('');
    try {
      await turnosApi.cancelarReserva(turnoId);
      await cargarReservasCliente(clienteSesionId);
    } catch (err) {
      console.error(err);
      setError('No se pudo cancelar la reserva.');
    } finally {
      setLoading(false);
    }
  };

  const onConsultarMisReservas = async () => {
    setError('');
    if (!clienteSesionId) {
      setError('Inicia sesión para ver tus reservas.');
      return;
    }
    setLoading(true);
    try {
      await cargarReservasCliente(clienteSesionId);
    } catch (err) {
      console.error(err);
      setError('No se pudieron cargar tus reservas.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white px-4 py-10">
      <div className="max-w-6xl mx-auto space-y-8">
        <header className="space-y-2">
          <p className="text-sm uppercase tracking-widest text-emerald-200">Reservas</p>
          <h1 className="text-3xl font-bold">Buscar y reservar turno</h1>
          {error && <p className="text-red-300 text-sm">{error}</p>}
        </header>

        <section className="grid gap-4">
          <div className="rounded-2xl bg-white/10 border border-white/10 p-5 shadow-xl backdrop-blur-md space-y-4">
            <div className="grid gap-3 md:grid-cols-2">
              <label className="text-sm">
                Deporte
                <select
                  value={deporte}
                  onChange={(e) => setDeporte(e.target.value)}
                  className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
                >
                  <option value="">Selecciona un deporte</option>
                  <option value="futbol">Fútbol</option>
                  <option value="basquet">Básquet</option>
                  <option value="padel">Pádel</option>
                </select>
              </label>
              <label className="text-sm">
                Fecha
                <input
                  type="date"
                  value={fecha}
                  onChange={(e) => setFecha(e.target.value)}
                  className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
                />
              </label>
            </div>
            <div className="flex flex-wrap gap-3">
              <button
                onClick={() => void buscar()}
                className="rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400 disabled:opacity-60"
                disabled={loading}
              >
                {loading ? 'Buscando...' : 'Buscar turnos'}
              </button>
            </div>

            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold">Resultados</h2>
                <span className="text-sm text-emerald-100/80">{disponibles.length} turnos</span>
              </div>
              <div className="grid gap-3">
                {loading ? (
                  <p className="text-emerald-100">Cargando...</p>
                ) : disponibles.length === 0 ? (
                  <p className="text-emerald-100/80">No hay turnos disponibles para esos filtros.</p>
                ) : (
                  disponibles.map((item) => (
                    <div
                      key={`${item.turno.id}-${item.turno.fecha_hora_inicio}`}
                      className="rounded-xl border border-white/10 bg-white/5 p-4 flex flex-col md:flex-row md:items-center md:justify-between gap-3"
                    >
                      <div>
                        <p className="text-sm text-emerald-200">{item.cancha.nombre}</p>
                        <p className="text-xl font-semibold">
                          {new Date(item.turno.fecha_hora_inicio).toLocaleTimeString('es-AR', {
                            hour: '2-digit',
                            minute: '2-digit',
                          })}{' '}
                          -{' '}
                          {new Date(item.turno.fecha_hora_fin).toLocaleTimeString('es-AR', {
                            hour: '2-digit',
                            minute: '2-digit',
                          })}
                        </p>
                        <p className="text-sm text-emerald-100/80">
                          {item.cancha.tipo_deporte ?? 'Deporte'} • {currency.format(item.turno.precio_final)}
                        </p>
                      </div>
                      <button
                        onClick={() => seleccionarTurno(item)}
                        className="rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400 disabled:opacity-60"
                        disabled={loading}
                      >
                        Reservar
                      </button>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>

        </section>

        <section className="rounded-2xl bg-white/5 border border-white/10 p-5 shadow-xl backdrop-blur-md space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold">Mis reservas</h2>
            <p className="text-xs text-amber-200">Al cancelar no hay reembolso.</p>
          </div>
          <div className="flex flex-col md:flex-row md:items-end gap-3">
            <button
              onClick={() => void onConsultarMisReservas()}
              className="rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400 disabled:opacity-60"
              disabled={loading}
            >
              Ver mis reservas
            </button>
          </div>
          {loading ? (
            <p className="text-emerald-100">Cargando...</p>
          ) : reservas.length === 0 ? (
            <p className="text-emerald-100/80">Aún no tienes reservas cargadas.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full text-sm">
                <thead className="text-left text-emerald-100 uppercase text-xs tracking-wider">
                  <tr>
                    <th className="px-3 py-2">Turno</th>
                    <th className="px-3 py-2">Estado</th>
                    <th className="px-3 py-2">Precio</th>
                    <th className="px-3 py-2 text-right">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {reservas.map((r) => (
                    <tr key={r.id} className="border-t border-white/5">
                      <td className="px-3 py-2">
                        <p className="font-semibold">{new Date(r.fecha_hora_inicio).toLocaleString('es-AR')}</p>
                        <p className="text-emerald-100/70 text-xs">Cancha #{r.id_cancha}</p>
                      </td>
                      <td className="px-3 py-2">{r.estado}</td>
                      <td className="px-3 py-2">{currency.format(r.precio_final)}</td>
                      <td className="px-3 py-2 text-right">
                        <button
                          onClick={() => void cancelarReserva(r.id)}
                          className="rounded-lg bg-red-500/80 px-3 py-1 text-xs font-semibold text-white hover:bg-red-500"
                          disabled={loading}
                        >
                          Cancelar (sin reembolso)
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
