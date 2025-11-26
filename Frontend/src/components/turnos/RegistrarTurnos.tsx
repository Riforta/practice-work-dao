import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import turnosApi from '../../services/turnos.service';
import clientesApi from '../../services/clientes.service';
import tarifasApi from '../../services/tarifas.service';
import serviciosApi from '../../services/servicios.service';
import type { CanchaRef } from '../../services/turnos.service';
import type { Cliente } from '../../services/clientes.service';
import type { Tarifa } from '../../services/tarifas.service';
import type { ServicioAdicional } from '../../services/servicios.service';

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

export default function RegistrarTurnos() {
  const navigate = useNavigate();
  const [error, setError] = useState('');
  const [canchas, setCanchas] = useState<CanchaRef[]>([]);
  const [loadingCanchas, setLoadingCanchas] = useState(true);
  const [clienteTerm, setClienteTerm] = useState('');
  const [clienteOptions, setClienteOptions] = useState<Cliente[]>([]);
  const [allClientes, setAllClientes] = useState<Cliente[]>([]);
  const [showClienteList, setShowClienteList] = useState(false);
  const [showHoraInicio, setShowHoraInicio] = useState(false);
  const [showHoraFin, setShowHoraFin] = useState(false);
  const [tarifas, setTarifas] = useState<Tarifa[]>([]);
  const [servicios, setServicios] = useState<ServicioAdicional[]>([]);
  const [luzAplicada, setLuzAplicada] = useState<{ aplicada: boolean; monto: number }>({
    aplicada: false,
    monto: 0,
  });

  const {
    register,
    handleSubmit,
    reset,
    watch,
    setValue,
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

  const estadoSeleccionado = watch('estado');
  const horaInicio = watch('hora_inicio');
  const horaFin = watch('hora_fin');
  const canchaSeleccionada = watch('id_cancha');

  useEffect(() => {
    const fetchCanchasYClientes = async () => {
      try {
        const [canchasList, clientesList, tarifasList, serviciosList] = await Promise.all([
          turnosApi.listCanchas(),
          clientesApi.list(),
          tarifasApi.list(),
          serviciosApi.list(),
        ]);
        setCanchas(canchasList);
        setAllClientes(clientesList);
        setClienteOptions(clientesList);
        setTarifas(tarifasList);
        setServicios(serviciosList);
      } catch (err) {
        console.error(err);
        setError('No se pudieron cargar canchas, clientes o tarifas/servicios.');
      } finally {
        setLoadingCanchas(false);
      }
    };
    void fetchCanchasYClientes();
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      const term = clienteTerm.trim().toLowerCase();
      if (!term) {
        setClienteOptions(allClientes);
        return;
      }
      const filtered = allClientes.filter((c) => {
        const full = `${c.nombre ?? ''} ${c.apellido ?? ''}`.toLowerCase();
        return full.includes(term);
      });
      setClienteOptions(filtered);
    }, 150);

    return () => clearTimeout(timer);
  }, [clienteTerm, allClientes]);

  // Recalcular precio final en base a tarifa, horas y luz
  useEffect(() => {
    if (!horaInicio || !horaFin) {
      setValue('precio_final', 0, { shouldValidate: false });
      return;
    }

    const [h1, m1] = horaInicio.split(':').map(Number);
    const [h2, m2] = horaFin.split(':').map(Number);
    if ([h1, m1, h2, m2].some((n) => Number.isNaN(n))) {
      setValue('precio_final', 0, { shouldValidate: false });
      return;
    }

    const startMinutes = h1 * 60 + m1;
    const endMinutes = h2 * 60 + m2;
    if (endMinutes <= startMinutes) {
      setValue('precio_final', 0, { shouldValidate: false });
      return;
    }

    const durationHours = (endMinutes - startMinutes) / 60;
    const tarifa = tarifas.find((t) => t.id_cancha === canchaSeleccionada);
    const baseHora = tarifa?.precio_hora ?? 0;
    let total = durationHours * baseHora;

    // Agregar servicio de luz si el rango toca noche (>=19:00) o madrugada (<07:00)
    const lucesActivas = servicios.filter((s) => (s.nombre ?? '').toLowerCase().includes('luz') && s.activo);
    const tocaNoche = endMinutes >= 19 * 60 || startMinutes < 7 * 60;
    let luzMonto = 0;
    if (tocaNoche && lucesActivas.length > 0) {
      const luzMayor = lucesActivas.reduce(
        (max, curr) => (curr.precio_actual > max.precio_actual ? curr : max),
        lucesActivas[0]
      );
      const luzTotal = durationHours * luzMayor.precio_actual;
      total += luzTotal;
      luzMonto = luzTotal;
    }

    setLuzAplicada({ aplicada: luzMonto > 0, monto: luzMonto });

    setValue('precio_final', Number(total.toFixed(2)), { shouldValidate: false });
  }, [canchaSeleccionada, horaInicio, horaFin, tarifas, servicios, setValue]);

  const onSubmit = async (values: FormValues) => {
    setError('');
    try {
      const { fecha, hora_inicio, hora_fin, ...rest } = values;
      const fechaInicio = fecha && hora_inicio ? `${fecha}T${hora_inicio}` : '';
      const fechaFin = fecha && hora_fin ? `${fecha}T${hora_fin}` : '';
      const idCliente = Number(values.id_cliente);
      const clienteValido = Number.isFinite(idCliente) && idCliente > 0;
      const payload = {
        ...rest,
        fecha_hora_inicio: fechaInicio,
        fecha_hora_fin: fechaFin,
        id_cliente: clienteValido ? idCliente : undefined,
      };
      if (!fechaInicio || !fechaFin) {
        setError('Completa fecha, hora inicio y hora fin.');
        return;
      }
      // Validar que la hora fin sea posterior a la hora inicio
      const start = new Date(fechaInicio).getTime();
      const end = new Date(fechaFin).getTime();
      if (Number.isNaN(start) || Number.isNaN(end) || end <= start) {
        setError('La hora fin debe ser posterior a la hora inicio.');
        return;
      }
      const now = Date.now();
      if (start < now) {
        setError('No se puede crear un turno en una fecha/hora pasada.');
        return;
      }
      if (values.estado === 'reservado' && !clienteValido) {
        setError('Debes seleccionar un cliente para un turno reservado.');
        return;
      }
      if (!rest.precio_final || rest.precio_final <= 0) {
        setError('No se pudo calcular el precio. Revisa la tarifa y los horarios.');
        return;
      }
      await turnosApi.create(payload);
      navigate('/turnos');
    } catch (err) {
      console.error(err);
      setError('No se pudo registrar el turno. Revisa los datos e intenta nuevamente.');
    }
  };

  const handleSelectCliente = (id: number) => {
    const c = clienteOptions.find((cli) => cli.id === id);
    setValue('id_cliente', id);
    setClienteTerm(c ? `${c.nombre} ${c.apellido ?? ''}`.trim() : clienteTerm);
    setShowClienteList(false);
  };

  const handleClearCliente = () => {
    setValue('id_cliente', undefined);
    setClienteTerm('');
    setClienteOptions([]);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center px-4 py-10">
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="w-full max-w-3xl space-y-4 rounded-2xl bg-white/10 p-6 shadow-2xl backdrop-blur-md border border-white/10"
      >
        <div className="space-y-1">
          <p className="text-sm uppercase tracking-widest text-emerald-200">Turnos</p>
          <h2 className="text-2xl font-bold">Registrar turno</h2>
          {error && <p className="text-red-300 text-sm">{error}</p>}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <label className="block text-sm">
            Cancha
            <select
              {...register('id_cancha', { required: 'Selecciona una cancha', valueAsNumber: true, min: 1 })}
              className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
              disabled={loadingCanchas}
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
            Fecha (misma para inicio y fin)
            <input
              type="date"
              {...register('fecha', { required: 'La fecha es obligatoria' })}
              className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
            />
            {errors.fecha && <span className="text-xs text-red-300">{errors.fecha.message}</span>}
          </label>

          <label className="block text-sm">
            Hora inicio
            <input type="hidden" {...register('hora_inicio', { required: 'La hora de inicio es obligatoria' })} />
            <div className="relative">
              <button
                type="button"
                onClick={() => {
                  setShowHoraInicio((p) => !p);
                  setShowHoraFin(false);
                }}
                className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white text-left focus:outline-none focus:ring-2 focus:ring-emerald-400"
              >
                {horaInicio ? horaInicio : '-- Selecciona --'}
              </button>
              {showHoraInicio && (
                <div className="absolute z-20 mt-1 max-h-60 w-full overflow-auto rounded-lg border border-white/10 bg-slate-900/95 shadow-xl">
                  {Array.from({ length: 24 }).map((_, h) =>
                    ['00', '30'].map((m) => {
                      const val = `${h.toString().padStart(2, '0')}:${m}`;
                      return (
                        <button
                          type="button"
                          key={val}
                          className="w-full text-left px-3 py-2 text-sm hover:bg-white/10 cursor-pointer"
                          onMouseDown={(e) => {
                            e.preventDefault();
                            setValue('hora_inicio', val, { shouldValidate: true });
                            setShowHoraInicio(false);
                          }}
                        >
                          {val}
                        </button>
                      );
                    })
                  )}
                </div>
              )}
            </div>
            {errors.hora_inicio && <span className="text-xs text-red-300">{errors.hora_inicio.message}</span>}
          </label>

          <label className="block text-sm">
            Hora fin
            <input type="hidden" {...register('hora_fin', { required: 'La hora de fin es obligatoria' })} />
            <div className="relative">
              <button
                type="button"
                onClick={() => {
                  setShowHoraFin((p) => !p);
                  setShowHoraInicio(false);
                }}
                className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white text-left focus:outline-none focus:ring-2 focus:ring-emerald-400"
              >
                {horaFin ? horaFin : '-- Selecciona --'}
              </button>
              {showHoraFin && (
                <div className="absolute z-20 mt-1 max-h-60 w-full overflow-auto rounded-lg border border-white/10 bg-slate-900/95 shadow-xl">
                  {Array.from({ length: 24 }).map((_, h) =>
                    ['00', '30'].map((m) => {
                      const val = `${h.toString().padStart(2, '0')}:${m}`;
                      return (
                        <button
                          type="button"
                          key={val}
                          className="w-full text-left px-3 py-2 text-sm hover:bg-white/10 cursor-pointer"
                          onMouseDown={(e) => {
                            e.preventDefault();
                            setValue('hora_fin', val, { shouldValidate: true });
                            setShowHoraFin(false);
                          }}
                        >
                          {val}
                        </button>
                      );
                    })
                  )}
                </div>
              )}
            </div>
            {errors.hora_fin && <span className="text-xs text-red-300">{errors.hora_fin.message}</span>}
          </label>

          <label className="block text-sm">
            Precio final
            <input
              type="number"
              step="0.01"
              {...register('precio_final', { valueAsNumber: true })}
              className="mt-2 w-full rounded-lg bg-slate-900/50 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
              placeholder="0.00"
              readOnly
            />
            {errors.precio_final && <span className="text-xs text-red-300">{errors.precio_final.message}</span>}
            {luzAplicada.aplicada && (
              <p className="text-xs text-emerald-200 mt-1">
                Incluye servicio de luz (+${luzAplicada.monto.toFixed(2)})
              </p>
            )}
          </label>

          <input type="hidden" {...register('id_cliente', { valueAsNumber: true })} />

          <label className="block text-sm md:col-span-2 relative">
            Cliente (escribe y selecciona)
            <div className="mt-2 flex gap-2">
              <input
                value={clienteTerm}
                onChange={(e) => {
                  setClienteTerm(e.target.value);
                  setShowClienteList(true);
                }}
                onFocus={() => setShowClienteList(true)}
                className="flex-1 rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
                placeholder="Ej: Juan Perez"
                autoComplete="off"
              />
              <button
                type="button"
                onClick={handleClearCliente}
                className="rounded-lg border border-white/20 bg-white/5 px-3 py-2 text-sm text-emerald-100 hover:border-emerald-400"
              >
                Limpiar
              </button>
            </div>
            {showClienteList && (
              <ul className="absolute z-10 mt-1 max-h-56 w-full overflow-auto rounded-lg border border-white/10 bg-slate-900/95 shadow-xl">
                {clienteOptions.length === 0 && (
                  <li className="px-3 py-2 text-sm text-emerald-200">Sin resultados</li>
                )}
                {clienteOptions.map((c) => (
                  <li
                    key={c.id}
                    className="px-3 py-2 text-sm hover:bg-white/10 cursor-pointer"
                    onMouseDown={(e) => {
                      e.preventDefault();
                      handleSelectCliente(c.id);
                    }}
                  >
                    <div className="font-semibold">{c.nombre} {c.apellido}</div>
                    <div className="text-xs text-emerald-200">{c.email ?? c.telefono ?? ''}</div>
                  </li>
                ))}
              </ul>
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
            {isSubmitting ? 'Guardando...' : 'Registrar'}
          </button>
          <button
            type="button"
            onClick={() =>
      reset({
        id_cancha: 0,
        fecha: '',
        hora_inicio: '',
        hora_fin: '',
        estado: 'disponible',
        precio_final: 0,
        id_cliente: undefined,
        motivo_bloqueo: '',
      })
            }
            className="rounded-lg border border-white/20 bg-white/5 px-4 py-2 text-sm text-emerald-100 hover:border-emerald-400"
          >
            Limpiar
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
