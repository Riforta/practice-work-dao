import React, { useState, useEffect } from 'react';
import service from '../../../services/canchas.service'; 
import { useNavigate } from 'react-router-dom';

export default function ConsultarCanchaFutbol() {
  const [rows, setRows] = useState<any[]>([]);
  const [filter, setFilter] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [deleteId, setDeleteId] = useState<number | null>(null);
  const navigate = useNavigate();

  const fetchCanchas = async (searchTerm = '') => {
    setLoading(true);
    setError('');
    try {
      let data;
      if (searchTerm) {
        data = await service.getCanchaFutbolByName(searchTerm);
      } else {
        data = await service.getAllCanchasFutbol();
      }
      setRows(data);
    } catch (err) {
      console.error('Error cargando canchas:', err);
      setError('No se pudieron cargar las canchas de fútbol.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const timerId = setTimeout(() => {
      fetchCanchas(filter);
    }, 500);

    return () => {
      clearTimeout(timerId);
    };
  }, [filter]);

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setFilter(event.target.value);
  };

  const handleDelete = async (id: number) => {
    if(!window.confirm("¿Seguro que quieres eliminar esta cancha?")) return;
    
    setDeleteId(id);
    try {
      await service.deleteCanchaFutbol(id);
      await fetchCanchas(filter);
    } catch (err) {
      console.error('Error al eliminar:', err);
      setError('No se pudo eliminar la cancha. Puede tener turnos asociados.');
    } finally {
      setDeleteId(null);
    }
  };

  const canchasFiltradas = filter
    ? rows.filter((c) => c.nombre.toLowerCase().includes(filter.toLowerCase()))
    : rows;

  return (
    <div className="min-h-screen bg-slate-950 text-white px-4 py-10">
      <div className="max-w-7xl mx-auto space-y-6">
        <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <p className="text-sm uppercase tracking-widest text-emerald-200">Canchas de Fútbol</p>
            <h1 className="text-3xl font-bold">Gestión de Canchas de Fútbol</h1>
            {error && <p className="text-sm text-red-300 mt-2">{error}</p>}
          </div>
          <div className="flex gap-3">
            <button
              onClick={() => navigate('/canchas')}
              className="min-w-[10rem] rounded-lg bg-white/10 px-4 py-2 text-sm font-semibold text-emerald-100 hover:bg-white/20"
            >
              Volver
            </button>
            <button
              onClick={() => fetchCanchas(filter)}
              className="min-w-[10rem] rounded-lg bg-white/10 px-4 py-2 text-sm font-semibold text-emerald-100 hover:bg-white/20 disabled:opacity-60"
              disabled={loading}
            >
              {loading ? 'Actualizando...' : 'Refrescar'}
            </button>
            <button
              onClick={() => navigate('/canchas/futbol/RegistrarCancha')}
              className="min-w-[10rem] rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400"
            >
              + Nueva Cancha
            </button>
          </div>
        </header>

        <section className="rounded-2xl border border-white/10 bg-white/5 p-4">
          <div className="mb-4">
            <input
              type="search"
              value={filter}
              onChange={handleSearchChange}
              placeholder="Buscar por nombre..."
              className="w-full rounded-lg bg-slate-900/80 px-4 py-2 text-sm text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>

          {loading ? (
            <p className="text-center text-emerald-100 py-8">Cargando canchas...</p>
          ) : canchasFiltradas.length === 0 ? (
            <p className="text-center text-emerald-100 py-8">
              {filter ? 'No se encontraron canchas con ese criterio.' : 'No hay canchas de fútbol registradas.'}
            </p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-white/10">
                    <th className="text-left py-3 px-2 font-semibold text-emerald-200">Nombre</th>
                    <th className="text-left py-3 px-2 font-semibold text-emerald-200">Descripción</th>
                    <th className="text-center py-3 px-2 font-semibold text-emerald-200">Estado</th>
                    <th className="text-center py-3 px-2 font-semibold text-emerald-200">Precio/Hora</th>
                    <th className="text-center py-3 px-2 font-semibold text-emerald-200">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {canchasFiltradas.map((item: any) => (
                    <tr
                      key={item.Id || item.id}
                      className="border-b border-white/5 hover:bg-white/5 transition-colors"
                    >
                      <td className="py-3 px-2 font-semibold">{item.nombre}</td>
                      <td className="py-3 px-2 text-gray-300">{item.descripcion || '-'}</td>
                      <td className="py-3 px-2 text-center">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                          item.activa 
                            ? 'bg-emerald-500/20 text-emerald-200' 
                            : 'bg-red-500/20 text-red-200'
                        }`}>
                          {item.activa ? 'Activa' : 'Inactiva'}
                        </span>
                      </td>
                      <td className="py-3 px-2 text-center font-semibold text-emerald-200">
                        ${item.precio_hora}
                      </td>
                      <td className="py-3 px-2">
                        <div className="flex items-center justify-center gap-2">
                          <button
                            onClick={() => navigate(`/canchas/futbol/ModificarCanchaFutbol/${item.Id || item.id}`)}
                            className="rounded-lg bg-emerald-500/20 px-3 py-1 text-xs font-semibold text-emerald-200 hover:bg-emerald-500/30"
                          >
                            Editar
                          </button>
                          <button
                            onClick={() => handleDelete(item.Id || item.id)}
                            disabled={deleteId === (item.Id || item.id)}
                            className="rounded-lg bg-red-500/20 px-3 py-1 text-xs font-semibold text-red-200 hover:bg-red-500/30 disabled:opacity-50"
                          >
                            {deleteId === (item.Id || item.id) ? 'Eliminando...' : 'Eliminar'}
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>

        <div className="rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-4">
          <p className="text-sm text-emerald-200">
            <span className="font-semibold">Total de canchas:</span> {canchasFiltradas.length}
            {filter && rows.length !== canchasFiltradas.length && (
              <span className="ml-2 text-emerald-100/70">
                (filtradas de {rows.length})
              </span>
            )}
          </p>
        </div>
      </div>
    </div>
  );
}