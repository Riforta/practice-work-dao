import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { useForm } from 'react-hook-form';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

type FormValues = {
  nombre: string;
  apellido: string;
  dni: string;
  telefono: string;
  email: string;
};

export default function ModificarCliente() {
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
      apellido: '',
      dni: '',
      telefono: '',
      email: '',
    },
  });

  useEffect(() => {
    const fetchCliente = async () => {
      if (!id || Number.isNaN(Number(id))) {
        setError('ID de cliente inválido.');
        setLoading(false);
        return;
      }
      try {
        const resp = await fetch(`${API_BASE_URL}/api/clientes/${id}`);
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const data = await resp.json();
        reset({
          nombre: data.nombre,
          apellido: data.apellido,
          dni: data.dni,
          telefono: data.telefono,
          email: data.email,
        });
      } catch (err) {
        console.error(err);
        setError('No se pudo cargar el cliente.');
      } finally {
        setLoading(false);
      }
    };

    void fetchCliente();
  }, [id, reset]);

  const onSubmit = async (values: FormValues) => {
    if (!id) return;
    setError('');
    try {
      const resp = await fetch(`${API_BASE_URL}/api/clientes/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(values),
      });
      if (!resp.ok) {
        const err = await resp.json();
        throw new Error(err.detail || 'Error al actualizar');
      }
      navigate('/clientes');
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'No se pudo actualizar el cliente. Intenta nuevamente.');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center">
        <p className="text-lg text-emerald-100">Cargando cliente...</p>
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
            <p className="text-sm uppercase tracking-widest text-emerald-200">Clientes</p>
            <h2 className="text-2xl font-bold">Modificar cliente</h2>
            {error && <p className="text-red-300 text-sm">{error}</p>}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <label className="block text-sm">
              Nombre
              <input
                {...register('nombre', { required: 'El nombre es obligatorio' })}
                className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white placeholder:text-emerald-200/60 focus:outline-none focus:ring-2 focus:ring-emerald-400"
                placeholder="Nombre"
              />
              {errors.nombre && <span className="text-xs text-red-300">{errors.nombre.message}</span>}
            </label>

            <label className="block text-sm">
              Apellido
              <input
                {...register('apellido', { required: 'El apellido es obligatorio' })}
                className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white placeholder:text-emerald-200/60 focus:outline-none focus:ring-2 focus:ring-emerald-400"
                placeholder="Apellido"
              />
              {errors.apellido && <span className="text-xs text-red-300">{errors.apellido.message}</span>}
            </label>

            <label className="block text-sm">
              DNI
              <input
                {...register('dni', { required: 'El DNI es obligatorio' })}
                className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white placeholder:text-emerald-200/60 focus:outline-none focus:ring-2 focus:ring-emerald-400"
                placeholder="DNI"
              />
              {errors.dni && <span className="text-xs text-red-300">{errors.dni.message}</span>}
            </label>

            <label className="block text-sm">
              Email
              <input
                type="email"
                {...register('email', { required: 'El email es obligatorio' })}
                className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white placeholder:text-emerald-200/60 focus:outline-none focus:ring-2 focus:ring-emerald-400"
                placeholder="Email"
              />
              {errors.email && <span className="text-xs text-red-300">{errors.email.message}</span>}
            </label>

            <label className="block text-sm md:col-span-2">
              Teléfono
              <input
                type="tel"
                {...register('telefono', { required: 'El teléfono es obligatorio' })}
                className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white placeholder:text-emerald-200/60 focus:outline-none focus:ring-2 focus:ring-emerald-400"
                placeholder="Teléfono"
              />
              {errors.telefono && <span className="text-xs text-red-300">{errors.telefono.message}</span>}
            </label>
          </div>

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
              to="/clientes"
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
