import React, { useState, useEffect } from 'react';
import service from '../../services/equipos.service'; 
import equipoMiembroService from '../../services/equipoMiembro.service';
import { useNavigate } from 'react-router-dom';

export default function ConsultarEquipo() {
  const [rows, setRows] = useState<any[]>([]);
  const [filter, setFilter] = useState('');
  const [loading, setLoading] = useState(false); // Estado para mostrar "Cargando..."
  const [miembrosCount, setMiembrosCount] = useState<Record<number, number>>({});
  const navigate = useNavigate();

  // Función unificada para cargar datos
  const fetchEquipos = async (searchTerm = '') => {
    setLoading(true);
    try {
      let data;
      if (searchTerm) {
        // Si hay texto, buscamos por nombre
        data = await service.getEquipoByName(searchTerm);
      } else {
        // Si está vacío, traemos todas
        data = await service.getAllEquipos();
      }
      setRows(data);
      
      // Cargar cantidad de miembros para cada equipo
      const counts: Record<number, number> = {};
      await Promise.all(
        data.map(async (equipo: any) => {
          const equipoId = equipo.id || equipo.Id;
          if (equipoId) {
            try {
              const miembros = await equipoMiembroService.listarMiembrosPorEquipo(equipoId);
              counts[equipoId] = miembros.length;
            } catch {
              counts[equipoId] = 0;
            }
          }
        })
      );
      setMiembrosCount(counts);
    } catch (error) {
      console.error('Error cargando Equipos:', error);
    } finally {
      setLoading(false);
    }
  };

  // useEffect con DEBOUNCE (El truco para no saturar)
  useEffect(() => {
    // 1. Configuramos el temporizador (500ms)
    const timerId = setTimeout(() => {
      fetchEquipos
      (filter);
    }, 500);

    // 2. Limpieza: Si el usuario escribe antes de 500ms, cancelamos el timer anterior
    return () => {
      clearTimeout(timerId);
    };
  }, [filter]); // Se ejecuta cuando cambia el filtro

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setFilter(event.target.value);
  };

  const handleDeleteUser = async (id: number) => {
    if(!window.confirm("¿Seguro que quieres eliminar esta equipo?")) return;
    
    try {
      await service.deleteEquipo(id);
      // Recargamos la lista actual manteniendo el filtro
      await fetchEquipos
      (filter); 
    } catch (error) {
      console.error('Error al eliminar:', error);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white px-4 py-10">
      <div className="max-w-6xl mx-auto space-y-6">
        <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <p className="text-sm uppercase tracking-widest text-emerald-200">Equipos</p>
            <h1 className="text-3xl font-bold">Gestión de equipos</h1>
          </div>
          <div className="flex gap-3">
            <button
              onClick={() => navigate('/')}
              className="rounded-lg bg-white/10 px-4 py-2 text-sm font-semibold text-emerald-100 hover:bg-white/20 min-w-[10rem]"
            >
              Volver
            </button>
            <button
              onClick={() => fetchEquipos(filter)}
              className="rounded-lg bg-white/10 px-4 py-2 text-sm font-semibold text-emerald-100 hover:bg-white/20 disabled:opacity-60 min-w-[10rem]"
              disabled={loading}
            >
              {loading ? 'Actualizando...' : 'Refrescar'}
            </button>
            <button
              onClick={() => navigate('/equipos/RegistrarEquipo')}
              className="rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400 min-w-[10rem]"
            >
              Registrar equipo
            </button>
          </div>
        </header>

        <section className="bg-white/10 backdrop-blur-md rounded-2xl p-4 shadow-lg border border-white/10">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-4">
            <label className="text-sm text-emerald-100">
              Buscar por nombre
              <input 
                type="search"
                className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
                placeholder="Buscar..."
                value={filter}
                onChange={handleSearchChange}
              />
            </label>
          </div>

          <div className="max-h-[65vh] overflow-y-auto rounded-2xl border border-white/5">
            <table className="min-w-full text-left text-sm">
              <thead className="sticky top-0 bg-slate-900/80 text-xs uppercase tracking-wide text-emerald-200">
                <tr>
                  <th className="px-4 py-3">Nombre</th>
                  <th className="px-4 py-3">Miembros</th>
                  <th className="px-4 py-3">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr>
                    <td colSpan={3} className="px-4 py-6 text-center text-emerald-100">
                      Cargando equipos...
                    </td>
                  </tr>
                ) : rows.length === 0 ? (
                  <tr>
                    <td colSpan={3} className="px-4 py-6 text-center text-emerald-100">
                      No se encontraron equipos.
                    </td>
                  </tr>
                ) : (
                  rows.map((item: any) => {
                    const equipoId = item.Id || item.id;
                    return (
                      <tr key={equipoId} className="border-t border-white/5 hover:bg-white/5">
                        <td className="px-4 py-3 text-sm font-semibold">{item.nombre_equipo}</td>
                        <td className="px-4 py-3 text-sm text-emerald-100">
                          {miembrosCount[equipoId] ?? 0}
                        </td>
                        <td className="px-4 py-3">
                          <div className="flex flex-wrap gap-2 text-xs">
                            <button
                              onClick={() => navigate(`/equipos/ModificarEquipo/${equipoId}`)}
                              className="rounded-lg bg-white/10 px-3 py-1 text-xs font-semibold text-emerald-100 hover:bg-white/20"
                            >
                              Editar
                            </button>
                            <button
                              onClick={() => handleDeleteUser(equipoId)}
                              className="rounded-lg bg-red-500/80 px-3 py-1 text-xs font-semibold text-white hover:bg-red-500"
                            >
                              Eliminar
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>
  );
}