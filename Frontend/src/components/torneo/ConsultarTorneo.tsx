import { useEffect, useMemo, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import torneosApi, { type Torneo, getTorneoIdFromMotivo } from '../../services/torneo.service';
import turnosApi, { type Turno } from '../../services/turnos.service';
import equipoTorneoApi from '../../services/equipoTorneo.service';

const estados = ['planificado', 'inscripciones_abiertas', 'en_curso', 'finalizado', 'cancelado'];

const formatDate = (value?: string | null) => {
	if (!value) return '-';
	try {
		return new Intl.DateTimeFormat('es-AR', { dateStyle: 'medium' }).format(new Date(value));
	} catch {
		return value;
	}
};

export default function ConsultarTorneo() {
	const navigate = useNavigate();
	const [torneos, setTorneos] = useState<Torneo[]>([]);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState('');
	const [search, setSearch] = useState('');
	const [estadoFiltro, setEstadoFiltro] = useState<'todos' | string>('todos');
	const [actionId, setActionId] = useState<number | null>(null);
	const [equiposCount, setEquiposCount] = useState<Record<number, number>>({});

	const fetchTorneos = async () => {
		setLoading(true);
		setError('');
		try {
			const data = await torneosApi.list();
			setTorneos(data);
			
			// Cargar cantidad de equipos inscritos para cada torneo
			const counts: Record<number, number> = {};
			await Promise.all(
				data.map(async (torneo) => {
					if (torneo.id) {
						try {
							const count = await equipoTorneoApi.contarEquiposTorneo(torneo.id);
							counts[torneo.id] = count;
						} catch {
							counts[torneo.id] = 0;
						}
					}
				})
			);
			setEquiposCount(counts);
		} catch (err) {
			console.error(err);
			setError('No se pudieron cargar los torneos.');
		} finally {
			setLoading(false);
		}
	};

	useEffect(() => {
		void fetchTorneos();
	}, []);

	const filtered = useMemo(() => {
		const term = search.trim().toLowerCase();
		return torneos.filter((torneo) => {
			const matchName = torneo.nombre.toLowerCase().includes(term);
			const matchEstado = estadoFiltro === 'todos' ? true : torneo.estado === estadoFiltro;
			return matchName && matchEstado;
		});
	}, [torneos, search, estadoFiltro]);

	const resumenPorEstado = useMemo(() => {
		return estados.reduce<Record<string, number>>((acc, estado) => {
			acc[estado] = torneos.filter((t) => t.estado === estado).length;
			return acc;
		}, {});
	}, [torneos]);

	const handleDelete = async (torneo: Torneo) => {
		if (!torneo.id) return;
		const confirmed = window.confirm('Esto eliminará el torneo y liberará sus turnos bloqueados. ¿Continuar?');
		if (!confirmed) return;
		setActionId(torneo.id);
		try {
			const bloqueados = await turnosApi.listByEstado('bloqueado');
			const relacionados = bloqueados
				.filter((turno: Turno) => getTorneoIdFromMotivo(turno.motivo_bloqueo) === torneo.id)
				.map((t) => t.id!)
				.filter(Boolean);

			if (relacionados.length) {
				await torneosApi.releaseTurnosFromTorneo(relacionados);
			}
			await torneosApi.remove(torneo.id);
			setTorneos((prev) => prev.filter((item) => item.id !== torneo.id));
		} catch (err) {
			console.error(err);
			setError('No se pudo eliminar el torneo.');
		} finally {
			setActionId(null);
		}
	};

	return (
		<div className="min-h-screen bg-slate-950 text-white px-4 py-10">
			<div className="max-w-6xl mx-auto space-y-6">
				<header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
					<div>
						<p className="text-sm uppercase tracking-widest text-emerald-200">Torneos</p>
						<h1 className="text-3xl font-bold">Panel de torneos</h1>
						{error && <p className="text-sm text-red-300 mt-2">{error}</p>}
					</div>
					<div className="flex gap-3">
						<button
							onClick={() => navigate('/')}
							className="min-w-[10rem] rounded-lg bg-white/10 px-4 py-2 text-sm font-semibold text-emerald-100 hover:bg-white/20"
						>
							Volver
						</button>
						<button
							onClick={fetchTorneos}
							className="min-w-[10rem] rounded-lg bg-white/10 px-4 py-2 text-sm font-semibold text-emerald-100 hover:bg-white/20 disabled:opacity-60"
							disabled={loading}
						>
							{loading ? 'Actualizando...' : 'Refrescar'}
						</button>
						<button
							onClick={() => navigate('/torneos/RegistrarTorneo')}
							className="min-w-[10rem] rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400"
						>
							Registrar torneo
						</button>
					</div>
				</header>

				<section className="grid grid-cols-2 gap-4 md:grid-cols-5">
					{estados.map((estado) => (
						<article key={estado} className="rounded-2xl border border-white/10 bg-white/5 p-3">
							<p className="text-xs uppercase tracking-wide text-emerald-200">{estado}</p>
							<p className="text-2xl font-bold">{resumenPorEstado[estado] ?? 0}</p>
						</article>
					))}
				</section>

				<section className="bg-white/10 backdrop-blur-md rounded-2xl p-4 shadow-lg border border-white/10">
					<div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
						<label className="text-sm text-emerald-100">
							Buscar por nombre
							<input
								type="search"
								value={search}
								onChange={(e) => setSearch(e.target.value)}
								placeholder="Buscar..."
								className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
							/>
						</label>
						<label className="text-sm text-emerald-100">
							Filtrar por estado
							<select
								value={estadoFiltro}
								onChange={(e) => setEstadoFiltro(e.target.value as typeof estadoFiltro)}
								className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
							>
								<option value="todos" className="bg-slate-900">Todos los estados</option>
								{estados.map((estado) => (
									<option key={estado} value={estado} className="bg-slate-900">
										{estado}
									</option>
								))}
							</select>
						</label>
					</div>

					<div className="max-h-[65vh] overflow-y-auto rounded-2xl border border-white/5">
						<table className="min-w-full text-left text-sm">
							<thead className="sticky top-0 bg-slate-900/80 text-xs uppercase tracking-wide text-emerald-200">
								<tr>
									<th className="px-4 py-3">Nombre</th>
									<th className="px-4 py-3">Deporte</th>
									<th className="px-4 py-3">Período</th>
									<th className="px-4 py-3">Cupos</th>
									<th className="px-4 py-3">Estado</th>
									<th className="px-4 py-3">Acciones</th>
								</tr>
							</thead>
							<tbody>
								{loading ? (
									<tr>
										<td colSpan={6} className="px-4 py-6 text-center text-emerald-100">
											Cargando torneos...
										</td>
									</tr>
								) : filtered.length === 0 ? (
									<tr>
										<td colSpan={6} className="px-4 py-6 text-center text-emerald-100">
											No se encontraron torneos con los filtros seleccionados.
										</td>
									</tr>
								) : (
									filtered.map((torneo) => (
										<tr key={torneo.id} className="border-t border-white/5 hover:bg-white/5">
											<td className="px-4 py-3 text-sm font-semibold">{torneo.nombre}</td>
											<td className="px-4 py-3 text-sm text-emerald-100">{torneo.tipo_deporte}</td>
											<td className="px-4 py-3 text-xs text-emerald-100">
												<span>{formatDate(torneo.fecha_inicio)}</span>
												<span className="mx-1">→</span>
												<span>{formatDate(torneo.fecha_fin)}</span>
											</td>
											<td className="px-4 py-3 text-sm">
												{torneo.cupos != null 
													? `${Math.max(0, torneo.cupos - (equiposCount[torneo.id!] ?? 0))} / ${torneo.cupos}`
													: '-'
												}
											</td>
											<td className="px-4 py-3">
												<span className="rounded-full bg-white/10 px-3 py-1 text-xs capitalize text-emerald-200">
													{torneo.estado ?? 'sin estado'}
												</span>
											</td>
											<td className="px-4 py-3">
												<div className="flex flex-wrap gap-2 text-xs">
													<button
														onClick={() => navigate(`/torneos/ModificarTorneo/${torneo.id}`)}
														className="rounded-lg bg-white/10 px-3 py-1 text-xs font-semibold text-emerald-100 hover:bg-white/20"
													>
														Editar
													</button>
													<button
														onClick={() => handleDelete(torneo)}
														disabled={actionId === torneo.id}
														className="rounded-lg bg-red-500/80 px-3 py-1 text-xs font-semibold text-white hover:bg-red-500 disabled:opacity-60"
													>
														{actionId === torneo.id ? 'Eliminando...' : 'Eliminar'}
													</button>
												</div>
											</td>
										</tr>
									))
								)}
							</tbody>
						</table>
					</div>
				</section>
			</div>
		</div>
	);
}
