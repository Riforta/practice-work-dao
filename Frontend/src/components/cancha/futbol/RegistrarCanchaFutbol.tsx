import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";
import service from "../../../services/canchas.service";
import backgroundImage from "./imagenes/robben.jpg";

type FormData = {
  nombre: string;
  tipo_deporte: string;
  descripcion: string; // Quité el optional '?' para que coincida con el form
  activa: boolean;     // Quité el optional '?'
};

export default function RegistroCanchaFutbol() {
  const [action, setAction] = useState("R");
  const [errorMessage, setErrorMessage] = useState("");
  
  const { register, handleSubmit, formState: { errors }, reset } = useForm<FormData>({
    defaultValues: { tipo_deporte: "futbol", activa: true }
  });
  
  const navigate = useNavigate();

  const onSubmit = async (data: FormData) => {
    // 0. Limpiamos errores previos
    setErrorMessage("");

    try {
      // --- PASO 1: VERIFICAR SI YA EXISTE ---
      // Llamamos al servicio para buscar por nombre
      const coincidencias = await service.getCanchaFutbolByName(data.nombre);
      
      // Verificamos si alguna de las coincidencias tiene el nombre EXACTO
      // (Porque la búsqueda puede traer parecidos)
      const existeDuplicado = coincidencias.some((c: any) => 
        c.nombre.trim().toLowerCase() === data.nombre.trim().toLowerCase()
      );

      if (existeDuplicado) {
        setErrorMessage("⚠️ Ya existe una cancha con ese nombre. Por favor elija otro.");
        return; // <--- AQUÍ SE DETIENE SI EXISTE
      }

      // --- PASO 2: CREAR LA CANCHA ---
      // Si llegamos acá, es porque no existe. Procedemos a crear.
      await service.creatCanchaFutbol(data);

      // --- PASO 3: REDIRECCIONAR ---
      // Si no hubo error en el await anterior, redirigimos.
      setAction("C"); // Opcional, ya que nos vamos de la página
      navigate("/canchas/futbol");

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
          <h5 className="text-center text-xl font-semibold mb-4">Registro de Cancha</h5>

          {errorMessage && (
            <div className="bg-red-500/20 border border-red-500 text-red-100 p-3 rounded mb-4 text-sm text-center">
              {errorMessage}
            </div>
          )}

          <label className="block text-sm font-medium mb-1">Nombre</label>
          <input
            {...register("nombre", { required: "El nombre es requerido" })}
            className="w-full mb-3 px-3 py-2 border border-white/30 bg-white/5 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400 text-white placeholder-gray-400"
            placeholder="Nombre de la cancha"
          />
          {errors.nombre && <p className="text-red-400 text-sm mb-2">{errors.nombre.message}</p>}

          <label className="block text-sm font-medium mb-1">Deporte</label>
          <select
            {...register("tipo_deporte", { required: "Seleccione un deporte" })}
            className="w-full mb-3 px-3 py-2 border border-white/30 bg-white/5 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400 text-white"
          >
            <option value="Futbol" className="bg-gray-700">Futbol</option>
          </select>
          {errors.tipo_deporte && <p className="text-red-400 text-sm mb-2">{errors.tipo_deporte.message}</p>}

          <label className="block text-sm font-medium mb-1">Descripción</label>
          <textarea
            {...register("descripcion")}
            className="w-full mb-3 px-3 py-2 border border-white/30 bg-white/5 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400 text-white placeholder-gray-400"
            rows={3}
            placeholder="Descripción breve"
          />

          <label className="flex items-center gap-2 mb-4">
            <input
              type="checkbox"
              {...register("activa")}
              defaultChecked
              className="w-4 h-4 rounded text-blue-500 bg-white/5 border-white/30"
            />
            <span className="text-sm">Activa</span>
          </label>

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
              to="/canchas/futbol"
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