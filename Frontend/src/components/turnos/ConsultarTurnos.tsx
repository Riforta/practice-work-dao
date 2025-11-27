import { useEffect, useMemo, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import turnosApi from '../../services/turnos.service';
import type { Turno, CanchaRef } from '../../services/turnos.service';

const estados = ['todos', 'disponible', 'reservado', 'bloqueado', 'cancelado', 'finalizado'];
const currency = new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS', maximumFractionDigits: 0 });

const formatDate = (value: string) => {
  if (!value) return '-';
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toLocaleString('es-AR', { dateStyle: 'short', timeStyle: 'short' });
};

export default function ConsultarTurnos() {
  const [turnos, setTurnos] = useState<Turno[]>([]);
  const [canchas, setCanchas] = useState<CanchaRef[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [estadoFiltro, setEstadoFiltro] = useState<string>('todos');
  const [canchaFiltro, setCanchaFiltro] = useState<number | 'todos'>('todos');
  const navigate = useNavigate();

  const loadData = async () => {
    setLoading(true);
    setError('');
    try {
      const [t, c] = await Promise.all([turnosApi.list(), turnosApi.listCanchas()]);
      setTurnos(t);
      setCanchas(c);
    } catch (err) {
      console.error(err);
      setError('No se pudieron cargar los turnos.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadData();
  }, []);

  const canchaMap = useMemo(() => {
    const map = new Map<number, CanchaRef>();
    canchas.forEach((c) => map.set(c.id, c));
    return map;
  }, [canchas]);

  const filtered = useMemo(() => {
    return turnos.filter((t) => {
      const pasaEstado = estadoFiltro === 'todos' ? true : t.estado === estadoFiltro;
      const pasaCancha = canchaFiltro === 'todos' ? true : t.id_cancha === canchaFiltro;
      return pasaEstado && pasaCancha;
    });
  }, [turnos, estadoFiltro, canchaFiltro]);

  const handleDelete = async (id?: number) => {
    if (!id) return;
    const confirm = window.confirm('¿Seguro que deseas eliminar este turno?');
    if (!confirm) return;
    setError('');
    setLoading(true);
    try {
      await turnosApi.remove(id);
      await loadData();
    } catch (err) {
      console.error(err);
      setError('No se pudo eliminar el turno.');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white px-4 py-10">
      <div className="max-w-6xl mx-auto space-y-6">
        <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <p className="text-sm uppercase tracking-widest text-emerald-200">Turnos</p>
            <h1 className="text-3xl font-bold">Gestión de turnos</h1>
            {error && <p className="text-red-300 text-sm mt-2">{error}</p>}
          </div>
          <div className="flex flex-nowrap gap-3">
            <button
              onClick={() => void loadData()}
              className="rounded-lg bg-white/10 px-4 py-2 text-sm font-semibold text-emerald-100 hover:bg-white/20 disabled:opacity-60"
              disabled={loading}
            >
              {loading ? 'Actualizando...' : 'Refrescar'}
            </button>
            <Link
              to="/turnos/nuevo"
              className="rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400 whitespace-nowrap"
            >
              + Registrar turno
            </Link>
          </div>
        </header>

        <section className="bg-white/10 backdrop-blur-md rounded-2xl p-4 shadow-lg border border-white/10">
          <div className="flex flex-col gap-3">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <label className="text-sm text-emerald-100">
                Filtrar por estado
                <select
                  value={estadoFiltro}
                  onChange={(e) => setEstadoFiltro(e.target.value)}
                  className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
                >
                  {estados.map((est) => (
                    <option key={est} value={est} className="bg-slate-900">
                      {est === 'todos' ? 'Todos' : est}
                    </option>
                  ))}
                </select>
              </label>

              <label className="text-sm text-emerald-100 sm:col-span-2">
                Filtrar por cancha
                <select
                  value={canchaFiltro}
                  onChange={(e) => setCanchaFiltro(e.target.value === 'todos' ? 'todos' : Number(e.target.value))}
                  className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
                >
                  <option value="todos" className="bg-slate-900">
                    Todas
                  </option>
                  {canchas.map((c) => (
                    <option key={c.id} value={c.id} className="bg-slate-900">
                      {c.nombre} {c.tipo_deporte ? `(${c.tipo_deporte})` : ''}
                    </option>
                  ))}
                </select>
              </label>
            </div>
            {(estadoFiltro !== 'todos' || canchaFiltro !== 'todos') && (
              <div className="flex justify-end">
                <button
                  onClick={() => { setEstadoFiltro('todos'); setCanchaFiltro('todos'); }}
                  className="rounded-lg border border-white/20 px-3 py-2 text-sm text-emerald-100 hover:border-emerald-400 hover:text-white"
                >
                  Limpiar filtros
                </button>
              </div>
            )}
          </div>
        </section>

        <section className="bg-white/5 backdrop-blur-md rounded-2xl border border-white/10 shadow-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full text-sm">
              <thead className="bg-white/10 text-emerald-100 uppercase text-xs tracking-wider">
                <tr>
                  <th className="px-4 py-3 text-left">Cancha</th>
                  <th className="px-4 py-3 text-left">Inicio</th>
                  <th className="px-4 py-3 text-left">Fin</th>
                  <th className="px-4 py-3 text-left">Estado</th>
                  <th className="px-4 py-3 text-left">Precio</th>
                  <th className="px-4 py-3 text-right">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr>
                    <td className="px-4 py-6 text-center text-emerald-100" colSpan={6}>
                      Cargando turnos...
                    </td>
                  </tr>
                ) : filtered.length === 0 ? (
                  <tr>
                    <td className="px-4 py-6 text-center text-emerald-100" colSpan={6}>
                      No hay turnos para mostrar.
                    </td>
                  </tr>
                ) : (
                  filtered.map((t) => (
                    <tr key={t.id} className="border-t border-white/5 hover:bg-white/5">
                      <td className="px-4 py-3 font-semibold">
                        {canchaMap.get(t.id_cancha)?.nombre ?? `Cancha ${t.id_cancha}`}
                      </td>
                      <td className="px-4 py-3 text-emerald-100">{formatDate(t.fecha_hora_inicio)}</td>
                      <td className="px-4 py-3 text-emerald-100">{formatDate(t.fecha_hora_fin)}</td>
                      <td className="px-4 py-3">
                        <span
                          className={`inline-flex items-center gap-2 rounded-full px-3 py-1 text-xs font-semibold ${
                            t.estado === 'disponible'
                              ? 'bg-emerald-500/20 text-emerald-100'
                              : t.estado === 'reservado'
                                ? 'bg-blue-500/20 text-blue-100'
                                : t.estado === 'bloqueado'
                                  ? 'bg-yellow-500/20 text-yellow-100'
                                  : t.estado === 'cancelado'
                                    ? 'bg-red-500/20 text-red-100'
                                    : 'bg-white/10 text-white'
                          }`}
                        >
                          <span className="size-2 rounded-full bg-white/80" />
                          {t.estado}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-emerald-100">{currency.format(t.precio_final)}</td>
                      <td className="px-4 py-3 text-right space-x-2">
                        <button
                          onClick={() => navigate(`/turnos/${t.id}/editar`)}
                          className="rounded-lg bg-white/10 px-3 py-1 text-xs font-semibold text-emerald-100 hover:bg-white/20"
                        >
                          Editar
                        </button>
                        <button
                          onClick={() => void handleDelete(t.id)}
                          className="rounded-lg bg-red-500/80 px-3 py-1 text-xs font-semibold text-white hover:bg-red-500"
                        >
                          Eliminar
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </section>

        <div className="text-center">
          <Link
            to="/"
            className="inline-block rounded-lg border border-white/20 bg-white/5 px-4 py-2 text-sm text-emerald-100 hover:border-emerald-400 hover:text-white"
          >
            Volver al inicio
          </Link>
        </div>
      </div>
    </div>
  );
}
