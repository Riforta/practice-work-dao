import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

type FormValues = {
  nombre: string;
  tipo_deporte: string;
  descripcion: string;
  activa: boolean;
};

export default function RegistrarCancha() {
  const navigate = useNavigate();
  const [error, setError] = useState('');
  const [currentErrorField, setCurrentErrorField] = useState<keyof FormValues | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const {
    register,
    reset,
    trigger,
    getValues,
    formState: { errors },
  } = useForm<FormValues>({
    defaultValues: { nombre: '', tipo_deporte: '', descripcion: '', activa: true },
    mode: 'onChange',
  });

  const fieldsOrder: (keyof FormValues)[] = ['nombre', 'tipo_deporte'];

  const validateNextField = async () => {
    for (const field of fieldsOrder) {
      const isValid = await trigger(field);
      if (!isValid) {
        setCurrentErrorField(field);
        return false;
      }
    }
    setCurrentErrorField(null);
    return true;
  };

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const isValid = await validateNextField();
    if (!isValid) return;

    setError('');
    setIsSubmitting(true);
    try {
      const values = getValues();
      const resp = await fetch(`${API_BASE_URL}/api/canchas/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(values)
      });
      
      if (!resp.ok) {
        const errorData = await resp.json();
        throw new Error(errorData.detail || 'Error al registrar');
      }
      
      navigate('/canchas');
    } catch (err: any) {
      const serverMsg = err?.message || '';
      setError(serverMsg ? `No se pudo registrar la cancha: ${serverMsg}` : 'No se pudo registrar la cancha. Revisa los datos e intenta nuevamente.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white px-4 py-10">
      <div className="max-w-6xl mx-auto space-y-6">
        <form onSubmit={handleFormSubmit} className="w-full max-w-3xl mx-auto space-y-4 rounded-2xl bg-white/10 p-6 shadow-2xl backdrop-blur-md border border-white/10">
          <div className="space-y-1">
            <p className="text-sm uppercase tracking-widest text-emerald-200">Canchas</p>
            <h2 className="text-2xl font-bold">Registrar cancha</h2>
            {error && <p className="text-red-300 text-sm">{error}</p>}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <label className="block text-sm">
              Nombre
              <input
                {...register('nombre', { 
                  required: 'El nombre es obligatorio',
                  minLength: { value: 3, message: 'El nombre debe tener al menos 3 caracteres' }
                })}
                className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white placeholder:text-emerald-200/60 focus:outline-none focus:ring-2 focus:ring-emerald-400"
                placeholder="Ej: Cancha Fútbol 1"
              />
              {currentErrorField === 'nombre' && errors.nombre && <span className="text-xs text-red-300">{errors.nombre.message}</span>}
            </label>

            <label className="block text-sm">
              Tipo de Deporte
              <select
                {...register('tipo_deporte', { 
                  required: 'El tipo de deporte es obligatorio'
                })}
                className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white placeholder:text-emerald-200/60 focus:outline-none focus:ring-2 focus:ring-emerald-400"
              >
                <option value="">Seleccionar...</option>
                <option value="futbol">Fútbol</option>
                <option value="basquet">Básquet</option>
                <option value="padel">Pádel</option>
              </select>
              {currentErrorField === 'tipo_deporte' && errors.tipo_deporte && <span className="text-xs text-red-300">{errors.tipo_deporte.message}</span>}
            </label>

            <label className="block text-sm md:col-span-2">
              Descripción
              <textarea
                {...register('descripcion')}
                className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white placeholder:text-emerald-200/60 focus:outline-none focus:ring-2 focus:ring-emerald-400"
                placeholder="Descripción de la cancha..."
                rows={4}
              />
            </label>

            <label className="flex items-center gap-2 text-sm md:col-span-2">
              <input
                type="checkbox"
                {...register('activa')}
                className="w-4 h-4 rounded"
              />
              Cancha activa (disponible para reservas)
            </label>
          </div>

          <div className="flex flex-wrap gap-3 pt-2">
            <button
              type="submit"
              disabled={isSubmitting}
              className="rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400 disabled:opacity-60"
            >
              {isSubmitting ? 'Guardando...' : 'Registrar'}
            </button>
            <button
              type="button"
              onClick={() => {
                reset({ nombre: '', tipo_deporte: '', descripcion: '', activa: true });
                setCurrentErrorField(null);
              }}
              className="rounded-lg border border-white/20 bg-white/5 px-4 py-2 text-sm text-emerald-100 hover:border-emerald-400"
            >
              Limpiar
            </button>
            <Link
              to="/canchas"
              className="rounded-lg border border-white/20 bg-white/0 px-4 py-2 text-sm text-emerald-100 hover:border-emerald-400"
            >
              Cancelar
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
