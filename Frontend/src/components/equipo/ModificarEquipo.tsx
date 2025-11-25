import React, { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate, useParams } from "react-router-dom";
import service from "../../services/equipos.service";
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

  const id = params.id || params.Id || params.Id_Equipo;

  // Carga inicial de datos
  useEffect(() => {
    if (!id) return;
    const fetchEquipo = async () => {
      try {
        const data: any = await service.getById(Number(id));
        if (!data) return;        
        setValue("nombre_equipo", data.nombre_equipo ?? data.nombre_equipo ?? "");

      } catch (err) {
        console.error(err);
        setErrorMessage("No se pudo cargar el Equipo.");
      }
    };
    fetchEquipo();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

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
      
      // --- PASO 3: REDIRECCIÓN ---
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