import { useEffect, useMemo, useState } from 'react';
import { useForm } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import torneosApi from '../../services/torneo.service';
import turnosApi from '../../services/turnos.service';
import type { Turno, CanchaRef } from '../../services/turnos.service';
import equiposService, { type Equipo } from '../../services/equipos.service';
import inscripcionesApi from '../../services/inscripciones.service';

type FormValues = {
	nombre: string;
	tipo_deporte: string;
	fecha_inicio?: string;
	fecha_fin?: string;
	costo_inscripcion?: number;
	cupos?: number;
	reglas?: string;
	estado?: string;
};

const deportes = ['Fútbol', 'Básquet', 'Pádel', 'Hockey'];
const estados = ['planificado', 'inscripciones_abiertas', 'en_curso', 'finalizado', 'cancelado'];

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

export default function RegistrarTorneo() {
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
		watch,
	} = useForm<FormValues>({
		defaultValues: {
			tipo_deporte: deportes[0],
			estado: estados[0],
			costo_inscripcion: 0,
		},
	});

	const fechaInicioValue = watch('fecha_inicio');
	const cuposValue = watch('cupos');
	const minFechaFin = fechaInicioValue && fechaInicioValue > todayISO ? fechaInicioValue : todayISO;

	const [error, setError] = useState('');
	const [success, setSuccess] = useState('');
	const [turnos, setTurnos] = useState<Turno[]>([]);
	const [canchas, setCanchas] = useState<CanchaRef[]>([]);
	const [turnosLoading, setTurnosLoading] = useState(true);
	const [selectedTurnos, setSelectedTurnos] = useState<number[]>([]);
	const [canchaFiltro, setCanchaFiltro] = useState<number | 'todos'>('todos');
	const [search, setSearch] = useState('');
	const [equipos, setEquipos] = useState<Equipo[]>([]);
	const [equiposLoading, setEquiposLoading] = useState(true);
	const [equiposError, setEquiposError] = useState('');
	const [equipoSearch, setEquipoSearch] = useState('');
	const [selectedEquipos, setSelectedEquipos] = useState<number[]>([]);
	const [equipoFeedback, setEquipoFeedback] = useState('');

	useEffect(() => {
		const loadRefs = async () => {
			setTurnosLoading(true);
			setEquiposLoading(true);
			try {
				const [turnosList, canchasList, equiposList] = await Promise.all([
					turnosApi.list(),
					turnosApi.listCanchas(),
					equiposService.getAllEquipos(),
				]);
				setTurnos(turnosList);
				setCanchas(canchasList);
				setEquipos(equiposList);
			} catch (err) {
				console.error(err);
				setError('No se pudieron cargar los turnos disponibles.');
				setEquiposError('No pudimos cargar la lista de equipos, intenta refrescar.');
			} finally {
				setTurnosLoading(false);
				setEquiposLoading(false);
			}
		};
		void loadRefs();
	}, []);

	const canchaMap = useMemo(() => {
		const map = new Map<number, CanchaRef>();
		canchas.forEach((c) => map.set(c.id, c));
		return map;
	}, [canchas]);

	const turnosDisponibles = useMemo(() => {
		return turnos.filter((t) => t.estado === 'disponible');
	}, [turnos]);

	const turnosFiltrados = useMemo(() => {
		const term = search.trim().toLowerCase();
		return turnosDisponibles.filter((t) => {
			const cancha = canchaMap.get(t.id_cancha);
			const coincideCancha = canchaFiltro === 'todos' ? true : t.id_cancha === canchaFiltro;
			const texto = `${cancha?.nombre ?? ''} ${formatDateRange(t.fecha_hora_inicio, t.fecha_hora_fin)}`.toLowerCase();
			const coincideSearch = term ? texto.includes(term) : true;
			return coincideCancha && coincideSearch;
		});
	}, [turnosDisponibles, canchaFiltro, search, canchaMap]);

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
		setError('');
		setSuccess('');
		try {
			const capacidadDeclarada =
				typeof values.cupos === 'number' && Number.isFinite(values.cupos) ? values.cupos : null;
			if (capacidadDeclarada != null && selectedEquipos.length > capacidadDeclarada) {
				setError('Seleccionaste más equipos de los cupos disponibles.');
				return;
			}
			const payload = {
				nombre: values.nombre.trim(),
				tipo_deporte: values.tipo_deporte,
				fecha_inicio: values.fecha_inicio || null,
				fecha_fin: values.fecha_fin || null,
				costo_inscripcion: values.costo_inscripcion ? Number(values.costo_inscripcion) : 0,
				cupos: values.cupos ? Number(values.cupos) : null,
				reglas: values.reglas || null,
				estado: values.estado,
			};

			const torneo = await torneosApi.create(payload);
			if (torneo.id && selectedTurnos.length > 0) {
				await torneosApi.assignTurnosToTorneo(torneo.id, selectedTurnos, currentUserId);
			}
			if (torneo.id && selectedEquipos.length > 0) {
				await inscripcionesApi.assignEquiposToTorneo(torneo.id, selectedEquipos);
			}

			setSuccess('Torneo creado correctamente. Redirigiendo...');
			setTimeout(() => navigate('/torneos/ConsultarTorneos'), 800);
		} catch (err) {
			console.error(err);
			setError('No se pudo registrar el torneo. Revisa los datos e intenta nuevamente.');
		}
	};

	return (
		<div className="min-h-screen bg-slate-950 text-white px-4 py-10">
			<div className="max-w-5xl mx-auto space-y-6">
				<header className="space-y-2">
					<p className="text-sm uppercase tracking-widest text-emerald-200">Torneos</p>
					<h1 className="text-3xl font-bold">Registrar torneo</h1>
					{error && <p className="text-red-300 text-sm">{error}</p>}
					{success && <p className="text-emerald-200 text-sm">{success}</p>}
				</header>

				<form
					onSubmit={handleSubmit(onSubmit)}
					className="space-y-6 rounded-2xl bg-white/5 p-6 shadow-2xl border border-white/10"
				>
					<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
						<label className="text-sm">
							Nombre del torneo
							<input
								type="text"
								{...register('nombre', { required: 'El nombre es obligatorio' })}
								className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm"
								placeholder="Ej: Copa Verano"
							/>
							{errors.nombre && <span className="text-xs text-red-300">{errors.nombre.message}</span>}
						</label>

						<label className="text-sm">
							Tipo de deporte
							<select
								{...register('tipo_deporte', { required: 'Selecciona un deporte' })}
								className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm"
							>
								{deportes.map((deporte) => (
									<option key={deporte} value={deporte} className="bg-slate-900">
										{deporte}
									</option>
								))}
							</select>
							{errors.tipo_deporte && <span className="text-xs text-red-300">{errors.tipo_deporte.message}</span>}
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
								className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm"
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
								className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm"
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
								className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm"
								placeholder="0.00"
							/>
						</label>

						<label className="text-sm">
							Cupos disponibles
							<input
								type="number"
								min={0}
								{...register('cupos', {
									valueAsNumber: true,
									validate: {
										notNegative: (value) => (value == null || value >= 0) || 'Debe ser un número positivo',
										suficienteParaEquipos: (value) => {
											if (value == null || Number.isNaN(value)) return true;
											return value >= selectedEquipos.length || 'Los cupos no pueden ser menores a los equipos seleccionados';
										},
									},
								})}
								className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm"
								placeholder="Ej: 16"
							/>
							{errors.cupos && <span className="text-xs text-red-300">{errors.cupos.message}</span>}
							{cuposRestantes != null && (
								<p className="text-xs text-emerald-100">Cupos restantes al ritmo actual: {cuposRestantes}</p>
							)}
						</label>

						<label className="text-sm md:col-span-2">
							Reglas o notas
							<textarea
								{...register('reglas')}
								rows={3}
								className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm"
								placeholder="Describe brevemente el formato, requisitos, etc."
							/>
						</label>

						<label className="text-sm">
							Estado
							<select
								{...register('estado')}
								className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm"
							>
								{estados.map((estado) => (
									<option key={estado} value={estado} className="bg-slate-900">
										{estado}
									</option>
								))}
							</select>
						</label>
					</div>

					<section className="space-y-4 rounded-2xl border border-white/10 bg-slate-900/40 p-4">
						<div className="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
							<div>
								<h2 className="text-lg font-semibold">Turnos a bloquear</h2>
								<p className="text-sm text-emerald-100">
									Selecciona los turnos que quedarán reservados para este torneo. ({selectedTurnos.length}{' '}
									seleccionados)
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
									placeholder="Buscar por cancha u horario"
									className="rounded-lg bg-slate-800 px-3 py-2 text-sm"
								/>
							</div>
						</div>

						<div className="max-h-72 overflow-y-auto rounded-xl border border-white/5 bg-slate-950/60">
							{turnosLoading ? (
								<p className="p-4 text-sm text-emerald-100">Cargando turnos disponibles...</p>
							) : turnosFiltrados.length === 0 ? (
								<p className="p-4 text-sm text-emerald-100">No hay turnos disponibles con los filtros actuales.</p>
							) : (
								<ul className="divide-y divide-white/5">
									{turnosFiltrados.map((turno) => (
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
														{formatDateRange(turno.fecha_hora_inicio, turno.fecha_hora_fin)}
													</p>
												</div>
											</label>
										</li>
									))}
								</ul>
							)}
						</div>
					</section>

					<section className="space-y-4 rounded-2xl border border-white/10 bg-slate-900/40 p-4">
						<div className="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
							<div>
								<h2 className="text-lg font-semibold">Equipos participantes</h2>
								<p className="text-sm text-emerald-100">
									Selecciona qué equipos ocuparán los cupos ({selectedEquipos.length}
									{capacidadMaxima != null ? ` / ${capacidadMaxima}` : ''})
								</p>
								{equipoFeedback && <p className="text-xs text-red-300">{equipoFeedback}</p>}
								{equiposError && <p className="text-xs text-red-300">{equiposError}</p>}
								{cuposRestantes != null && (
									<p className="text-xs text-emerald-100">Quedan {cuposRestantes} cupos libres</p>
								)}
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
						<div className="max-h-64 overflow-y-auto rounded-xl border border-white/5 bg-slate-950/60">
							{equiposLoading ? (
								<p className="p-4 text-sm text-emerald-100">Cargando equipos...</p>
							) : equiposFiltrados.length === 0 ? (
								<p className="p-4 text-sm text-emerald-100">No hay equipos que coincidan con la búsqueda.</p>
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
							className="rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400 disabled:opacity-60"
						>
							{isSubmitting ? 'Guardando...' : 'Registrar torneo'}
						</button>
						<Link
							to="/torneos/ConsultarTorneos"
							className="rounded-lg border border-white/20 px-4 py-2 text-sm text-emerald-100 hover:border-emerald-400"
						>
							Volver
						</Link>
					</div>
				</form>
			</div>
		</div>
	);
}
