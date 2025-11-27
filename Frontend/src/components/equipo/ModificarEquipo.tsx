import React, { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate, useParams } from "react-router-dom";
import service from "../../services/equipos.service";

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
    <div className="min-h-screen bg-slate-950 text-white px-4 py-10">
      <div className="max-w-6xl mx-auto space-y-6">
        <form
          onSubmit={handleSubmit(onSubmit)}
          className="w-full max-w-lg mx-auto space-y-4 rounded-2xl bg-white/10 p-6 shadow-2xl backdrop-blur-md border border-white/10"
        >
          <div className="space-y-1">
            <p className="text-sm uppercase tracking-widest text-emerald-200">Equipos</p>
            <h2 className="text-2xl font-bold">Modificar equipo</h2>
            {errorMessage && <p className="text-red-300 text-sm">{errorMessage}</p>}
          </div>

          <label className="block text-sm">
            Nombre Equipo
            <input
              {...register("nombre_equipo", { required: "El nombre es requerido" })}
              className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white placeholder:text-emerald-200/60 focus:outline-none focus:ring-2 focus:ring-emerald-400"
              placeholder="Nombre del equipo"
            />
            {errors.nombre_equipo && <span className="text-xs text-red-300">{errors.nombre_equipo.message}</span>}
          </label>

          <div className="flex flex-wrap gap-3 pt-2">
            <button
              type="submit"
              className="rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400"
            >
              Actualizar
            </button>
            <button
              type="button"
              onClick={() => { reset(); setErrorMessage(""); }}
              className="rounded-lg border border-white/20 bg-white/5 px-4 py-2 text-sm text-emerald-100 hover:border-emerald-400"
            >
              Restaurar
            </button>
            <Link 
              to="/equipos/ConsultarEquipo" 
              className="rounded-lg border border-white/20 bg-white/0 px-4 py-2 text-sm text-emerald-100 hover:border-emerald-400"
            >
              Volver
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}