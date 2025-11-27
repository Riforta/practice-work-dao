import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

interface Cliente {
  id?: number;
  nombre: string;
  apellido: string;
  dni: string;
  telefono: string;
  email: string;
}

const GestionClientes: React.FC = () => {
  const navigate = useNavigate();
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [filteredClientes, setFilteredClientes] = useState<Cliente[]>([]);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Filtros
  const [filterNombre, setFilterNombre] = useState('');
  const [filterApellido, setFilterApellido] = useState('');
  const [filterDni, setFilterDni] = useState('');

  const cargarClientes = async () => {
    try {
      setLoading(true);
      setErrorMsg(null);
      const resp = await fetch(`${API_BASE_URL}/api/clientes/`);
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const data: Cliente[] = await resp.json();
      setClientes(data);
      setFilteredClientes(data);
    } catch (err: any) {
      setErrorMsg('Error al cargar los clientes');
    } finally {
      setLoading(false);
    }
  };

  const eliminarCliente = async (id: number) => {
    try {
      const resp = await fetch(`${API_BASE_URL}/api/clientes/${id}`, { method: 'DELETE' });
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      await cargarClientes();
    } catch {
      setErrorMsg('No se pudo eliminar el cliente');
    }
  };

  const limpiarFiltros = () => {
    setFilterNombre('');
    setFilterApellido('');
    setFilterDni('');
    setFilteredClientes(clientes);
  };

  useEffect(() => {
    cargarClientes();
  }, []);

  useEffect(() => {
    let filtrados = [...clientes];
    if (filterNombre) {
      filtrados = filtrados.filter(c => c.nombre.toLowerCase().includes(filterNombre.toLowerCase()));
    }
    if (filterApellido) {
      filtrados = filtrados.filter(c => c.apellido.toLowerCase().includes(filterApellido.toLowerCase()));
    }
    if (filterDni) {
      filtrados = filtrados.filter(c => c.dni.toLowerCase().includes(filterDni.toLowerCase()));
    }
    setFilteredClientes(filtrados);
  }, [clientes, filterNombre, filterApellido, filterDni]);

  return (
    <div className="min-h-screen bg-slate-950 text-white px-4 py-10">
      <div className="max-w-6xl mx-auto space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <p className="text-sm uppercase tracking-widest text-emerald-200">Clientes</p>
            <h1 className="text-3xl font-bold">Gestión de clientes</h1>
            {errorMsg && <p className="text-red-300 text-sm mt-2">{errorMsg}</p>}
          </div>
          <div className="flex flex-nowrap gap-3">
            <button onClick={() => cargarClientes()} className="rounded-lg bg-white/10 px-4 py-2 text-sm font-semibold text-emerald-100 hover:bg-white/20">
              Refrescar
            </button>
            <Link to="/clientes/nuevo" className="rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400 whitespace-nowrap">
              + Registrar cliente
            </Link>
          </div>
        </div>

        <section className="bg-white/10 backdrop-blur-md rounded-2xl p-4 shadow-lg border border-white/10">
          <div className="flex flex-col gap-3">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              <label className="text-sm text-emerald-100">
                Filtrar por nombre
                <input type="text" value={filterNombre} onChange={(e) => setFilterNombre(e.target.value)}
                       className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400" placeholder="Todos" />
              </label>
              <label className="text-sm text-emerald-100">
                Filtrar por apellido
                <input type="text" value={filterApellido} onChange={(e) => setFilterApellido(e.target.value)}
                       className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400" placeholder="Todos" />
              </label>
              <label className="text-sm text-emerald-100">
                Filtrar por DNI
                <input type="text" value={filterDni} onChange={(e) => setFilterDni(e.target.value)}
                       className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400" placeholder="Todos" />
              </label>
            </div>
            {(filterNombre || filterApellido || filterDni) && (
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
                  <th className="px-4 py-3 text-left">Apellido</th>
                  <th className="px-4 py-3 text-left">DNI</th>
                  <th className="px-4 py-3 text-left">Teléfono</th>
                  <th className="px-4 py-3 text-left">Email</th>
                  <th className="px-4 py-3 text-right">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {filteredClientes.length === 0 ? (
                  <tr>
                    <td className="px-4 py-6 text-center text-emerald-100" colSpan={7}>No hay clientes para mostrar.</td>
                  </tr>
                ) : (
                  filteredClientes.map(cliente => (
                    <tr key={cliente.id} className="border-t border-white/5 hover:bg-white/5">
                      <td className="px-4 py-3 text-emerald-100">{cliente.id}</td>
                      <td className="px-4 py-3 text-emerald-100">{cliente.nombre}</td>
                      <td className="px-4 py-3 text-emerald-100">{cliente.apellido}</td>
                      <td className="px-4 py-3 text-emerald-100">{cliente.dni}</td>
                      <td className="px-4 py-3 text-emerald-100">{cliente.telefono}</td>
                      <td className="px-4 py-3 text-emerald-100">{cliente.email}</td>
                      <td className="px-4 py-3 text-right space-x-2">
                        <button className="rounded-lg bg-white/10 px-3 py-1 text-xs font-semibold text-emerald-100 hover:bg-white/20" onClick={() => navigate(`/clientes/${cliente.id}/editar`)}>Editar</button>
                        <button className="rounded-lg bg-red-500/80 px-3 py-1 text-xs font-semibold text-white hover:bg-red-500" onClick={() => eliminarCliente(cliente.id!)}>Eliminar</button>
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

export default GestionClientes;
