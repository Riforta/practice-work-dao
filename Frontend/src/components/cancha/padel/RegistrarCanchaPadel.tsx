import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import service from '../../../services/canchas.service';

interface FormData {
  nombre: string;
  descripcion: string;
  activa: boolean;
  precio_hora: number;
  tipo_deporte: string;
}

export default function RegistrarCanchaPadel() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm<FormData>({
    defaultValues: {
      tipo_deporte: 'padel',
      activa: true,
      precio_hora: 0
    }
  });

  const onSubmit = async (data: FormData) => {
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const allCanchas = await service.getAllCanchasPadel();
      const exists = allCanchas.some(
        (c: any) => c.nombre.toLowerCase() === data.nombre.toLowerCase()
      );

      if (exists) {
        setError('Ya existe una cancha de pádel con ese nombre.');
        setLoading(false);
        return;
      }

      const payload = {
        ...data,
        tipo_deporte: 'padel'
      };

      await service.creatCanchaPadel(payload);
      setSuccess('¡Cancha de pádel creada con éxito!');
      setTimeout(() => {
        navigate('/canchas/padel');
      }, 1500);
    } catch (err: any) {
      console.error('Error al crear cancha:', err);
      setError(err?.response?.data?.detail || 'Error al crear la cancha.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white px-4 py-10">
      <div className="max-w-3xl mx-auto space-y-6">
        <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <p className="text-sm uppercase tracking-widest text-emerald-200">Nueva Cancha</p>
            <h1 className="text-3xl font-bold">Registrar Cancha de Pádel</h1>
          </div>
          <button
            onClick={() => navigate('/canchas/padel')}
            className="min-w-[10rem] rounded-lg bg-white/10 px-4 py-2 text-sm font-semibold text-emerald-100 hover:bg-white/20"
          >
            Volver
          </button>
        </header>

        {error && (
          <div className="rounded-xl border border-red-500/30 bg-red-500/10 p-4">
            <p className="text-sm text-red-200">{error}</p>
          </div>
        )}

        {success && (
          <div className="rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-4">
            <p className="text-sm text-emerald-200">{success}</p>
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="rounded-2xl border border-white/10 bg-white/5 p-6 space-y-6">
          <div className="space-y-4">
            <div>
              <label className="block mb-2 text-sm font-semibold text-emerald-200">
                Nombre de la Cancha *
              </label>
              <input
                type="text"
                {...register('nombre', { required: 'El nombre es obligatorio' })}
                className="w-full rounded-lg bg-slate-900/80 px-4 py-2 text-sm text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                placeholder="Ej: Cancha Pádel Central"
              />
              {errors.nombre && (
                <p className="text-xs text-red-300 mt-1">{errors.nombre.message}</p>
              )}
            </div>

            <div>
              <label className="block mb-2 text-sm font-semibold text-emerald-200">
                Descripción
              </label>
              <textarea
                {...register('descripcion')}
                rows={4}
                className="w-full rounded-lg bg-slate-900/80 px-4 py-2 text-sm text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                placeholder="Describe las características de la cancha..."
              />
            </div>

            <div>
              <label className="block mb-2 text-sm font-semibold text-emerald-200">
                Tipo de Deporte
              </label>
              <input
                type="text"
                value="Pádel"
                disabled
                className="w-full rounded-lg bg-slate-800/50 px-4 py-2 text-sm text-gray-400 cursor-not-allowed"
              />
              <p className="text-xs text-gray-400 mt-1">Este campo se establece automáticamente.</p>
            </div>

            <div>
              <label className="block mb-2 text-sm font-semibold text-emerald-200">
                Precio por Hora *
              </label>
              <input
                type="number"
                step="0.01"
                {...register('precio_hora', {
                  required: 'El precio es obligatorio',
                  min: { value: 0, message: 'El precio debe ser mayor o igual a 0' }
                })}
                className="w-full rounded-lg bg-slate-900/80 px-4 py-2 text-sm text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                placeholder="0.00"
              />
              {errors.precio_hora && (
                <p className="text-xs text-red-300 mt-1">{errors.precio_hora.message}</p>
              )}
            </div>

            <div className="flex items-center gap-3">
              <input
                type="checkbox"
                id="activa"
                {...register('activa')}
                className="w-5 h-5 rounded bg-slate-900 border-white/20 text-emerald-500 focus:ring-2 focus:ring-emerald-500"
              />
              <label htmlFor="activa" className="text-sm font-semibold text-emerald-200 cursor-pointer">
                Cancha activa
              </label>
            </div>
          </div>

          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={() => navigate('/canchas/padel')}
              disabled={loading}
              className="flex-1 rounded-lg bg-white/10 px-4 py-2 text-sm font-semibold text-emerald-100 hover:bg-white/20 disabled:opacity-50"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex-1 rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400 disabled:opacity-50"
            >
              {loading ? 'Guardando...' : 'Crear Cancha'}
            </button>
          </div>
        </form>

        <div className="rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-4">
          <p className="text-xs text-emerald-200">
            <span className="font-semibold">Nota:</span> Los campos marcados con * son obligatorios.
          </p>
        </div>
      </div>
    </div>
  );
}
