import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";
import service from "../../services/equipos.service";
import backgroundImage from "./imagenes/curry_hd_si.jpg";

type FormData = {
  nombre_equipo: string;
  id_capitan?: number;
};

export default function RegistroEquipo() {
  const [action, setAction] = useState("R");
  const [errorMessage, setErrorMessage] = useState("");
  
  const { register, handleSubmit, formState: { errors }, reset } = useForm<FormData>();
  
  const navigate = useNavigate();

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
      await service.creatEquipo(data);

      // --- PASO 3: REDIRECCIONAR ---
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