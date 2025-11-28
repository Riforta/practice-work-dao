import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import turnosApi from '../../services/turnos.service';
import type { CanchaRef, Turno } from '../../services/turnos.service';
import clientesApi from '../../services/clientes.service';
import type { Cliente } from '../../services/clientes.service';

type FormValues = {
  id_cancha: number;
  fecha: string;
  hora_inicio: string;
  hora_fin: string;
  estado: string;
  precio_final: number;
  id_cliente?: number;
  motivo_bloqueo?: string;
};

const estados = ['disponible', 'reservado', 'bloqueado', 'cancelado', 'finalizado'];

export default function ModificarTurnos() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [canchas, setCanchas] = useState<CanchaRef[]>([]);
  const [todosLosClientes, setTodosLosClientes] = useState<Cliente[]>([]);
  const [clientesBusqueda, setClientesBusqueda] = useState<Cliente[]>([]);
  const [terminoBusqueda, setTerminoBusqueda] = useState('');
  const [clienteSeleccionado, setClienteSeleccionado] = useState<Cliente | null>(null);
  const [mostrarSugerencias, setMostrarSugerencias] = useState(false);

  const {
    register,
    handleSubmit,
    reset,
    watch,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({
    defaultValues: {
      id_cancha: 0,
      fecha: '',
      hora_inicio: '',
      hora_fin: '',
      estado: 'disponible',
      precio_final: 0,
      id_cliente: undefined,
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
        const [turno, canchasList, clientesList] = await Promise.all([
          turnosApi.getById(Number(id)),
          turnosApi.listCanchas(),
          clientesApi.list(),
        ]);
        setCanchas(canchasList);
        setTodosLosClientes(clientesList);
        setClientesBusqueda(clientesList); // Inicialmente mostrar todos
        
        // Separar fecha y hora de los datetime (parsear directamente sin conversión de zona horaria)
        const parseDateTime = (value: string) => {
          if (!value) return { fecha: '', hora: '' };
          
          // Parsear directamente del string ISO sin conversión de zona horaria
          // Formato esperado: "2025-11-28T08:00:00" o "2025-11-28T08:00:00.000Z"
          const cleanValue = value.replace('Z', '').split('.')[0]; // Quitar Z y milisegundos
          const [fecha, hora] = cleanValue.split('T');
          
          if (!fecha || !hora) return { fecha: '', hora: '' };
          
          // Tomar solo HH:MM (sin segundos)
          const horaSinSegundos = hora.substring(0, 5);
          
          return { fecha, hora: horaSinSegundos };
        };

        const inicio = parseDateTime(turno.fecha_hora_inicio);
        const fin = parseDateTime(turno.fecha_hora_fin);

        reset({
          id_cancha: turno.id_cancha,
          fecha: inicio.fecha,
          hora_inicio: inicio.hora,
          hora_fin: fin.hora,
          estado: turno.estado,
          precio_final: turno.precio_final,
          id_cliente: turno.id_cliente,
          motivo_bloqueo: turno.motivo_bloqueo,
        });
        
        // Si hay cliente, cargarlo para mostrarlo
        if (turno.id_cliente) {
          try {
            const cliente = await clientesApi.getById(turno.id_cliente);
            setClienteSeleccionado(cliente);
            setTerminoBusqueda(`${cliente.nombre} ${cliente.apellido || ''}`.trim());
          } catch (err) {
            console.warn('No se pudo cargar el cliente:', err);
          }
        }
      } catch (err) {
        console.error(err);
        setError('No se pudo cargar el turno.');
      } finally {
        setLoading(false);
      }
    };

    void loadData();
  }, [id, reset]);

  // Filtrado de clientes local
  useEffect(() => {
    const termino = terminoBusqueda.trim().toLowerCase();
    
    if (!termino) {
      // Si no hay término, mostrar todos
      setClientesBusqueda(todosLosClientes);
      return;
    }

    // Filtrar localmente
    const filtrados = todosLosClientes.filter((cliente) => {
      const nombreCompleto = `${cliente.nombre} ${cliente.apellido || ''}`.toLowerCase();
      const dni = cliente.dni?.toLowerCase() || '';
      return nombreCompleto.includes(termino) || dni.includes(termino);
    });
    
    setClientesBusqueda(filtrados);
  }, [terminoBusqueda, todosLosClientes]);

  const onSubmit = async (values: FormValues) => {
    if (!id) return;
    setError('');
    try {
      // Combinar fecha con hora_inicio y hora_fin, y convertir a ISO
      const fechaInicio = `${values.fecha}T${values.hora_inicio}:00`;
      const fechaFin = `${values.fecha}T${values.hora_fin}:00`;
      
      const dataToSend: any = {
        id_cancha: values.id_cancha,
        // Enviar directamente sin convertir a ISO (el backend lo manejará)
        fecha_hora_inicio: fechaInicio,
        fecha_hora_fin: fechaFin,
        estado: values.estado,
        precio_final: values.precio_final,
      };
      
      // Solo agregar campos opcionales si tienen valor
      if (values.id_cliente) {
        dataToSend.id_cliente = values.id_cliente;
      }
      
      if (values.motivo_bloqueo && values.motivo_bloqueo.trim()) {
        dataToSend.motivo_bloqueo = values.motivo_bloqueo;
      }
      
      console.log('Datos a enviar:', dataToSend);
      await turnosApi.update(Number(id), dataToSend);
      navigate('/turnos');
    } catch (err: any) {
      console.error('Error completo:', err);
      const errorMsg = err.response?.data?.detail || 'No se pudo actualizar el turno. Intenta nuevamente.';
      setError(errorMsg);
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
    <div 
      className="min-h-screen bg-slate-950 text-white flex items-center justify-center px-4 py-10"
      onClick={() => setMostrarSugerencias(false)}
    >
      <form
        onSubmit={handleSubmit(onSubmit)}
        onClick={(e) => e.stopPropagation()}
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
            Fecha
            <input
              type="date"
              {...register('fecha', { required: 'La fecha es obligatoria' })}
              className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
            />
            {errors.fecha && (
              <span className="text-xs text-red-300">{errors.fecha.message}</span>
            )}
          </label>

          <label className="block text-sm">
            Hora inicio
            <input
              type="time"
              {...register('hora_inicio', { required: 'La hora de inicio es obligatoria' })}
              className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
            />
            {errors.hora_inicio && <span className="text-xs text-red-300">{errors.hora_inicio.message}</span>}
          </label>

          <label className="block text-sm">
            Hora fin
            <input
              type="time"
              {...register('hora_fin', { required: 'La hora de fin es obligatoria' })}
              className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
            />
            {errors.hora_fin && <span className="text-xs text-red-300">{errors.hora_fin.message}</span>}
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

          <label className="block text-sm md:col-span-2 relative">
            Cliente (opcional)
            <input
              type="text"
              value={terminoBusqueda}
              onChange={(e) => {
                setTerminoBusqueda(e.target.value);
                setMostrarSugerencias(true);
                if (!e.target.value) {
                  setClienteSeleccionado(null);
                  reset({ ...watch(), id_cliente: undefined });
                }
              }}
              onFocus={() => {
                setMostrarSugerencias(true);
                // Si no hay búsqueda, mostrar todos
                if (!terminoBusqueda.trim()) {
                  setClientesBusqueda(todosLosClientes);
                }
              }}
              className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
              placeholder="Buscar cliente por nombre..."
            />
            {mostrarSugerencias && !clienteSeleccionado && clientesBusqueda.length > 0 && (
              <div className="absolute z-10 mt-1 w-full rounded-lg bg-slate-800 border border-white/20 shadow-lg max-h-48 overflow-y-auto">
                {clientesBusqueda.map((cliente) => (
                  <button
                    key={cliente.id}
                    type="button"
                    onClick={() => {
                      setClienteSeleccionado(cliente);
                      setTerminoBusqueda(`${cliente.nombre} ${cliente.apellido || ''}`.trim());
                      setMostrarSugerencias(false);
                      reset({ ...watch(), id_cliente: cliente.id });
                    }}
                    className="w-full text-left px-3 py-2 hover:bg-white/10 text-sm text-white"
                  >
                    <div className="font-semibold">{cliente.nombre} {cliente.apellido}</div>
                    {cliente.dni && <div className="text-xs text-emerald-200">DNI: {cliente.dni}</div>}
                  </button>
                ))}
              </div>
            )}
            {clienteSeleccionado && (
              <div className="mt-2 text-xs text-emerald-200">
                Cliente seleccionado: {clienteSeleccionado.nombre} {clienteSeleccionado.apellido} (ID: {clienteSeleccionado.id})
              </div>
            )}
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
