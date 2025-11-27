import React, { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate, useParams } from "react-router-dom";
import service from "../../../services/canchas.service";

type FormData = {
  nombre: string;
  tipo_deporte: string;
  descripcion: string;
  activa: boolean;
};

export default function ModificarCanchaPadel() {
  const { register, handleSubmit, formState: { errors }, setValue, reset } = useForm<FormData>();
  const params = useParams();
  const navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState("");

  const id = params.id || params.Id || params.Id_Cancha;

  // Carga inicial de datos
  useEffect(() => {
    if (!id) return;
    const fetchCancha = async () => {
      try {
        const data: any = await service.getByIdPadel(Number(id));
        if (!data) return;
        
        setValue("nombre", data.nombre ?? data.Nombre ?? "");
        setValue("tipo_deporte", (data.tipo_deporte ?? data.deporte ?? "").toString().toLowerCase());
        setValue("descripcion", data.descripcion ?? "");
        setValue("activa", Boolean(data.activa));
      } catch (err) {
        console.error(err);
        setErrorMessage("No se pudo cargar la cancha.");
      }
    };
    fetchCancha();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const onSubmit = async (form: FormData) => {
    // Limpiamos errores previos
    setErrorMessage("");

    try {
      // --- PASO 1: VERIFICACIÓN DE NOMBRE DUPLICADO ---
      
      // Buscamos si ya existe alguien con ese nombre
      // (Asumiendo que tienes este método en tu servicio, lo vimos antes)
      const canchasConEseNombre = await service.getCanchaPadelByName(form.nombre);
      
      // Revisamos si encontramos alguna cancha QUE NO SEA la actual
      // (Comparamos IDs: si el ID es distinto pero el nombre es igual, es un duplicado)
      const existeDuplicado = canchasConEseNombre.some((c: any) => 
        // Asegúrate de comparar usando el nombre exacto y excluyendo el ID actual
        c.nombre.toLowerCase() === form.nombre.toLowerCase() && 
        (c.id || c.Id) !== Number(id)
      );

      if (existeDuplicado) {
        setErrorMessage("⚠️ Ya existe otra cancha con ese nombre. Por favor elija uno distinto.");
        return; // <--- AQUÍ DETENEMOS LA EJECUCIÓN
      }

      // --- PASO 2: ACTUALIZACIÓN ---

      const payload = {
        nombre: form.nombre,
        tipo_deporte: form.tipo_deporte,
        descripcion: form.descripcion,
        activa: form.activa,
      };
      
      await service.actualizarCancha(Number(id), payload);
      
      // --- PASO 3: REDIRECCIÓN ---
      // Si llegamos acá es que no hubo error en el await anterior
      navigate("/canchas/padel"); 
      
    } catch (err) {
      console.error(err);
      setErrorMessage("Error al actualizar la cancha. Verifique los datos o la conexión.");
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
            <p className="text-sm uppercase tracking-widest text-emerald-200">Canchas - Padel</p>
            <h2 className="text-2xl font-bold">Modificar cancha</h2>
            {errorMessage && <p className="text-red-300 text-sm">{errorMessage}</p>}
          </div>

          <label className="block text-sm">
            Nombre
            <input
              {...register("nombre", { required: "El nombre es requerido" })}
              className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white placeholder:text-emerald-200/60 focus:outline-none focus:ring-2 focus:ring-emerald-400"
              placeholder="Nombre de la cancha"
            />
            {errors.nombre && <span className="text-xs text-red-300">{errors.nombre.message}</span>}
          </label>

          <label className="block text-sm">
            Deporte
            <select
              {...register("tipo_deporte", { required: "Seleccione un deporte" })}
              className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
            >
              <option value="Padel" className="bg-slate-900">Padel</option>
            </select>
            {errors.tipo_deporte && <span className="text-xs text-red-300">{errors.tipo_deporte.message}</span>}
          </label>

          <label className="block text-sm">
            Descripción
            <textarea
              {...register("descripcion")}
              className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white placeholder:text-emerald-200/60 focus:outline-none focus:ring-2 focus:ring-emerald-400"
              rows={3}
              placeholder="Descripción opcional"
            />
          </label>

          <label className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              {...register("activa")}
              className="size-4 rounded border-white/30 bg-slate-800 text-emerald-500 focus:ring-emerald-400"
            />
            Cancha activa
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
              to="/canchas/padel" 
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