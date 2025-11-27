import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { turnosService } from '../../services/turnos';
import { canchasService } from '../../services/canchas';
import { useAuth } from '../../contexts/AuthContext';

interface Turno {
  id_turno: number;
  fecha: string;
  hora_inicio: string;
  estado: string;
  id_cancha: number;
  precio_final: number;
}

interface Cancha {
  id_cancha: number;
  nombre_cancha: string;
  tipo_deporte: string;
  techada: number;
  precio_hora: number;
}

interface Cliente {
  id_cliente: number;
  nombre: string;
  apellido: string;
  email: string;
}

const ClienteReservas: React.FC = () => {
  const { user } = useAuth();
  const esAdmin = user?.nombre_rol === 'Administrador';
  const location = useLocation();
  
  const [turnos, setTurnos] = useState<Turno[]>([]);
  const [canchas, setCanchas] = useState<Cancha[]>([]);
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [loading, setLoading] = useState(true);
  const [fechaSeleccionada, setFechaSeleccionada] = useState<string>(
    new Date().toISOString().split('T')[0]
  );
  const [canchaFiltro, setCanchaFiltro] = useState<number | null>(null);
  
  // Estados para registro admin
  const [modoAdmin, setModoAdmin] = useState(false);
  const [clienteSeleccionado, setClienteSeleccionado] = useState<number | null>(null);

  useEffect(() => {
    cargarDatos();
  }, []);

  useEffect(() => {
    cargarTurnos();
  }, [fechaSeleccionada, canchaFiltro]);

  // Habilitar modo admin desde query param ?admin=1
  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const adminParam = params.get('admin');
    if (esAdmin && adminParam === '1') {
      setModoAdmin(true);
    }
  }, [location.search, esAdmin]);

  const cargarDatos = async () => {
    try {
      const canchasData = await canchasService.obtenerTodas();
      setCanchas(canchasData);
      
      // Cargar clientes solo si es admin
      if (esAdmin) {
        const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000/api';
        const response = await fetch(`${API_BASE}/clientes/`);
        const clientesData = await response.json();
        setClientes(clientesData);
      }
    } catch (error) {
      console.error('Error cargando datos:', error);
    } finally {
      setLoading(false);
    }
  };

  const cargarTurnos = async () => {
    try {
      const turnosData = await turnosService.obtenerTodos();
      let filtrados = turnosData.filter((t: Turno) => t.fecha === fechaSeleccionada);
      if (canchaFiltro) {
        filtrados = filtrados.filter((t: Turno) => t.id_cancha === canchaFiltro);
      }
      setTurnos(filtrados);
    } catch (error) {
      console.error('Error cargando turnos:', error);
    }
  };

  const realizarReserva = async (turnoId: number) => {
    try {
      let clienteId: number;
      
      if (modoAdmin && clienteSeleccionado) {
        clienteId = clienteSeleccionado;
      } else {
        // En una implementación real, usarías el ID del cliente del contexto/auth
        clienteId = 1; // Ejemplo
      }
      
      await turnosService.reservar(turnoId, clienteId);
      alert('¡Reserva realizada con éxito!');
      cargarTurnos();
      
      if (modoAdmin) {
        setClienteSeleccionado(null);
      }
    } catch (error) {
      console.error('Error realizando reserva:', error);
      alert('Error al realizar la reserva');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl">Cargando disponibilidad...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            {modoAdmin ? 'Registrar Reserva' : 'Reservar Cancha'}
          </h1>
          
          {esAdmin && (
            <button
              onClick={() => {
                setModoAdmin(!modoAdmin);
                setClienteSeleccionado(null);
              }}
              className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
            >
              {modoAdmin ? 'Modo Cliente' : 'Modo Admin: Registrar para Cliente'}
            </button>
          )}
        </div>

        {/* Selector de Cliente (solo admin) */}
        {esAdmin && modoAdmin && (
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Seleccionar Cliente
            </label>
            <select
              value={clienteSeleccionado || ''}
              onChange={(e) => setClienteSeleccionado(e.target.value ? Number(e.target.value) : null)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            >
              <option value="">-- Seleccione un cliente --</option>
              {clientes.map(cliente => (
                <option key={cliente.id_cliente} value={cliente.id_cliente}>
                  {cliente.nombre} {cliente.apellido} - {cliente.email}
                </option>
              ))}
            </select>
          </div>
        )}

        {/* Filtros */}
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Fecha
              </label>
              <input
                type="date"
                value={fechaSeleccionada}
                onChange={(e) => setFechaSeleccionada(e.target.value)}
                min={new Date().toISOString().split('T')[0]}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Cancha
              </label>
              <select
                value={canchaFiltro || ''}
                onChange={(e) => setCanchaFiltro(e.target.value ? Number(e.target.value) : null)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              >
                <option value="">Todas las canchas</option>
                {canchas.map(cancha => (
                  <option key={cancha.id_cancha} value={cancha.id_cancha}>
                    {cancha.nombre_cancha} - {cancha.tipo_deporte}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Turnos Disponibles */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">
              Turnos Disponibles ({turnos.length})
            </h2>
          </div>
          <div className="p-6">
            {turnos.length === 0 ? (
              <div className="text-center py-12 text-gray-500">
                No hay turnos disponibles para esta fecha y cancha
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {turnos.map(turno => {
                  const cancha = canchas.find(c => c.id_cancha === turno.id_cancha);
                  return (
                    <div 
                      key={turno.id_turno}
                      className="border border-gray-200 rounded-lg p-4 hover:border-indigo-500 transition-colors"
                    >
                      <div className="flex justify-between items-start mb-3">
                        <div>
                          <h3 className="font-semibold text-gray-900">{cancha?.nombre_cancha}</h3>
                          <p className="text-sm text-gray-600">{cancha?.tipo_deporte}</p>
                        </div>
                        {cancha?.techada === 1 && (
                          <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
                            Techada
                          </span>
                        )}
                      </div>
                      <div className="space-y-2 mb-4">
                        <div className="flex items-center text-sm text-gray-600">
                          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          {turno.hora_inicio}
                        </div>
                        <div className="flex items-center text-sm font-semibold text-gray-900">
                          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          ${turno.precio_final.toFixed(2)}
                        </div>
                      </div>
                      <button
                        onClick={() => realizarReserva(turno.id_turno)}
                        disabled={modoAdmin && !clienteSeleccionado}
                        className={`w-full px-4 py-2 rounded-lg transition-colors font-medium ${
                          modoAdmin && !clienteSeleccionado
                            ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                            : 'bg-indigo-600 text-white hover:bg-indigo-700'
                        }`}
                      >
                        {modoAdmin ? 'Registrar Reserva' : 'Reservar'}
                      </button>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>

        {/* Información */}
        <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h3 className="font-semibold text-blue-900 mb-2">Información importante</h3>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• Los turnos son de 1 hora de duración</li>
            <li>• Horario de atención: 15:00 a 00:00</li>
            <li>• El servicio de iluminación está disponible desde las 19:00</li>
            <li>• Puede agregar servicios adicionales después de reservar</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ClienteReservas;
