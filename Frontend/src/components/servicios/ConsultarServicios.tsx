import React, { useEffect, useMemo, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import serviciosApi from '../../services/servicios.service';
import type { ServicioAdicional } from '../../services/servicios.service';

const currency = new Intl.NumberFormat('es-AR', {
  style: 'currency',
  currency: 'ARS',
  maximumFractionDigits: 2,
});

export default function ConsultarServicios() {
  const [servicios, setServicios] = useState<ServicioAdicional[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [search, setSearch] = useState('');
  const navigate = useNavigate();

  const loadServicios = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await serviciosApi.list();
      setServicios(data);
    } catch (err) {
      console.error(err);
      setError('No se pudieron cargar los servicios. Intenta nuevamente.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadServicios();
  }, []);

  const filtered = useMemo(() => {
    const term = search.trim().toLowerCase();
    if (!term) return servicios;
    return servicios.filter((s) => s.nombre.toLowerCase().includes(term));
  }, [search, servicios]);

  const handleDelete = async (id?: number) => {
    if (!id) return;
    const confirm = window.confirm('¿Seguro que deseas eliminar este servicio?');
    if (!confirm) return;

    setError('');
    setLoading(true);
    try {
      await serviciosApi.remove(id);
      await loadServicios();
    } catch (err) {
      console.error(err);
      setError('No se pudo eliminar el servicio.');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white px-4 py-10">
      <div className="max-w-5xl mx-auto space-y-6">
        <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <p className="text-sm uppercase tracking-widest text-emerald-200">Servicios adicionales</p>
            <h1 className="text-3xl font-bold">Gestión de servicios</h1>
            {error && <p className="text-red-300 text-sm mt-2">{error}</p>}
          </div>
          <div className="flex gap-3">
            <button
              onClick={() => void loadServicios()}
              className="rounded-lg bg-white/10 px-4 py-2 text-sm font-semibold text-emerald-100 hover:bg-white/20 disabled:opacity-60"
              disabled={loading}
            >
              {loading ? 'Actualizando...' : 'Refrescar'}
            </button>
            <Link
              to="/servicios/nuevo"
              className="rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400"
            >
              + Registrar servicio
            </Link>
          </div>
        </header>

        <section className="bg-white/10 backdrop-blur-md rounded-2xl p-4 shadow-lg border border-white/10">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <label className="text-sm text-emerald-100">
              Buscá por nombre
              <input
                type="text"
                className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white placeholder:text-emerald-200/60 focus:outline-none focus:ring-2 focus:ring-emerald-400"
                placeholder="Ej: Buffet, Estacionamiento..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </label>
            <button
              onClick={() => setSearch('')}
              className="self-start rounded-lg border border-white/20 px-3 py-2 text-sm text-emerald-100 hover:border-emerald-400 hover:text-white"
            >
              Limpiar filtro
            </button>
          </div>
        </section>

        <section className="bg-white/5 backdrop-blur-md rounded-2xl border border-white/10 shadow-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full text-sm">
              <thead className="bg-white/10 text-emerald-100 uppercase text-xs tracking-wider">
                <tr>
                  <th className="px-4 py-3 text-left">Nombre</th>
                  <th className="px-4 py-3 text-left">Precio actual</th>
                  <th className="px-4 py-3 text-left">Estado</th>
                  <th className="px-4 py-3 text-right">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr>
                    <td className="px-4 py-6 text-center text-emerald-100" colSpan={4}>
                      Cargando servicios...
                    </td>
                  </tr>
                ) : filtered.length === 0 ? (
                  <tr>
                    <td className="px-4 py-6 text-center text-emerald-100" colSpan={4}>
                      No hay servicios para mostrar.
                    </td>
                  </tr>
                ) : (
                  filtered.map((servicio) => (
                    <tr key={servicio.id} className="border-t border-white/5 hover:bg-white/5">
                      <td className="px-4 py-3 font-semibold">{servicio.nombre}</td>
                      <td className="px-4 py-3 text-emerald-100">{currency.format(servicio.precio_actual)}</td>
                      <td className="px-4 py-3">
                        <span
                          className={`inline-flex items-center gap-2 rounded-full px-3 py-1 text-xs font-semibold ${
                            servicio.activo ? 'bg-emerald-500/20 text-emerald-100' : 'bg-red-500/20 text-red-100'
                          }`}
                        >
                          <span className={`size-2 rounded-full ${servicio.activo ? 'bg-emerald-300' : 'bg-red-300'}`} />
                          {servicio.activo ? 'Activo' : 'Inactivo'}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-right space-x-2">
                        <button
                          onClick={() => navigate(`/servicios/${servicio.id}/editar`)}
                          className="rounded-lg bg-white/10 px-3 py-1 text-xs font-semibold text-emerald-100 hover:bg-white/20"
                        >
                          Editar
                        </button>
                        <button
                          onClick={() => void handleDelete(servicio.id)}
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
