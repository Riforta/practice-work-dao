import React, { useState, useEffect } from 'react';
// Asegúrate de que la ruta sea correcta
import service from '../../services/equipos.service'; 
import { Link, useNavigate } from 'react-router-dom';
import backgroundImage from "./imagenes/cancha_bas.jpg";

export default function ConsultarEquipo() {
  const [rows, setRows] = useState<any[]>([]);
  const [filter, setFilter] = useState('');
  const [loading, setLoading] = useState(false); // Estado para mostrar "Cargando..."
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
    <div
      className="min-h-screen bg-no-repeat bg-cover bg-center"
      style={{
        backgroundImage: `url(${backgroundImage})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
        backgroundAttachment: "scroll" // evita parallax/repintados raros
      }}>
      {/* Wrapper centrado horizontalmente y con espacio superior */}
      <div className="w-full max-w-6xl mx-auto px-6 py-12">
        <div className="flex justify-between items-center mb-6">
          <h2 className="bg-white text-red-900 px-6 py-3 rounded hover:bg-gray-100 shadow text-4xl md:text-5xl font-extrabold" >Gestión de Equipos

          </h2>
          <Link to="/equipos/RegistrarEquipo" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
            + Nueva equipo
          </Link>
        </div>

        {/* Barra de búsqueda */}
        <div className="mb-6">
          <input 
            type="text"
            className="bg-white w-full max-w-md p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
            placeholder="🔍 Buscar por nombre..."
            value={filter}
            onChange={handleSearchChange}
          />
        </div>

        {/* Tabla */}
        <div className="overflow-auto bg-white rounded-lg shadow max-h-[60vh]">
            <table className="w-full text-sm text-left text-gray-500">
                <thead className="text-xs text-gray-700 uppercase bg-gray-100 text-center">
                    <tr>
                        <th className="px-6 py-3">Nombre</th>
                        <th className="px-6 py-3">Acciones</th>
                    </tr>
                </thead>
                <tbody className="text-center">
                    {loading ? (
                        <tr><td colSpan={5} className="py-4">Cargando...</td></tr>
                    ) : rows.length === 0 ? (
                        <tr><td colSpan={5} className="py-4">No se encontraron Equipos
                        </td></tr>
                    ) : (
                        rows.map((item: any) => (
                            <tr key={item.Id || item.id} className="border-b hover:bg-gray-50">
                                <td className="px-6 py-4 font-medium text-gray-900">{item.nombre_equipo}</td>
                                <td className="px-6 py-4 space-x-2">
                                    <button
                                        onClick={() => navigate(`/equipos/ModificarEquipo/${item.Id || item.id}`)}
                                        className="text-white bg-blue-600 hover:bg-blue-700 px-3 py-1 rounded text-xs">
                                        Editar
                                    </button>
                                    <button
                                        onClick={() => handleDeleteUser(item.Id || item.id)}
                                        className="text-white bg-red-600 hover:bg-red-700 px-3 py-1 rounded text-xs">
                                        Eliminar
                                    </button>
                                </td>
                            </tr>
                        ))
                    )}
                </tbody>
            </table>
        </div>
        
        <div className="mt-6 text-center">
          <Link to='/' className='bg-white text-gray-800 px-4 py-2 rounded hover:bg-gray-100 shadow'>Volver al menú</Link>
        </div>
    </div>
    </div>
  );
}