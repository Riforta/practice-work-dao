import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import clientesApi from '../../services/clientes.service';

type FormValues = {
  nombre: string;
  apellido: string;
  dni: string;
  telefono: string;
  email: string;
};

export default function RegistrarCliente() {
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
    defaultValues: { nombre: '', apellido: '', dni: '', telefono: '', email: '' },
    mode: 'onChange',
  });

  const fieldsOrder: (keyof FormValues)[] = ['nombre', 'apellido', 'dni', 'telefono', 'email'];

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
      await clientesApi.create(values as any);
      navigate('/clientes');
    } catch (err: any) {
      // Mostrar detalle del backend si existe
      const serverMsg = err?.response?.data?.detail
        || err?.response?.data?.message
        || (typeof err?.response?.data === 'string' ? err.response.data : '')
        || err?.message;
      console.error('Error creando cliente:', err?.response?.status, err?.response?.data);
      setError(serverMsg ? `No se pudo registrar el cliente: ${serverMsg}` : 'No se pudo registrar el cliente. Revisa los datos e intenta nuevamente.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white px-4 py-10">
      <div className="max-w-6xl mx-auto space-y-6">
        <form onSubmit={handleFormSubmit} className="w-full max-w-3xl mx-auto space-y-4 rounded-2xl bg-white/10 p-6 shadow-2xl backdrop-blur-md border border-white/10">
          <div className="space-y-1">
            <p className="text-sm uppercase tracking-widest text-emerald-200">Clientes</p>
            <h2 className="text-2xl font-bold">Registrar cliente</h2>
            {error && <p className="text-red-300 text-sm">{error}</p>}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <label className="block text-sm">
              Nombre
              <input
                {...register('nombre', { 
                  required: 'El nombre es obligatorio',
                  minLength: { value: 2, message: 'El nombre debe tener al menos 2 caracteres' }
                })}
                className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white placeholder:text-emerald-200/60 focus:outline-none focus:ring-2 focus:ring-emerald-400"
                placeholder="Ej: Juan"
              />
              {currentErrorField === 'nombre' && errors.nombre && <span className="text-xs text-red-300">{errors.nombre.message}</span>}
            </label>

            <label className="block text-sm">
              Apellido
              <input
                {...register('apellido', { 
                  required: 'El apellido es obligatorio',
                  minLength: { value: 2, message: 'El apellido debe tener al menos 2 caracteres' }
                })}
                className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white placeholder:text-emerald-200/60 focus:outline-none focus:ring-2 focus:ring-emerald-400"
                placeholder="Ej: Pérez"
              />
              {currentErrorField === 'apellido' && errors.apellido && <span className="text-xs text-red-300">{errors.apellido.message}</span>}
            </label>

            <label className="block text-sm">
              DNI
              <input
                {...register('dni', { 
                  required: 'El DNI es obligatorio',
                  pattern: { value: /^[0-9]{7,8}$/, message: 'El DNI debe tener 7 u 8 dígitos' }
                })}
                className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white placeholder:text-emerald-200/60 focus:outline-none focus:ring-2 focus:ring-emerald-400"
                placeholder="Ej: 12345678"
              />
              {currentErrorField === 'dni' && errors.dni && <span className="text-xs text-red-300">{errors.dni.message}</span>}
            </label>

            <label className="block text-sm">
              Teléfono
              <input
                {...register('telefono', { 
                  required: 'El teléfono es obligatorio',
                  minLength: { value: 8, message: 'El teléfono debe tener al menos 8 caracteres' }
                })}
                className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white placeholder:text-emerald-200/60 focus:outline-none focus:ring-2 focus:ring-emerald-400"
                placeholder="Ej: 11 5555-5555"
              />
              {currentErrorField === 'telefono' && errors.telefono && <span className="text-xs text-red-300">{errors.telefono.message}</span>}
            </label>

            <label className="block text-sm md:col-span-2">
              Email
              <input
                type="email"
                {...register('email', { 
                  required: 'El email es obligatorio',
                  pattern: { 
                    value: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/, 
                    message: 'Ingresa un email válido' 
                  }
                })}
                className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white placeholder:text-emerald-200/60 focus:outline-none focus:ring-2 focus:ring-emerald-400"
                placeholder="Ej: juan@mail.com"
              />
              {currentErrorField === 'email' && errors.email && <span className="text-xs text-red-300">{errors.email.message}</span>}
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
                reset({ nombre: '', apellido: '', dni: '', telefono: '', email: '' });
                setCurrentErrorField(null);
              }}
              className="rounded-lg border border-white/20 bg-white/5 px-4 py-2 text-sm text-emerald-100 hover:border-emerald-400"
            >
              Limpiar
            </button>
            <Link
              to="/clientes"
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
