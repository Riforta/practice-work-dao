import { useEffect, useMemo, useState } from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import pagosService from '../../services/pagos.service';
import clientesService, { type Cliente } from '../../services/clientes.service';
import turnosService, { type Turno, type CanchaRef } from '../../services/turnos.service';
import serviciosService, { type ServicioAdicional } from '../../services/servicios.service';

type FormValues = {
	id_cliente: number;
	id_turno?: number | null;
	monto_turno: number;
	metodo_pago: string;
	estado: string;
};

const metodosPago = ['efectivo', 'tarjeta', 'transferencia', 'mercadopago', 'otro'];
const estados = ['iniciado', 'completado', 'fallido'];

const formatDateRange = (inicio?: string, fin?: string) => {
	if (!inicio) return 'Sin horario';
	try {
		const start = new Date(inicio);
		const end = fin ? new Date(fin) : null;
		const format = new Intl.DateTimeFormat('es-AR', {
			dateStyle: 'short',
			timeStyle: 'short',
		});
		const startTxt = format.format(start);
		return end ? `${startTxt} → ${format.format(end)}` : startTxt;
	} catch {
		return inicio;
	}
};

const formatCurrency = (value: number) => {
	return new Intl.NumberFormat('es-AR', {
		style: 'currency',
		currency: 'ARS'
	}).format(value);
};

export default function RegistrarPago() {
	const navigate = useNavigate();
	const {
		register,
		handleSubmit,
		formState: { errors, isSubmitting },
		watch,
		setValue,
	} = useForm<FormValues>({
		defaultValues: {
			monto_turno: 0,
			metodo_pago: metodosPago[0],
			estado: 'completado',
		},
	});

	const [error, setError] = useState('');
	const [success, setSuccess] = useState('');
	const [clientes, setClientes] = useState<Cliente[]>([]);
	const [clientesLoading, setClientesLoading] = useState(true);
	const [clienteSearch, setClienteSearch] = useState('');
	const [turnos, setTurnos] = useState<Turno[]>([]);
	const [canchas, setCanchas] = useState<CanchaRef[]>([]);
	const [turnosLoading, setTurnosLoading] = useState(true);
	const [turnoSearch, setTurnoSearch] = useState('');
	const [incluirTurno, setIncluirTurno] = useState(false);
	const [servicios, setServicios] = useState<ServicioAdicional[]>([]);
	const [serviciosLoading, setServiciosLoading] = useState(true);
	const [serviciosSeleccionados, setServiciosSeleccionados] = useState<Set<number>>(new Set());

	const montoTurnoValue = watch('monto_turno');
	const idTurnoValue = watch('id_turno');

	// Actualizar monto cuando se selecciona un turno
	useEffect(() => {
		if (idTurnoValue && incluirTurno) {
			const turno = turnos.find(t => t.id === Number(idTurnoValue));
			if (turno && turno.precio_final) {
				setValue('monto_turno', turno.precio_final);
			}
		}
	}, [idTurnoValue, turnos, incluirTurno, setValue]);

	const montoServicios = useMemo(() => {
		return Array.from(serviciosSeleccionados).reduce((acc, id) => {
			const servicio = servicios.find(s => s.id === id);
			return acc + (servicio?.precio_actual ?? 0);
		}, 0);
	}, [serviciosSeleccionados, servicios]);

	const montoTotal = useMemo(() => {
		const turno = typeof montoTurnoValue === 'number' ? montoTurnoValue : 0;
		return turno + montoServicios;
	}, [montoTurnoValue, montoServicios]);

	useEffect(() => {
		const loadData = async () => {
			setClientesLoading(true);
			setTurnosLoading(true);
			setServiciosLoading(true);
			try {
				const [clientesData, turnosData, canchasData, serviciosData] = await Promise.all([
					clientesService.list(),
					turnosService.list(),
					turnosService.listCanchas(),
					serviciosService.list(),
				]);
				setClientes(clientesData);
				setTurnos(turnosData);
				setCanchas(canchasData);
				setServicios(serviciosData.filter(s => s.activo));
			} catch (err) {
				console.error(err);
				setError('No se pudieron cargar los datos.');
			} finally {
				setClientesLoading(false);
				setTurnosLoading(false);
				setServiciosLoading(false);
			}
		};
		void loadData();
	}, []);

	const clientesFiltrados = useMemo(() => {
		const term = clienteSearch.trim().toLowerCase();
		return clientes.filter((cliente) => {
			const nombreCompleto = `${cliente.nombre} ${cliente.apellido || ''}`.toLowerCase();
			return term ? nombreCompleto.includes(term) : true;
		});
	}, [clientes, clienteSearch]);

	const canchaMap = useMemo(() => {
		const map = new Map<number, CanchaRef>();
		canchas.forEach((c) => map.set(c.id, c));
		return map;
	}, [canchas]);

	const turnosDisponibles = useMemo(() => {
		return turnos.filter((t) => t.estado === 'disponible' || t.estado === 'reservado');
	}, [turnos]);

	const turnosFiltrados = useMemo(() => {
		if (!turnoSearch.trim()) return turnosDisponibles;
		
		const term = turnoSearch.trim().toLowerCase();
		return turnosDisponibles.filter((t) => {
			const cancha = canchaMap.get(t.id_cancha);
			const canchaText = cancha?.nombre ?? '';
			const idText = `#${t.id}`;
			const fechaText = formatDateRange(t.fecha_hora_inicio, t.fecha_hora_fin);
			const estadoText = t.estado ?? '';
			
			const texto = `${idText} ${canchaText} ${fechaText} ${estadoText}`.toLowerCase();
			return texto.includes(term);
		});
	}, [turnosDisponibles, turnoSearch, canchaMap]);

	const toggleServicio = (id: number) => {
		setServiciosSeleccionados(prev => {
			const next = new Set(prev);
			if (next.has(id)) {
				next.delete(id);
			} else {
				next.add(id);
			}
			return next;
		});
	};

	const onSubmit = async (values: FormValues) => {
		setError('');
		setSuccess('');
		try {
			const payload = {
				id_cliente: Number(values.id_cliente),
				id_turno: incluirTurno && values.id_turno ? Number(values.id_turno) : null,
				monto_turno: Number(values.monto_turno),
				monto_servicios: montoServicios,
				monto_total: montoTotal,
				metodo_pago: values.metodo_pago,
				estado: values.estado,
			};

			console.log('Enviando payload:', payload);
			await pagosService.crearPagoManual(payload);
			setSuccess('Pago registrado correctamente. Redirigiendo...');
			setTimeout(() => navigate('/pagos'), 800);
		} catch (err: any) {
			console.error('Error completo:', err);
			console.error('Error response:', err.response);
			const errorMsg = err.response?.data?.detail || err.message || 'Error desconocido';
			setError(`No se pudo registrar el pago: ${errorMsg}`);
		}
	};

	return (
		<div className="min-h-screen bg-slate-950 text-white px-4 py-10">
			<div className="max-w-4xl mx-auto space-y-6">
				<header className="space-y-2">
					<p className="text-sm uppercase tracking-widest text-emerald-200">Pagos</p>
					<h1 className="text-3xl font-bold">Registrar pago manual</h1>
					{error && <p className="text-red-300 text-sm">{error}</p>}
					{success && <p className="text-emerald-200 text-sm">{success}</p>}
				</header>

				<form
					onSubmit={handleSubmit(onSubmit)}
					className="space-y-6 rounded-2xl bg-white/5 p-6 shadow-2xl border border-white/10"
				>
					<section className="space-y-4 rounded-2xl border border-white/10 bg-slate-900/40 p-4">
						<h2 className="text-lg font-semibold">Cliente</h2>
						<div>
							<input
								type="search"
								value={clienteSearch}
								onChange={(e) => setClienteSearch(e.target.value)}
								placeholder="Buscar cliente..."
								className="w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm mb-3"
							/>
							<div className="max-h-48 overflow-y-auto rounded-xl border border-white/5 bg-slate-950/60">
								{clientesLoading ? (
									<p className="p-4 text-sm text-emerald-100">Cargando clientes...</p>
								) : clientesFiltrados.length === 0 ? (
									<p className="p-4 text-sm text-emerald-100">No hay clientes disponibles.</p>
								) : (
									<div className="divide-y divide-white/5">
										{clientesFiltrados.map((cliente) => (
											<label key={cliente.id} className="flex items-center gap-3 p-3 hover:bg-white/5 cursor-pointer">
												<input
													type="radio"
													value={cliente.id}
													{...register('id_cliente', { required: 'Selecciona un cliente' })}
													className="size-4"
												/>
												<div>
													<p className="font-semibold text-sm">
														{cliente.nombre} {cliente.apellido}
													</p>
													<p className="text-xs text-emerald-100">DNI: {cliente.dni || 'N/A'}</p>
												</div>
											</label>
										))}
									</div>
								)}
							</div>
							{errors.id_cliente && <span className="text-xs text-red-300">{errors.id_cliente.message}</span>}
						</div>
					</section>

					<section className="space-y-4 rounded-2xl border border-white/10 bg-slate-900/40 p-4">
						<div className="flex items-center gap-3">
							<input
								type="checkbox"
								checked={incluirTurno}
								onChange={(e) => {
									setIncluirTurno(e.target.checked);
									if (!e.target.checked) setValue('id_turno', null);
								}}
								className="size-4"
							/>
							<h2 className="text-lg font-semibold">Asociar a un turno (opcional)</h2>
						</div>
						{incluirTurno && (
							<div>
								<div className="mb-3">
									<input
										type="search"
										value={turnoSearch}
										onChange={(e) => setTurnoSearch(e.target.value)}
										placeholder="Buscar por ID, cancha, fecha o estado..."
										className="w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm"
									/>
									<p className="text-xs text-emerald-100/70 mt-1">
										Ejemplo: "Futbol", "27/11", "#123", "disponible"
									</p>
								</div>
								<div className="max-h-64 overflow-y-auto rounded-xl border border-white/5 bg-slate-950/60">
									{turnosLoading ? (
										<p className="p-4 text-sm text-emerald-100">Cargando turnos...</p>
									) : turnosFiltrados.length === 0 ? (
										<p className="p-4 text-sm text-emerald-100">
											{turnoSearch.trim() ? 'No se encontraron turnos con ese criterio.' : 'No hay turnos disponibles.'}
										</p>
									) : (
										<div className="divide-y divide-white/5">
											{turnosFiltrados.map((turno) => {
												const cancha = canchaMap.get(turno.id_cancha);
												return (
													<label key={turno.id} className="flex items-start gap-3 p-3 hover:bg-white/5 cursor-pointer">
														<input
															type="radio"
															value={turno.id}
															{...register('id_turno')}
															className="size-4 mt-1"
														/>
														<div className="flex-1 min-w-0">
															<div className="flex items-center gap-2 flex-wrap">
																<p className="font-semibold text-sm">
																	{cancha?.nombre ?? `Cancha ${turno.id_cancha}`}
																</p>
																<span className="text-xs px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-200">
																	{turno.estado}
																</span>
																<span className="text-xs text-emerald-100/60">
																	#{turno.id}
																</span>
															</div>
															<p className="text-xs text-emerald-100 mt-1">
																{formatDateRange(turno.fecha_hora_inicio, turno.fecha_hora_fin)}
															</p>
															{turno.precio_final && (
																<p className="text-xs text-emerald-200 font-semibold mt-1">
																	{formatCurrency(turno.precio_final)}
																</p>
															)}
														</div>
													</label>
												);
											})}
										</div>
									)}
								</div>
							</div>
						)}
					</section>

					<section className="space-y-4 rounded-2xl border border-white/10 bg-slate-900/40 p-4">
						<h2 className="text-lg font-semibold">Servicios adicionales</h2>
						{serviciosLoading ? (
							<p className="text-sm text-emerald-100">Cargando servicios...</p>
						) : servicios.length === 0 ? (
							<p className="text-sm text-emerald-100">No hay servicios disponibles.</p>
						) : (
							<div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
								{servicios.map((servicio) => {
									const isSelected = serviciosSeleccionados.has(servicio.id!);
									return (
										<label
											key={servicio.id}
											className={`flex items-start gap-3 p-3 rounded-lg border cursor-pointer transition-colors ${
												isSelected
													? 'border-emerald-500 bg-emerald-500/10'
													: 'border-white/10 bg-slate-950/40 hover:border-emerald-500/50'
											}`}
										>
											<input
												type="checkbox"
												checked={isSelected}
												onChange={() => toggleServicio(servicio.id!)}
												className="size-4 mt-1"
											/>
											<div className="flex-1">
												<p className="font-semibold text-sm">{servicio.nombre}</p>
												<p className="text-xs text-emerald-200 font-mono mt-1">
													{formatCurrency(servicio.precio_actual)}
												</p>
											</div>
										</label>
									);
								})}
							</div>
						)}
						{serviciosSeleccionados.size > 0 && (
							<div className="rounded-lg bg-emerald-500/10 border border-emerald-500/30 p-3">
								<p className="text-sm text-emerald-200">
									<span className="font-semibold">Total servicios:</span> {formatCurrency(montoServicios)}
								</p>
							</div>
						)}
					</section>

					<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
						<label className="text-sm">
							Monto turno
							<input
								type="number"
								step="0.01"
								min={0}
								{...register('monto_turno', { 
									valueAsNumber: true,
									min: { value: 0, message: 'Debe ser mayor o igual a 0' }
								})}
								className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm"
								placeholder="0.00"
							/>
							{errors.monto_turno && <span className="text-xs text-red-300">{errors.monto_turno.message}</span>}
						</label>

						<div className="text-sm">
							<label className="block mb-2">Monto servicios</label>
							<div className="rounded-lg bg-slate-900/50 px-3 py-2.5 text-sm border border-emerald-500/30">
								<span className="font-semibold text-emerald-200">
									{formatCurrency(montoServicios)}
								</span>
								<span className="text-xs text-emerald-100/70 ml-2">
									({serviciosSeleccionados.size} {serviciosSeleccionados.size === 1 ? 'servicio' : 'servicios'})
								</span>
							</div>
						</div>

						<label className="text-sm">
							Método de pago
							<select
								{...register('metodo_pago', { required: 'Selecciona un método' })}
								className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm"
							>
								{metodosPago.map((metodo) => (
									<option key={metodo} value={metodo} className="bg-slate-900">
										{metodo}
									</option>
								))}
							</select>
							{errors.metodo_pago && <span className="text-xs text-red-300">{errors.metodo_pago.message}</span>}
						</label>

						<label className="text-sm">
							Estado
							<select
								{...register('estado', { required: 'Selecciona un estado' })}
								className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm"
							>
								{estados.map((estado) => (
									<option key={estado} value={estado} className="bg-slate-900">
										{estado}
									</option>
								))}
							</select>
							{errors.estado && <span className="text-xs text-red-300">{errors.estado.message}</span>}
						</label>
					</div>

					<div className="rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-4">
						<p className="text-emerald-200 font-semibold text-lg">
							Monto Total: ${montoTotal.toFixed(2)}
						</p>
					</div>

					<div className="flex flex-wrap gap-3">
						<button
							type="submit"
							disabled={isSubmitting}
							className="rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400 disabled:opacity-60"
						>
							{isSubmitting ? 'Registrando...' : 'Registrar pago'}
						</button>
						<button
							type="button"
							onClick={() => navigate('/pagos')}
							className="rounded-lg border border-white/20 px-4 py-2 text-sm text-emerald-100 hover:border-emerald-400"
						>
							Cancelar
						</button>
					</div>
				</form>
			</div>
		</div>
	);
}
