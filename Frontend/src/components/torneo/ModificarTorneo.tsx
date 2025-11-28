import { useEffect, useMemo, useState } from 'react';
import { useForm } from 'react-hook-form';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import torneosApi, { type Torneo } from '../../services/torneo.service';
import turnosApi, { type Turno, type CanchaRef } from '../../services/turnos.service';
import equiposService, { type Equipo } from '../../services/equipos.service';
import equipoTorneoApi, { type EquipoTorneo } from '../../services/equipoTorneo.service';

type FormValues = {
	nombre: string;
	tipo_deporte: string;
	fecha_inicio?: string | null;
	fecha_fin?: string | null;
	costo_inscripcion?: number;
	cupos?: number | null;
	reglas?: string | null;
	estado?: string | null;
};

const estadoLabels: Record<string, string> = {
	planificado: 'Planificado',
	inscripciones_abiertas: 'Inscripciones abiertas',
	en_curso: 'En curso',
	finalizado: 'Finalizado',
	cancelado: 'Cancelado',
};
const estadoKeys = Object.keys(estadoLabels);

const normalizeEstadoValue = (value?: string | null) => {
	if (!value) return estadoKeys[0];
	const lower = value.toLowerCase();
	if (estadoKeys.includes(lower)) return lower;
	const normalized = lower.replace(/\s+/g, '_');
	if (estadoKeys.includes(normalized)) return normalized;
	const match = estadoKeys.find((key) => estadoLabels[key].toLowerCase() === lower);
	return match ?? estadoKeys[0];
};

const toFieldNumber = (value?: number | null) =>
	typeof value === 'number' && Number.isFinite(value) ? value : undefined;

const toPayloadNumberOrZero = (value?: number | null) =>
	typeof value === 'number' && Number.isFinite(value) ? value : 0;

const toPayloadNumberOrNull = (value?: number | null) =>
	typeof value === 'number' && Number.isFinite(value) ? value : null;

const formatRange = (inicio?: string | null, fin?: string | null) => {
	if (!inicio) return 'Sin horario';
	const start = new Date(inicio);
	const end = fin ? new Date(fin) : null;
	const formatter = new Intl.DateTimeFormat('es-AR', { dateStyle: 'short' });
	return end ? `${formatter.format(start)} → ${formatter.format(end)}` : formatter.format(start);
};

export default function ModificarTorneo() {
	const { id } = useParams<{ id: string }>();
	const torneoId = Number(id);
	const navigate = useNavigate();
	const { user } = useAuth();
	const currentUserId = (user?.id ?? user?.ID ?? user?.id_usuario) as number | undefined;

	const todayISO = useMemo(() => {
		const today = new Date();
		today.setHours(0, 0, 0, 0);
		return today.toISOString().split('T')[0];
	}, []);

	const {
		register,
		handleSubmit,
		formState: { errors, isSubmitting },
		reset,
		watch,
	} = useForm<FormValues>();

	const fechaInicioValue = watch('fecha_inicio');
	const cuposValue = watch('cupos');
	const minFechaFin = fechaInicioValue && fechaInicioValue > todayISO ? fechaInicioValue : todayISO;

	const [error, setError] = useState('');
	const [success, setSuccess] = useState('');
	const [loading, setLoading] = useState(true);
	const [torneo, setTorneo] = useState<Torneo | null>(null);
	const [turnos, setTurnos] = useState<Turno[]>([]);
	const [canchas, setCanchas] = useState<CanchaRef[]>([]);
	const [selectedTurnos, setSelectedTurnos] = useState<number[]>([]);
	const [originalTurnos, setOriginalTurnos] = useState<number[]>([]);
	const [search, setSearch] = useState('');
	const [canchaFiltro, setCanchaFiltro] = useState<'todos' | number>('todos');
	const [equipos, setEquipos] = useState<Equipo[]>([]);
	const [equiposLoading, setEquiposLoading] = useState(true);
	const [equiposError, setEquiposError] = useState('');
	const [equipoSearch, setEquipoSearch] = useState('');
	const [selectedEquipos, setSelectedEquipos] = useState<number[]>([]);
	const [originalEquipos, setOriginalEquipos] = useState<number[]>([]);
	const [equipoFeedback, setEquipoFeedback] = useState('');

	useEffect(() => {
		const loadData = async () => {
			if (!torneoId) return;
			setLoading(true);
			setError('');
			setEquiposLoading(true);
			setEquiposError('');
			try {
			const [torneoData, turnosData, canchasData, equiposList, equiposTorneoList] = await Promise.all([
				torneosApi.getById(torneoId),
				turnosApi.list(),
				turnosApi.listCanchas(),
				equiposService.getAllEquipos(),
				equipoTorneoApi.listarEquiposPorTorneo(torneoId),
			]);
				setTorneo(torneoData);
				reset({
					nombre: torneoData.nombre,
					tipo_deporte: torneoData.tipo_deporte,
					fecha_inicio: torneoData.fecha_inicio ?? undefined,
					fecha_fin: torneoData.fecha_fin ?? undefined,
					costo_inscripcion: toFieldNumber(torneoData.costo_inscripcion),
					cupos: toFieldNumber(torneoData.cupos),
					reglas: torneoData.reglas,
					estado: normalizeEstadoValue(torneoData.estado),
				});
				setTurnos(turnosData);
				setCanchas(canchasData);
				setEquipos(equiposList);
				setEquiposError('');
				const asignados = turnosData
					.filter((t) => t.motivo_bloqueo?.includes(`Torneo:${torneoId}`))
					.map((t) => t.id!)
					.filter(Boolean);
				setSelectedTurnos(asignados);
				setOriginalTurnos(asignados);
			const equiposAsignados = equiposTorneoList.map((et: EquipoTorneo) => et.id_equipo);
			setSelectedEquipos(equiposAsignados);
			setOriginalEquipos(equiposAsignados);
			} catch (err) {
				console.error(err);
				setError('No se pudo cargar el torneo.');
				setEquiposError('No se pudieron cargar los equipos inscritos.');
			} finally {
				setLoading(false);
				setEquiposLoading(false);
			}
		};
		void loadData();
	}, [torneoId, reset]);

	const canchaMap = useMemo(() => {
		const map = new Map<number, CanchaRef>();
		canchas.forEach((c) => map.set(c.id, c));
		return map;
	}, [canchas]);

	const turnosMostrables = useMemo(() => {
		const term = search.trim().toLowerCase();
		const assignedSet = new Set(originalTurnos);
		return turnos
			.filter((turno) => turno.estado === 'disponible' || assignedSet.has(turno.id!))
			.filter((turno) => {
				const cancha = canchaMap.get(turno.id_cancha);
				const coincideCancha = canchaFiltro === 'todos' ? true : turno.id_cancha === canchaFiltro;
				const texto = `${cancha?.nombre ?? ''} ${formatRange(turno.fecha_hora_inicio, turno.fecha_hora_fin)}`.toLowerCase();
				const coincideSearch = term ? texto.includes(term) : true;
				return coincideCancha && coincideSearch;
			});
	}, [turnos, canchaMap, canchaFiltro, search, originalTurnos]);

	const equiposFiltrados = useMemo(() => {
		const term = equipoSearch.trim().toLowerCase();
		return equipos.filter((equipo) =>
			term ? equipo.nombre_equipo.toLowerCase().includes(term) : true
		);
	}, [equipos, equipoSearch]);

	const equiposMap = useMemo(() => {
		const map = new Map<number, Equipo>();
		equipos.forEach((equipo) => {
			if (equipo.id) {
				map.set(equipo.id, equipo);
			}
		});
		return map;
	}, [equipos]);

	const capacidadMaxima = useMemo(() => {
		return typeof cuposValue === 'number' && Number.isFinite(cuposValue) && cuposValue > 0 ? cuposValue : null;
	}, [cuposValue]);

	const cuposRestantes = capacidadMaxima != null ? Math.max(capacidadMaxima - selectedEquipos.length, 0) : null;

	const toggleTurno = (turnoId: number) => {
		setSelectedTurnos((prev) =>
			prev.includes(turnoId) ? prev.filter((id) => id !== turnoId) : [...prev, turnoId]
		);
	};

	const toggleEquipo = (equipoId: number) => {
		setEquipoFeedback('');
		setSelectedEquipos((prev) => {
			const already = prev.includes(equipoId);
			if (already) {
				return prev.filter((id) => id !== equipoId);
			}
			if (capacidadMaxima != null && prev.length >= capacidadMaxima) {
				setEquipoFeedback('No quedan cupos disponibles para agregar más equipos.');
				return prev;
			}
			return [...prev, equipoId];
		});
	};

	const onSubmit = async (values: FormValues) => {
		if (!torneoId) return;
		setError('');
		setSuccess('');
		try {
			const capacidadDeclarada =
				typeof values.cupos === 'number' && Number.isFinite(values.cupos) ? values.cupos : null;
			if (capacidadDeclarada != null && selectedEquipos.length > capacidadDeclarada) {
				setError('Seleccionaste más equipos que los cupos declarados.');
				return;
			}
			await torneosApi.update(torneoId, {
				nombre: values.nombre.trim(),
				tipo_deporte: values.tipo_deporte,
				fecha_inicio: values.fecha_inicio || null,
				fecha_fin: values.fecha_fin || null,
				costo_inscripcion: toPayloadNumberOrZero(values.costo_inscripcion),
				cupos: toPayloadNumberOrNull(values.cupos),
				reglas: values.reglas ?? null,
				estado: normalizeEstadoValue(values.estado),
			});

			const turnosAAsignar = selectedTurnos.filter((id) => !originalTurnos.includes(id));
			const turnosALiberar = originalTurnos.filter((id) => !selectedTurnos.includes(id));

			if (turnosALiberar.length) {
				await torneosApi.releaseTurnosFromTorneo(turnosALiberar);
			}
			if (turnosAAsignar.length) {
				await torneosApi.assignTurnosToTorneo(torneoId, turnosAAsignar, currentUserId);
			}
            

			const equiposAAgregar = selectedEquipos.filter((id) => !originalEquipos.includes(id));
			const equiposAQuitar = originalEquipos.filter((id) => !selectedEquipos.includes(id));

			if (equiposAQuitar.length) {
				const inscripcionesAEliminar: Array<[number, number]> = equiposAQuitar.map(equipoId => [equipoId, torneoId]);
				await equipoTorneoApi.desinscribirEquiposMasivo(inscripcionesAEliminar);
			}
			if (equiposAAgregar.length) {
				await equipoTorneoApi.assignEquiposToTorneo(torneoId, equiposAAgregar);
			}

			setSuccess('Cambios guardados correctamente.');
			setOriginalTurnos(selectedTurnos);
			setOriginalEquipos(selectedEquipos);
			setTimeout(() => navigate('/torneos/ConsultarTorneos'), 800);
		} catch (err) {
			console.error(err);
			setError('No se pudo actualizar el torneo.');
		}
	};

	if (!torneoId) {
		return (
			<div className="min-h-screen bg-slate-950 px-4 py-10 text-center text-red-200">
				Identificador de torneo inválido.
			</div>
		);
	}

	return (
		<div className="min-h-screen bg-slate-950 px-4 py-10 text-white">
			<div className="mx-auto flex max-w-5xl flex-col gap-6">
				<header className="space-y-2">
					<p className="text-xs uppercase tracking-widest text-emerald-300">Torneos</p>
					<h1 className="text-3xl font-bold">Editar torneo</h1>
					{torneo && <p className="text-sm text-emerald-100">Última creación: {formatRange(torneo.created_at, null)}</p>}
					{error && <p className="text-sm text-red-300">{error}</p>}
					{success && <p className="text-sm text-emerald-200">{success}</p>}
				</header>

				{loading ? (
					<p className="text-center text-emerald-100">Cargando datos del torneo...</p>
				) : (
					<form
						onSubmit={handleSubmit(onSubmit)}
						className="space-y-6 rounded-2xl border border-white/10 bg-white/5 p-6"
					>
						<div className="grid grid-cols-1 gap-4 md:grid-cols-2">
							<label className="text-sm">
								Nombre
								<input
									type="text"
									{...register('nombre', { required: 'El nombre es obligatorio' })}
									className="mt-2 w-full rounded-lg bg-slate-900/70 px-3 py-2 text-sm"
								/>
								{errors.nombre && <span className="text-xs text-red-300">{errors.nombre.message}</span>}
							</label>

							<label className="text-sm">
								Tipo de deporte
								<input
									type="text"
									{...register('tipo_deporte', { required: 'El deporte es obligatorio' })}
									className="mt-2 w-full rounded-lg bg-slate-900/70 px-3 py-2 text-sm"
								/>
							</label>

							<label className="text-sm">
								Fecha de inicio
								<input
									type="date"
									min={todayISO}
									{...register('fecha_inicio', {
										required: 'La fecha de inicio es obligatoria',
										validate: {
											notPast: (value) => !value || value >= todayISO || 'No puedes seleccionar una fecha anterior a hoy',
										},
									})}
									className="mt-2 w-full rounded-lg bg-slate-900/70 px-3 py-2 text-sm"
								/>
								{errors.fecha_inicio && <span className="text-xs text-red-300">{errors.fecha_inicio.message}</span>}
							</label>

							<label className="text-sm">
								Fecha de fin
								<input
									type="date"
									min={minFechaFin}
									{...register('fecha_fin', {
										required: 'La fecha de fin es obligatoria',
										validate: {
											notPast: (value) => !value || value >= todayISO || 'No puedes seleccionar una fecha anterior a hoy',
											afterStart: (value) => {
												if (!value || !fechaInicioValue) return true;
												return value >= fechaInicioValue || 'La fecha fin no puede ser anterior a la fecha inicio';
											},
										},
									})}
									className="mt-2 w-full rounded-lg bg-slate-900/70 px-3 py-2 text-sm"
								/>
								{errors.fecha_fin && <span className="text-xs text-red-300">{errors.fecha_fin.message}</span>}
							</label>

							<label className="text-sm">
								Costo de inscripción
								<input
									type="number"
									step="0.01"
									min={0}
									{...register('costo_inscripcion', { valueAsNumber: true })}
									className="mt-2 w-full rounded-lg bg-slate-900/70 px-3 py-2 text-sm"
								/>
							</label>

							<label className="text-sm">
								Cupos
								<input
									type="number"
									min={0}
									{...register('cupos', {
										valueAsNumber: true,
										validate: {
											suficienteParaEquipos: (value) => {
												if (value == null || Number.isNaN(value)) return true;
												return value >= selectedEquipos.length || 'No puede ser menor a los equipos seleccionados';
											},
										},
									})}
									className="mt-2 w-full rounded-lg bg-slate-900/70 px-3 py-2 text-sm"
								/>
								{errors.cupos && <span className="text-xs text-red-300">{errors.cupos.message}</span>}
								{cuposRestantes != null && (
									<p className="text-xs text-emerald-100">Cupos restantes: {cuposRestantes}</p>
								)}
							</label>

							<label className="text-sm md:col-span-2">
								Reglas
								<textarea
									{...register('reglas')}
									rows={3}
									className="mt-2 w-full rounded-lg bg-slate-900/70 px-3 py-2 text-sm"
								/>
							</label>

							<label className="text-sm">
								Estado
								<select {...register('estado')} className="mt-2 w-full rounded-lg bg-slate-900/70 px-3 py-2 text-sm">
									{estadoKeys.map((estado) => (
										<option key={estado} value={estado}>
											{estadoLabels[estado]}
										</option>
									))}
								</select>
							</label>
						</div>

						<section className="space-y-4 rounded-2xl border border-white/10 bg-slate-900/50 p-4">
							<div className="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
								<div>
									<h2 className="text-lg font-semibold">Turnos bloqueados</h2>
									<p className="text-sm text-emerald-100">
										Selecciona los turnos que debe retener este torneo ({selectedTurnos.length} seleccionados)
									</p>
								</div>
								<div className="flex flex-col gap-2 md:flex-row">
									<select
										value={canchaFiltro}
										onChange={(e) =>
											setCanchaFiltro(e.target.value === 'todos' ? 'todos' : Number(e.target.value))
										}
										className="rounded-lg bg-slate-800 px-3 py-2 text-sm"
									>
										<option value="todos">Todas las canchas</option>
										{canchas.map((c) => (
											<option key={c.id} value={c.id}>
												{c.nombre}
											</option>
										))}
									</select>
									<input
										type="text"
										value={search}
										onChange={(e) => setSearch(e.target.value)}
										placeholder="Buscar turno"
										className="rounded-lg bg-slate-800 px-3 py-2 text-sm"
									/>
								</div>
							</div>
							<div className="max-h-72 overflow-y-auto rounded-xl border border-white/5">
								{turnosMostrables.length === 0 ? (
									<p className="p-4 text-sm text-emerald-100">No hay turnos disponibles con los filtros seleccionados.</p>
								) : (
									<ul className="divide-y divide-white/5">
										{turnosMostrables.map((turno) => (
											<li key={turno.id}>
												<label className="flex items-start gap-4 p-4 hover:bg-white/5">
													<input
														type="checkbox"
														className="mt-1 size-4"
														checked={selectedTurnos.includes(turno.id!)}
														onChange={() => toggleTurno(turno.id!)}
													/>
													<div>
														<p className="font-semibold">
															{canchaMap.get(turno.id_cancha)?.nombre ?? `Cancha ${turno.id_cancha}`}
														</p>
														<p className="text-sm text-emerald-100">
															{formatRange(turno.fecha_hora_inicio, turno.fecha_hora_fin)}
														</p>
													</div>
												</label>
											</li>
										))}
									</ul>
								)}
							</div>
						</section>

						<section className="space-y-4 rounded-2xl border border-white/10 bg-slate-900/50 p-4">
							<div className="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
								<div>
									<h2 className="text-lg font-semibold">Equipos participantes</h2>
									<p className="text-sm text-emerald-100">
										Selecciona qué equipos ocupan los cupos ({selectedEquipos.length}
										{capacidadMaxima != null ? ` / ${capacidadMaxima}` : ''})
									</p>
									{cuposRestantes != null && (
										<p className="text-xs text-emerald-100">Quedan {cuposRestantes} cupos libres</p>
									)}
									{equipoFeedback && <p className="text-xs text-red-300">{equipoFeedback}</p>}
									{equiposError && <p className="text-xs text-red-300">{equiposError}</p>}
								</div>
								<div className="flex flex-col gap-2 md:flex-row">
									<input
										type="search"
										value={equipoSearch}
										onChange={(e) => setEquipoSearch(e.target.value)}
										placeholder="Buscar equipo"
										className="rounded-lg bg-slate-800 px-3 py-2 text-sm"
									/>
								</div>
							</div>
							<div className="max-h-64 overflow-y-auto rounded-xl border border-white/5">
								{equiposLoading ? (
									<p className="p-4 text-sm text-emerald-100">Cargando equipos...</p>
								) : equiposFiltrados.length === 0 ? (
									<p className="p-4 text-sm text-emerald-100">No hay equipos que coincidan con tu búsqueda.</p>
								) : (
									<ul className="divide-y divide-white/5">
										{equiposFiltrados.map((equipo) => (
											<li key={equipo.id}>
												<label className="flex items-center gap-4 p-4 hover:bg-white/5">
													<input
														type="checkbox"
														className="size-4"
														checked={equipo.id ? selectedEquipos.includes(equipo.id) : false}
														onChange={() => equipo.id && toggleEquipo(equipo.id)}
													/>
													<div>
														<p className="font-semibold">{equipo.nombre_equipo}</p>
														<p className="text-xs text-emerald-100">ID #{equipo.id}</p>
													</div>
												</label>
											</li>
										))}
									</ul>
								)}
							</div>
							{selectedEquipos.length > 0 && (
								<div className="flex flex-wrap gap-2 text-xs text-emerald-100">
									{selectedEquipos.map((equipoId) => (
										<span key={equipoId} className="rounded-full border border-white/20 px-3 py-1">
											{equiposMap.get(equipoId)?.nombre_equipo ?? `Equipo ${equipoId}`}
										</span>
									))}
								</div>
							)}
						</section>

						<div className="flex flex-wrap gap-3">
							<button
								type="submit"
								disabled={isSubmitting}
								className="rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400 disabled:opacity-70"
							>
								{isSubmitting ? 'Guardando...' : 'Guardar cambios'}
							</button>
							<button
								type="button"
								onClick={() => navigate('/torneos/ConsultarTorneos')}
								className="rounded-lg border border-white/20 px-4 py-2 text-sm text-emerald-100 hover:border-emerald-400"
							>
								Cancelar
							</button>
							<Link
								to="/torneos/ConsultarTorneos"
								className="rounded-lg border border-white/20 px-4 py-2 text-sm text-emerald-100 hover:border-emerald-400"
							>
								Volver al listado
							</Link>
						</div>
					</form>
				)}
			</div>
		</div>
	);
}
