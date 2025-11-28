import React, { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate, useParams } from "react-router-dom";
import service from "../../services/equipos.service";
import clientesService, { type Cliente } from "../../services/clientes.service";
import equipoMiembroService, { type EquipoMiembro } from "../../services/equipoMiembro.service";
import backgroundImage from "./imagenes/curry_hd_si.jpg";

type FormData = {
  nombre_equipo: string;
  id_capitan?: number;
};

export default function ModificarEquipo() {
  const { register, handleSubmit, formState: { errors }, setValue, reset } = useForm<FormData>();
  const params = useParams();
  const navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState("");
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [clientesLoading, setClientesLoading] = useState(true);
  const [clienteSearch, setClienteSearch] = useState('');
  const [selectedClientes, setSelectedClientes] = useState<number[]>([]);
  const [originalClientes, setOriginalClientes] = useState<number[]>([]);

  const id = params.id || params.Id || params.Id_Equipo;

  // Carga inicial de datos
  useEffect(() => {
    if (!id) return;
    const fetchData = async () => {
      setClientesLoading(true);
      try {
        const [equipoData, clientesData, miembrosData] = await Promise.all([
          service.getById(Number(id)),
          clientesService.list(),
          equipoMiembroService.listarMiembrosPorEquipo(Number(id)),
        ]);
        
        if (equipoData) {
          setValue("nombre_equipo", equipoData.nombre_equipo ?? equipoData.nombre_equipo ?? "");
        }
        
        setClientes(clientesData);
        
        const miembrosIds = miembrosData.map((m: EquipoMiembro) => m.id_cliente);
        setSelectedClientes(miembrosIds);
        setOriginalClientes(miembrosIds);
      } catch (err) {
        console.error(err);
        setErrorMessage("No se pudo cargar el Equipo.");
      } finally {
        setClientesLoading(false);
      }
    };
    fetchData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

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

  const onSubmit = async (form: FormData) => {
    // Limpiamos errores previos
    setErrorMessage("");

    try {
      // --- PASO 1: VERIFICACIÓN DE nombre_equipo DUPLICADO ---
      
      // Buscamos si ya existe alguien con ese nombre_equipo
      // (Asumiendo que tienes este método en tu servicio, lo vimos antes)
      const EquiposConEsenombre_equipo = await service.getEquipoByName(form.nombre_equipo);
      
      // Revisamos si encontramos alguna Equipo QUE NO SEA la actual
      // (Comparamos IDs: si el ID es distinto pero el nombre_equipo es igual, es un duplicado)
      const existeDuplicado = EquiposConEsenombre_equipo.some((c: any) => 
        // Asegúrate de comparar usando el nombre_equipo exacto y excluyendo el ID actual
        c.nombre_equipo.toLowerCase() === form.nombre_equipo.toLowerCase() && 
        (c.id || c.Id) !== Number(id)
      );

      if (existeDuplicado) {
        setErrorMessage("⚠️ Ya existe otra Equipo con ese nombre. Por favor elija uno distinto.");
        return; // <--- AQUÍ DETENEMOS LA EJECUCIÓN
      }

      // --- PASO 2: ACTUALIZACIÓN ---

      const payload = {
        nombre_equipo: form.nombre_equipo,
      };
      
      await service.actualizarEquipo(Number(id), payload);
      
      // --- PASO 3: ACTUALIZAR MIEMBROS ---
      const clientesAAgregar = selectedClientes.filter((cId) => !originalClientes.includes(cId));
      const clientesAQuitar = originalClientes.filter((cId) => !selectedClientes.includes(cId));

      if (clientesAQuitar.length) {
        const miembrosAEliminar: Array<[number, number]> = clientesAQuitar.map(clienteId => [Number(id), clienteId]);
        await equipoMiembroService.eliminarMiembrosMasivo(miembrosAEliminar);
      }
      if (clientesAAgregar.length) {
        await equipoMiembroService.agregarMiembrosMasivo(Number(id), clientesAAgregar);
      }
      
      // --- PASO 4: REDIRECCIÓN ---
      // Si llegamos acá es que no hubo error en el await anterior
      navigate("/equipos/ConsultarEquipo"); 
      
    } catch (err) {
      console.error(err);
      setErrorMessage("Error al actualizar el Equipo. Verifique los datos o la conexión.");
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
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="bg-white/10 backdrop-blur-md text-white rounded-lg p-6 w-full max-w-lg shadow-lg"
      >
        <h3 className="text-2xl mb-4">Modificar Equipo</h3>
        
        {/* Mensaje de error destacado */}
        {errorMessage && (
            <div className="bg-red-500/20 border border-red-500 text-red-100 p-3 rounded mb-4 text-sm text-center">
                {errorMessage}
            </div>
        )}

        <label className="block mb-2 text-sm">Nombre Equipo</label>
        <input
          {...register("nombre_equipo", { required: "El nombre_equipo es requerido" })}
          className="w-full mb-3 px-3 py-2 rounded bg-white/5 focus:outline-none focus:ring-2 focus:ring-white/30"
        />
        {errors.nombre_equipo && <p className="text-red-400 text-sm mb-2">{errors.nombre_equipo.message}</p>}
        
        <section className="mb-4 rounded-xl border border-white/20 bg-white/5 p-4">
          <div className="mb-3">
            <h3 className="text-sm font-semibold mb-2">Miembros del equipo</h3>
            <p className="text-xs text-gray-300 mb-2">
              Selecciona los clientes que forman parte del equipo ({selectedClientes.length} seleccionados)
            </p>
            <input
              type="search"
              value={clienteSearch}
              onChange={(e) => setClienteSearch(e.target.value)}
              placeholder="Buscar cliente..."
              className="w-full px-3 py-2 rounded-lg bg-white/10 text-sm text-white focus:outline-none focus:ring-2 focus:ring-white/30"
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


        <div className="flex justify-center gap-3 mt-4">
          <button
            type="submit"
            className="px-4 py-2 bg-green-600 hover:bg-green-700 rounded text-white"
          >
            Actualizar
          </button>
          
          <button
            type="button"
            onClick={() => { reset(); setErrorMessage(""); }}
            className="px-4 py-2 bg-gray-600 hover:bg-gray-700 rounded text-white"
          >
            Limpiar
          </button>
          
          <Link to="/Equipos/" className="px-4 py-2 bg-black/60 hover:bg-black/80 rounded text-white flex items-center">
            Volver
          </Link>
        </div>
      </form>
    </div>
  );
}