import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import turnosApi from '../../services/turnos.service';
import type { CanchaRef, Turno } from '../../services/turnos.service';

type FormValues = {
  id_cancha: number;
  fecha_hora_inicio: string;
  fecha_hora_fin: string;
  estado: string;
  precio_final: number;
  id_cliente?: number;
  id_usuario_registro?: number;
  motivo_bloqueo?: string;
};

const estados = ['disponible', 'reservado', 'bloqueado', 'cancelado', 'finalizado'];

export default function ModificarTurnos() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [canchas, setCanchas] = useState<CanchaRef[]>([]);

  const {
    register,
    handleSubmit,
    reset,
    watch,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({
    defaultValues: {
      id_cancha: 0,
      fecha_hora_inicio: '',
      fecha_hora_fin: '',
      estado: 'disponible',
      precio_final: 0,
      id_cliente: undefined,
      id_usuario_registro: undefined,
      motivo_bloqueo: '',
    },
  });

  useEffect(() => {
    const loadData = async () => {
      if (!id || Number.isNaN(Number(id))) {
        setError('ID de turno inválido.');
        setLoading(false);
        return;
      }
      try {
        const [turno, canchasList] = await Promise.all([
          turnosApi.getById(Number(id)),
          turnosApi.listCanchas(),
        ]);
        setCanchas(canchasList);
        const parseDate = (value: string) => {
          if (!value) return '';
          // Adaptar ISO a formato datetime-local (sin Z y sin segundos)
          const d = new Date(value);
          if (Number.isNaN(d.getTime())) return value;
          const pad = (n: number) => n.toString().padStart(2, '0');
          return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(
            d.getMinutes()
          )}`;
        };

        reset({
          id_cancha: turno.id_cancha,
          fecha_hora_inicio: parseDate(turno.fecha_hora_inicio),
          fecha_hora_fin: parseDate(turno.fecha_hora_fin),
          estado: turno.estado,
          precio_final: turno.precio_final,
          id_cliente: turno.id_cliente,
          id_usuario_registro: turno.id_usuario_registro,
          motivo_bloqueo: turno.motivo_bloqueo,
        });
      } catch (err) {
        console.error(err);
        setError('No se pudo cargar el turno.');
      } finally {
        setLoading(false);
      }
    };

    void loadData();
  }, [id, reset]);

  const onSubmit = async (values: FormValues) => {
    if (!id) return;
    setError('');
    try {
      await turnosApi.update(Number(id), values as Partial<Turno>);
      navigate('/turnos');
    } catch (err) {
      console.error(err);
      setError('No se pudo actualizar el turno. Intenta nuevamente.');
    }
  };

  const estadoSeleccionado = watch('estado');

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center">
        <p className="text-lg text-emerald-100">Cargando turno...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center px-4 py-10">
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="w-full max-w-3xl space-y-4 rounded-2xl bg-white/10 p-6 shadow-2xl backdrop-blur-md border border-white/10"
      >
        <div className="space-y-1">
          <p className="text-sm uppercase tracking-widest text-emerald-200">Turnos</p>
          <h2 className="text-2xl font-bold">Modificar turno</h2>
          {error && <p className="text-red-300 text-sm">{error}</p>}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <label className="block text-sm">
            Cancha
            <select
              {...register('id_cancha', { required: 'Selecciona una cancha', valueAsNumber: true, min: 1 })}
              className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
            >
              <option value={0}>-- Selecciona --</option>
              {canchas.map((c) => (
                <option key={c.id} value={c.id} className="bg-slate-900">
                  {c.nombre} {c.tipo_deporte ? `(${c.tipo_deporte})` : ''}
                </option>
              ))}
            </select>
            {errors.id_cancha && <span className="text-xs text-red-300">{errors.id_cancha.message}</span>}
          </label>

          <label className="block text-sm">
            Estado
            <select
              {...register('estado', { required: 'Selecciona un estado' })}
              className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
            >
              {estados.map((estado) => (
                <option key={estado} value={estado} className="bg-slate-900">
                  {estado}
                </option>
              ))}
            </select>
            {errors.estado && <span className="text-xs text-red-300">{errors.estado.message}</span>}
          </label>

          <label className="block text-sm">
            Fecha y hora inicio
            <input
              type="datetime-local"
              {...register('fecha_hora_inicio', { required: 'La fecha de inicio es obligatoria' })}
              className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
            />
            {errors.fecha_hora_inicio && (
              <span className="text-xs text-red-300">{errors.fecha_hora_inicio.message}</span>
            )}
          </label>

          <label className="block text-sm">
            Fecha y hora fin
            <input
              type="datetime-local"
              {...register('fecha_hora_fin', { required: 'La fecha de fin es obligatoria' })}
              className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
            />
            {errors.fecha_hora_fin && <span className="text-xs text-red-300">{errors.fecha_hora_fin.message}</span>}
          </label>

          <label className="block text-sm">
            Precio final
            <input
              type="number"
              step="0.01"
              {...register('precio_final', {
                required: 'El precio es obligatorio',
                valueAsNumber: true,
                min: { value: 0, message: 'Debe ser mayor o igual a 0' },
              })}
              className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
              placeholder="0.00"
            />
            {errors.precio_final && <span className="text-xs text-red-300">{errors.precio_final.message}</span>}
          </label>

          <label className="block text-sm">
            ID Cliente (opcional)
            <input
              type="number"
              {...register('id_cliente', { valueAsNumber: true })}
              className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
              placeholder="Ej: 5"
            />
          </label>

          <label className="block text-sm">
            ID Usuario registro (opcional)
            <input
              type="number"
              {...register('id_usuario_registro', { valueAsNumber: true })}
              className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
              placeholder="Ej: 1"
            />
          </label>

          {estadoSeleccionado === 'bloqueado' && (
            <label className="block text-sm md:col-span-2">
              Motivo de bloqueo
              <textarea
                {...register('motivo_bloqueo')}
                className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
                rows={2}
                placeholder="Opcional, describe el motivo"
              />
            </label>
          )}
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
            to="/turnos"
            className="rounded-lg border border-white/20 bg-white/0 px-4 py-2 text-sm text-emerald-100 hover:border-emerald-400"
          >
            Volver
          </Link>
        </div>
      </form>
    </div>
  );
}
