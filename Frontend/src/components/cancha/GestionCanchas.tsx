import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

interface Cancha {
  id?: number;
  nombre: string;
  tipo_deporte: string;
  descripcion: string;
  activa: boolean;
}

const GestionCanchas: React.FC = () => {
  const navigate = useNavigate();
  const [canchas, setCanchas] = useState<Cancha[]>([]);
  const [filteredCanchas, setFilteredCanchas] = useState<Cancha[]>([]);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Filtros
  const [filterNombre, setFilterNombre] = useState('');
  const [filterTipoDeporte, setFilterTipoDeporte] = useState('todos');
  const [filterEstado, setFilterEstado] = useState('todos');

  const cargarCanchas = async () => {
    try {
      setLoading(true);
      setErrorMsg(null);
      const resp = await fetch(`${API_BASE_URL}/api/canchas/`);
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const data: Cancha[] = await resp.json();
      setCanchas(data);
      setFilteredCanchas(data);
    } catch (err: any) {
      setErrorMsg('Error al cargar las canchas');
    } finally {
      setLoading(false);
    }
  };

  const eliminarCancha = async (id: number) => {
    if (!window.confirm('¿Estás seguro de eliminar esta cancha?')) return;
    
    try {
      const resp = await fetch(`${API_BASE_URL}/api/canchas/${id}`, { method: 'DELETE' });
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      await cargarCanchas();
    } catch {
      setErrorMsg('No se pudo eliminar la cancha');
    }
  };

  const limpiarFiltros = () => {
    setFilterNombre('');
    setFilterTipoDeporte('todos');
    setFilterEstado('todos');
  };

  useEffect(() => {
    cargarCanchas();
  }, []);

  useEffect(() => {
    let result = [...canchas];
    if (filterNombre) {
      result = result.filter((c) =>
        c.nombre.toLowerCase().includes(filterNombre.toLowerCase())
      );
    }
    if (filterTipoDeporte && filterTipoDeporte !== 'todos') {
      result = result.filter((c) =>
        c.tipo_deporte.toLowerCase() === filterTipoDeporte.toLowerCase()
      );
    }
    if (filterEstado && filterEstado !== 'todos') {
      result = result.filter((c) =>
        filterEstado === 'activas' ? c.activa : !c.activa
      );
    }
    setFilteredCanchas(result);
  }, [filterNombre, filterTipoDeporte, filterEstado, canchas]);

  return (
    <div className="min-h-screen bg-slate-950 text-white px-4 py-10">
      <div className="max-w-6xl mx-auto space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <p className="text-sm uppercase tracking-widest text-emerald-200">Canchas</p>
            <h1 className="text-3xl font-bold">Gestión de Canchas</h1>
            {errorMsg && <p className="text-red-300 text-sm mt-2">{errorMsg}</p>}
          </div>
          <div className="flex flex-nowrap gap-3">
            <button onClick={() => cargarCanchas()} className="rounded-lg bg-white/10 px-4 py-2 text-sm font-semibold text-emerald-100 hover:bg-white/20">
              Refrescar
            </button>
            <Link to="/canchas/nuevo" className="rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400 whitespace-nowrap">
              + Registrar Cancha
            </Link>
          </div>
        </div>

        <section className="bg-white/10 backdrop-blur-md rounded-2xl p-4 shadow-lg border border-white/10">
          <div className="flex flex-col gap-3">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              <label className="text-sm text-emerald-100">
                Filtrar por nombre
                <input
                  type="text"
                  value={filterNombre}
                  onChange={(e) => setFilterNombre(e.target.value)}
                  placeholder="Todos"
                  className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
                />
              </label>
              <label className="text-sm text-emerald-100">
                Filtrar por tipo de deporte
                <select
                  value={filterTipoDeporte}
                  onChange={(e) => setFilterTipoDeporte(e.target.value)}
                  className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
                >
                  <option value="todos">Todos</option>
                  <option value="futbol">Fútbol</option>
                  <option value="basquet">Básquet</option>
                  <option value="padel">Pádel</option>
                </select>
              </label>
              <label className="text-sm text-emerald-100">
                Filtrar por estado
                <select
                  value={filterEstado}
                  onChange={(e) => setFilterEstado(e.target.value)}
                  className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
                >
                  <option value="todos">Todos</option>
                  <option value="activas">Activas</option>
                  <option value="inactivas">Inactivas</option>
                </select>
              </label>
            </div>
            {(filterNombre || filterTipoDeporte !== 'todos' || filterEstado !== 'todos') && (
              <div className="flex justify-end">
                <button
                  onClick={limpiarFiltros}
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
                  <th className="px-4 py-3 text-left">ID</th>
                  <th className="px-4 py-3 text-left">Nombre</th>
                  <th className="px-4 py-3 text-left">Tipo de Deporte</th>
                  <th className="px-4 py-3 text-left">Descripción</th>
                  <th className="px-4 py-3 text-left">Estado</th>
                  <th className="px-4 py-3 text-right">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr>
                    <td className="px-4 py-6 text-center text-emerald-100" colSpan={6}>Cargando canchas...</td>
                  </tr>
                ) : filteredCanchas.length === 0 ? (
                  <tr>
                    <td className="px-4 py-6 text-center text-emerald-100" colSpan={6}>No se encontraron canchas</td>
                  </tr>
                ) : (
                  filteredCanchas.map((cancha) => (
                    <tr
                      key={cancha.id}
                      className="border-t border-white/5 hover:bg-white/5"
                    >
                      <td className="px-4 py-3 text-emerald-100">{cancha.id}</td>
                      <td className="px-4 py-3 text-emerald-100">{cancha.nombre}</td>
                      <td className="px-4 py-3 text-emerald-100 capitalize">{cancha.tipo_deporte}</td>
                      <td className="px-4 py-3 text-emerald-100">{cancha.descripcion || '-'}</td>
                      <td className="px-4 py-3 text-emerald-100">
                        {cancha.activa ? 'Activa' : 'Inactiva'}
                      </td>
                      <td className="px-4 py-3 text-right space-x-2">
                        <button className="rounded-lg bg-white/10 px-3 py-1 text-xs font-semibold text-emerald-100 hover:bg-white/20" onClick={() => navigate(`/canchas/${cancha.id}/editar`)}>Editar</button>
                        <button className="rounded-lg bg-red-500/80 px-3 py-1 text-xs font-semibold text-white hover:bg-red-500" onClick={() => cancha.id && eliminarCancha(cancha.id)}>Eliminar</button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </section>

        <div className="text-center">
          <Link to="/" className="inline-block rounded-lg border border-white/20 bg-white/5 px-4 py-2 text-sm text-emerald-100 hover:border-emerald-400 hover:text-white">
            Volver al inicio
          </Link>
        </div>
      </div>
    </div>
  );
};

export default GestionCanchas;
