import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { useForm } from 'react-hook-form';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

type FormValues = {
  nombre: string;
  tipo_deporte: string;
  descripcion: string;
  activa: boolean;
};

export default function ModificarCancha() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({
    defaultValues: {
      nombre: '',
      tipo_deporte: '',
      descripcion: '',
      activa: true,
    },
  });

  useEffect(() => {
    const fetchCancha = async () => {
      if (!id || Number.isNaN(Number(id))) {
        setError('ID de cancha inválido.');
        setLoading(false);
        return;
      }
      try {
        const resp = await fetch(`${API_BASE_URL}/api/canchas/${id}`);
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const data = await resp.json();
        reset({
          nombre: data.nombre,
          tipo_deporte: data.tipo_deporte,
          descripcion: data.descripcion,
          activa: data.activa,
        });
      } catch (err) {
        console.error(err);
        setError('No se pudo cargar la cancha.');
      } finally {
        setLoading(false);
      }
    };

    void fetchCancha();
  }, [id, reset]);

  const onSubmit = async (values: FormValues) => {
    if (!id) return;
    setError('');
    try {
      const resp = await fetch(`${API_BASE_URL}/api/canchas/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(values),
      });
      if (!resp.ok) {
        const err = await resp.json();
        throw new Error(err.detail || 'Error al actualizar');
      }
      navigate('/canchas');
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'No se pudo actualizar la cancha. Intenta nuevamente.');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center">
        <p className="text-lg text-emerald-100">Cargando cancha...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white px-4 py-10">
      <div className="max-w-6xl mx-auto space-y-6">
        <form
          onSubmit={handleSubmit(onSubmit)}
          className="w-full max-w-lg mx-auto space-y-4 rounded-2xl bg-white/10 p-6 shadow-2xl backdrop-blur-md border border-white/10"
        >
          <div className="space-y-1">
            <p className="text-sm uppercase tracking-widest text-emerald-200">Canchas</p>
            <h2 className="text-2xl font-bold">Modificar cancha</h2>
            {error && <p className="text-red-300 text-sm">{error}</p>}
          </div>

          <label className="block text-sm">
            Nombre
            <input
              {...register('nombre', { required: 'El nombre es obligatorio' })}
              className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white placeholder:text-emerald-200/60 focus:outline-none focus:ring-2 focus:ring-emerald-400"
              placeholder="Nombre de la cancha"
            />
            {errors.nombre && <span className="text-xs text-red-300">{errors.nombre.message}</span>}
          </label>

          <label className="block text-sm">
            Tipo de Deporte
            <select
              {...register('tipo_deporte', { required: 'Selecciona un deporte' })}
              className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
            >
              <option value="">Seleccionar...</option>
              <option value="futbol">Fútbol</option>
              <option value="basquet">Básquet</option>
              <option value="padel">Pádel</option>
            </select>
            {errors.tipo_deporte && <span className="text-xs text-red-300">{errors.tipo_deporte.message}</span>}
          </label>

          <label className="block text-sm">
            Descripción
            <textarea
              {...register('descripcion')}
              className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white placeholder:text-emerald-200/60 focus:outline-none focus:ring-2 focus:ring-emerald-400"
              rows={3}
              placeholder="Descripción opcional"
            />
          </label>

          <label className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              {...register('activa')}
              className="size-4 rounded border-white/30 bg-slate-800 text-emerald-500 focus:ring-emerald-400"
            />
            Cancha activa
          </label>

          <div className="flex flex-wrap gap-3 pt-2">
            <button
              type="submit"
              disabled={isSubmitting}
              className="rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400 disabled:opacity-60"
            >
              {isSubmitting ? 'Guardando...' : 'Actualizar'}
            </button>
            <button
              type="button"
              onClick={() => reset()}
              className="rounded-lg border border-white/20 bg-white/5 px-4 py-2 text-sm text-emerald-100 hover:border-emerald-400"
            >
              Restaurar
            </button>
            <Link
              to="/canchas"
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
