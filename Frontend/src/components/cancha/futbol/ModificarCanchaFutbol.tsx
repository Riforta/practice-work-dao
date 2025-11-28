import React, { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate, useParams } from "react-router-dom";
import service from "../../../services/canchas.service";

type FormData = {
  nombre: string;
  tipo_deporte: string;
  descripcion: string;
  activa: boolean;
  precio_hora: number;
};

export default function ModificarCanchaFutbol() {
  const { register, handleSubmit, formState: { errors }, setValue, reset } = useForm<FormData>();
  const params = useParams();
  const navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [loadingData, setLoadingData] = useState(true);

  const id = params.id || params.Id || params.Id_Cancha;

  useEffect(() => {
    if (!id) return;
    const fetchCancha = async () => {
      setLoadingData(true);
      try {
        const data: any = await service.getByIdFutbol(Number(id));
        if (!data) {
          setErrorMessage("No se encontró la cancha.");
          return;
        }
        
        setValue("nombre", data.nombre ?? data.Nombre ?? "");
        setValue("tipo_deporte", (data.tipo_deporte ?? data.deporte ?? "").toString().toLowerCase());
        setValue("descripcion", data.descripcion ?? "");
        setValue("activa", Boolean(data.activa));
        setValue("precio_hora", data.precio_hora ?? 0);
      } catch (err) {
        console.error(err);
        setErrorMessage("No se pudo cargar la cancha.");
      } finally {
        setLoadingData(false);
      }
    };
    fetchCancha();
  }, [id, setValue]);

  const onSubmit = async (form: FormData) => {
    setErrorMessage("");
    setLoading(true);

    try {
      const canchasConEseNombre = await service.getCanchaFutbolByName(form.nombre);
      
      const existeDuplicado = canchasConEseNombre.some((c: any) => 
        c.nombre.toLowerCase() === form.nombre.toLowerCase() && 
        (c.id || c.Id) !== Number(id)
      );

      if (existeDuplicado) {
        setErrorMessage("Ya existe otra cancha con ese nombre. Por favor elija uno distinto.");
        setLoading(false);
        return;
      }

      const payload = {
        nombre: form.nombre,
        tipo_deporte: form.tipo_deporte,
        descripcion: form.descripcion,
        activa: form.activa,
        precio_hora: form.precio_hora,
      };
      
      await service.actualizarCancha(Number(id), payload);
      navigate("/canchas/futbol"); 
      
    } catch (err) {
      console.error(err);
      setErrorMessage("Error al actualizar la cancha. Verifique los datos o la conexión.");
    } finally {
      setLoading(false);
    }
  };

  if (loadingData) {
    return (
      <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center">
        <div className="text-emerald-200">Cargando datos...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white px-4 py-10">
      <div className="max-w-2xl mx-auto space-y-6">
        <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <p className="text-sm uppercase tracking-widest text-emerald-200">Editar Cancha</p>
            <h1 className="text-3xl font-bold">Modificar Cancha de Fútbol</h1>
          </div>
          <button
            onClick={() => navigate('/canchas/futbol')}
            className="min-w-[10rem] rounded-lg bg-white/10 px-4 py-2 text-sm font-semibold text-emerald-100 hover:bg-white/20"
          >
            Volver
          </button>
        </header>

        <form
          onSubmit={handleSubmit(onSubmit)}
          className="rounded-2xl border border-white/10 bg-white/5 p-6 space-y-4"
        >
          {errorMessage && (
            <div className="rounded-lg bg-red-500/20 border border-red-500/50 text-red-200 p-3 text-sm">
              {errorMessage}
            </div>
          )}

          <div>
            <label className="block text-sm font-medium mb-2 text-emerald-200">Nombre</label>
            <input
              {...register("nombre", { required: "El nombre es requerido" })}
              className="w-full px-3 py-2 rounded-lg bg-slate-900/80 border border-white/10 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              placeholder="Nombre de la cancha"
            />
            {errors.nombre && <p className="text-red-400 text-sm mt-1">{errors.nombre.message}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium mb-2 text-emerald-200">Tipo de Deporte</label>
            <input
              type="text"
              value="Fútbol"
              disabled
              className="w-full px-3 py-2 rounded-lg bg-slate-800/50 border border-white/10 text-gray-400 cursor-not-allowed"
            />
            <p className="text-xs text-gray-400 mt-1">Este campo no se puede modificar.</p>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2 text-emerald-200">Descripción</label>
            <textarea
              {...register("descripcion")}
              className="w-full px-3 py-2 rounded-lg bg-slate-900/80 border border-white/10 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              rows={3}
              placeholder="Descripción breve"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2 text-emerald-200">Precio por Hora</label>
            <input
              type="number"
              min={10}
              step={1}
              {...register("precio_hora", {
                required: "El precio es requerido",
                valueAsNumber: true,
                min: { value: 10, message: "El precio debe ser mayor o igual a 10" },
              })}
              className="w-full px-3 py-2 rounded-lg bg-slate-900/80 border border-white/10 text-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
              placeholder="0"
            />
            {errors.precio_hora && <p className="text-red-400 text-sm mt-1">{errors.precio_hora.message}</p>}
          </div>

          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              {...register("activa")}
              className="w-4 h-4 rounded text-emerald-500 bg-slate-900/80 border-white/10 focus:ring-2 focus:ring-emerald-500"
            />
            <label className="text-sm text-emerald-100">Cancha activa</label>
          </div>

          <div className="flex justify-end gap-3 pt-4">
            <button
              type="button"
              onClick={() => navigate('/canchas/futbol')}
              disabled={loading}
              className="px-4 py-2 rounded-lg bg-white/10 text-emerald-100 hover:bg-white/20 font-semibold transition-colors disabled:opacity-50"
            >
              Cancelar
            </button>
            <button
              type="button"
              onClick={() => { reset(); setErrorMessage(""); }}
              className="px-4 py-2 rounded-lg bg-white/10 text-emerald-100 hover:bg-white/20 font-semibold transition-colors"
            >
              Limpiar
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 rounded-lg bg-emerald-500 text-slate-950 hover:bg-emerald-400 font-semibold transition-colors disabled:opacity-50"
            >
              {loading ? 'Actualizando...' : 'Actualizar Cancha'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}