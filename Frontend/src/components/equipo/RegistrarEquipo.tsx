import React, { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";
import service from "../../services/equipos.service";
import clientesService, { type Cliente } from "../../services/clientes.service";
import equipoMiembroService from "../../services/equipoMiembro.service";
import backgroundImage from "./imagenes/curry_hd_si.jpg";

type FormData = {
  nombre_equipo: string;
  id_capitan?: number;
};

export default function RegistroEquipo() {
  const [action, setAction] = useState("R");
  const [errorMessage, setErrorMessage] = useState("");
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [clientesLoading, setClientesLoading] = useState(true);
  const [clienteSearch, setClienteSearch] = useState('');
  const [selectedClientes, setSelectedClientes] = useState<number[]>([]);
  
  const { register, handleSubmit, formState: { errors }, reset } = useForm<FormData>();
  
  const navigate = useNavigate();

  useEffect(() => {
    const loadClientes = async () => {
      setClientesLoading(true);
      try {
        const data = await clientesService.list();
        setClientes(data);
      } catch (err) {
        console.error(err);
        setErrorMessage('No se pudieron cargar los clientes.');
      } finally {
        setClientesLoading(false);
      }
    };
    void loadClientes();
  }, []);

  const clientesFiltrados = React.useMemo(() => {
    const term = clienteSearch.trim().toLowerCase();
    return clientes.filter((cliente) => {
      const nombreCompleto = `${cliente.nombre} ${cliente.apellido || ''}`.toLowerCase();
      return term ? nombreCompleto.includes(term) : true;
    });
  }, [clientes, clienteSearch]);

  const clientesMap = React.useMemo(() => {
    const map = new Map<number, Cliente>();
    clientes.forEach((cliente) => map.set(cliente.id, cliente));
    return map;
  }, [clientes]);

  const toggleCliente = (clienteId: number) => {
    setSelectedClientes((prev) =>
      prev.includes(clienteId) ? prev.filter((id) => id !== clienteId) : [...prev, clienteId]
    );
  };

  const onSubmit = async (data: FormData) => {
    // 0. Limpiamos errores previos
    setErrorMessage("");

    try {
      // --- PASO 1: VERIFICAR SI YA EXISTE ---
      // Llamamos al servicio para buscar por nombre
      const coincidencias = await service.getEquipoByName(data.nombre_equipo);
      
      // Verificamos si alguna de las coincidencias tiene el nombre EXACTO
      // (Porque la búsqueda puede traer parecidos)
      const existeDuplicado = coincidencias.some((c: any) => 
        c.nombre_equipo.trim().toLowerCase() === data.nombre_equipo.trim().toLowerCase()
      );

      if (existeDuplicado) {
        setErrorMessage("⚠️ Ya existe una equipo con ese nombre. Por favor elija otro.");
        return; // <--- AQUÍ SE DETIENE SI EXISTE
      }

      // --- PASO 2: CREAR EL EQUIPO ---
      // Si llegamos acá, es porque no existe. Procedemos a crear.
      const equipoCreado = await service.creatEquipo(data);
      
      // --- PASO 3: AGREGAR MIEMBROS ---
      if (equipoCreado.id && selectedClientes.length > 0) {
        await equipoMiembroService.agregarMiembrosMasivo(equipoCreado.id, selectedClientes);
      }

      // --- PASO 4: REDIRECCIONAR ---
      // Si no hubo error en el await anterior, redirigimos.
      setAction("C"); // Opcional, ya que nos vamos de la página
      navigate("/equipos/ConsultarEquipo");

    } catch (error) {
      console.error(error);
      setErrorMessage("Error al conectar con el servidor. Intente nuevamente.");
    }
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center"
      style={{
        backgroundImage: `url(${backgroundImage})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
      }}
    >
      {action === "R" && (
        <form
          onSubmit={handleSubmit(onSubmit)}
          className="w-full max-w-md bg-white/10 backdrop-blur-md text-white rounded-lg p-6 shadow-lg"
        >
          <h5 className="text-center text-xl font-semibold mb-4">Registro de Equipo</h5>

          {errorMessage && (
            <div className="bg-red-500/20 border border-red-500 text-red-100 p-3 rounded mb-4 text-sm text-center">
              {errorMessage}
            </div>
          )}

          <label className="block text-sm font-medium mb-1">Nombre</label>
          <input
            {...register("nombre_equipo", { required: "El nombre es requerido" })}
            className="w-full mb-3 px-3 py-2 border border-white/30 bg-white/5 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400 text-white placeholder-gray-400"
            placeholder="Nombre del equipo "
          />
          {errors.nombre_equipo && <p className="text-red-400 text-sm mb-2">{errors.nombre_equipo.message}</p>}

          <section className="mb-4 rounded-xl border border-white/20 bg-white/5 p-4">
            <div className="mb-3">
              <h3 className="text-sm font-semibold mb-2">Miembros del equipo</h3>
              <p className="text-xs text-gray-300 mb-2">
                Selecciona los clientes que formarán parte del equipo ({selectedClientes.length} seleccionados)
              </p>
              <input
                type="search"
                value={clienteSearch}
                onChange={(e) => setClienteSearch(e.target.value)}
                placeholder="Buscar cliente..."
                className="w-full px-3 py-2 rounded-lg bg-white/10 text-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-400"
              />
            </div>
            <div className="max-h-48 overflow-y-auto rounded-lg border border-white/10 bg-black/20">
              {clientesLoading ? (
                <p className="p-3 text-sm text-gray-300">Cargando clientes...</p>
              ) : clientesFiltrados.length === 0 ? (
                <p className="p-3 text-sm text-gray-300">No hay clientes disponibles.</p>
              ) : (
                <ul className="divide-y divide-white/5">
                  {clientesFiltrados.map((cliente) => (
                    <li key={cliente.id}>
                      <label className="flex items-center gap-3 p-3 hover:bg-white/5 cursor-pointer">
                        <input
                          type="checkbox"
                          className="size-4"
                          checked={selectedClientes.includes(cliente.id)}
                          onChange={() => toggleCliente(cliente.id)}
                        />
                        <div>
                          <p className="font-semibold text-sm">
                            {cliente.nombre} {cliente.apellido}
                          </p>
                          <p className="text-xs text-gray-400">DNI: {cliente.dni || 'N/A'}</p>
                        </div>
                      </label>
                    </li>
                  ))}
                </ul>
              )}
            </div>
            {selectedClientes.length > 0 && (
              <div className="mt-3 flex flex-wrap gap-2 text-xs">
                {selectedClientes.map((clienteId) => {
                  const cliente = clientesMap.get(clienteId);
                  return (
                    <span key={clienteId} className="rounded-full border border-white/30 px-3 py-1 text-gray-200">
                      {cliente ? `${cliente.nombre} ${cliente.apellido || ''}` : `Cliente ${clienteId}`}
                    </span>
                  );
                })}
              </div>
            )}
          </section>


          <div className="flex justify-center gap-3">
            <button
              type="submit"
              className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-md transition-colors"
            >
              Registrar
            </button>
            <button
              type="button"
              onClick={() => { reset(); setErrorMessage(""); }}
              className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-md transition-colors"
            >
              Limpiar
            </button>
            <Link
              to="/equipos/ConsultarEquipo"
              className="px-4 py-2 bg-white/20 hover:bg-white/30 text-white rounded-md shadow transition-colors"
            >
              Volver
            </Link>
          </div>
        </form>
      )}
    </div>
  );
}