import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import service from "../../../services/canchas.service";

type FormData = {
  nombre: string;
  tipo_deporte: string;
  descripcion: string;
  activa: boolean;
  precio_hora: number;
};

export default function RegistroCanchaFutbol() {
  const [errorMessage, setErrorMessage] = useState("");
  const [loading, setLoading] = useState(false);
  
  const { register, handleSubmit, formState: { errors }, reset } = useForm<FormData>({
    defaultValues: { tipo_deporte: "futbol", activa: true }
  });
  
  const navigate = useNavigate();

  const onSubmit = async (data: FormData) => {
    setErrorMessage("");
    setLoading(true);

    try {
      const coincidencias = await service.getCanchaFutbolByName(data.nombre);
      
      const existeDuplicado = coincidencias.some((c: any) => 
        c.nombre.trim().toLowerCase() === data.nombre.trim().toLowerCase()
      );

      if (existeDuplicado) {
        setErrorMessage("Ya existe una cancha con ese nombre. Por favor elija otro.");
        setLoading(false);
        return;
      }

      await service.creatCanchaFutbol(data);
      navigate("/canchas/futbol");

    } catch (error) {
      console.error(error);
      setErrorMessage("Error al conectar con el servidor. Intente nuevamente.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white px-4 py-10">
      <div className="max-w-2xl mx-auto space-y-6">
        <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <p className="text-sm uppercase tracking-widest text-emerald-200">Nueva Cancha</p>
            <h1 className="text-3xl font-bold">Registrar Cancha de Fútbol</h1>
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
            <p className="text-xs text-gray-400 mt-1">Este campo se establece automáticamente.</p>
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
              defaultChecked
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
              {loading ? 'Registrando...' : 'Registrar Cancha'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}