import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import serviciosApi from '../../services/servicios.service';

type FormValues = {
  nombre: string;
  precio_actual: number;
  activo: boolean;
};

export default function ModificarServicios() {
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
      precio_actual: 0,
      activo: true,
    },
  });

  useEffect(() => {
    const fetchServicio = async () => {
      if (!id || Number.isNaN(Number(id))) {
        setError('ID de servicio inválido.');
        setLoading(false);
        return;
      }
      try {
        const data = await serviciosApi.getById(Number(id));
        reset({
          nombre: data.nombre,
          precio_actual: data.precio_actual,
          activo: data.activo,
        });
      } catch (err) {
        console.error(err);
        setError('No se pudo cargar el servicio.');
      } finally {
        setLoading(false);
      }
    };

    void fetchServicio();
  }, [id, reset]);

  const onSubmit = async (values: FormValues) => {
    if (!id) return;
    setError('');
    try {
      await serviciosApi.update(Number(id), values);
      navigate('/servicios');
    } catch (err) {
      console.error(err);
      setError('No se pudo actualizar el servicio. Intenta nuevamente.');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-emerald-900 text-white flex items-center justify-center">
        <p className="text-lg text-emerald-100">Cargando servicio...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-emerald-900 text-white flex items-center justify-center px-4 py-10">
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="w-full max-w-lg space-y-4 rounded-2xl bg-white/10 p-6 shadow-2xl backdrop-blur-md border border-white/10"
      >
        <div className="space-y-1">
          <p className="text-sm uppercase tracking-widest text-emerald-200">Servicios adicionales</p>
          <h2 className="text-2xl font-bold">Modificar servicio</h2>
          {error && <p className="text-red-300 text-sm">{error}</p>}
        </div>

        <label className="block text-sm">
          Nombre
          <input
            {...register('nombre', { required: 'El nombre es obligatorio' })}
            className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white placeholder:text-emerald-200/60 focus:outline-none focus:ring-2 focus:ring-emerald-400"
            placeholder="Ej: Buffet, Estacionamiento..."
          />
          {errors.nombre && <span className="text-xs text-red-300">{errors.nombre.message}</span>}
        </label>

        <label className="block text-sm">
          Precio actual
          <input
            type="number"
            step="0.01"
            {...register('precio_actual', {
              required: 'El precio es obligatorio',
              min: { value: 0, message: 'Debe ser mayor o igual a 0' },
              valueAsNumber: true,
            })}
            className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white placeholder:text-emerald-200/60 focus:outline-none focus:ring-2 focus:ring-emerald-400"
            placeholder="0.00"
          />
          {errors.precio_actual && <span className="text-xs text-red-300">{errors.precio_actual.message}</span>}
        </label>

        <label className="flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            {...register('activo')}
            className="size-4 rounded border-white/30 bg-slate-800 text-emerald-500 focus:ring-emerald-400"
          />
          Servicio activo
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
            to="/servicios"
            className="rounded-lg border border-white/20 bg-white/0 px-4 py-2 text-sm text-emerald-100 hover:border-emerald-400"
          >
            Volver
          </Link>
        </div>
      </form>
    </div>
  );
}
