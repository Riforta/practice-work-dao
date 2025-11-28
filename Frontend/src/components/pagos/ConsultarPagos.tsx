import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import pagosService, { type Pago } from '../../services/pagos.service';
import clientesService, { type Cliente } from '../../services/clientes.service';

const formatDate = (value?: string | null) => {
	if (!value) return '-';
	try {
		return new Intl.DateTimeFormat('es-AR', { 
			dateStyle: 'short',
			timeStyle: 'short' 
		}).format(new Date(value));
	} catch {
		return value;
	}
};

const formatCurrency = (value: number) => {
	return new Intl.NumberFormat('es-AR', {
		style: 'currency',
		currency: 'ARS'
	}).format(value);
};

const estadoColors: Record<string, string> = {
	iniciado: 'bg-blue-500/20 text-blue-200',
	completado: 'bg-green-500/20 text-green-200',
	fallido: 'bg-red-500/20 text-red-200',
};

export default function ConsultarPagos() {
	const navigate = useNavigate();
	const [pagos, setPagos] = useState<Pago[]>([]);
	const [clientes, setClientes] = useState<Record<number, Cliente>>({});
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState('');
	const [estadoFiltro, setEstadoFiltro] = useState<'todos' | string>('todos');
	const [actionId, setActionId] = useState<number | null>(null);

	const fetchPagos = async () => {
		setLoading(true);
		setError('');
		try {
			const data = await pagosService.listarTodos();
			setPagos(data);
			
			// Cargar información de clientes
			const clientesMap: Record<number, Cliente> = {};
			const uniqueClienteIds = [...new Set(data.map(p => p.id_cliente).filter(Boolean))];
			
			await Promise.all(
				uniqueClienteIds.map(async (id) => {
					try {
						const cliente = await clientesService.getById(id);
						clientesMap[id] = cliente;
					} catch {
						// Ignorar errores de clientes no encontrados
					}
				})
			);
			setClientes(clientesMap);
		} catch (err) {
			console.error(err);
			setError('No se pudieron cargar los pagos.');
		} finally {
			setLoading(false);
		}
	};

	useEffect(() => {
		void fetchPagos();
	}, []);

	const filtered = useMemo(() => {
		return pagos.filter((pago) => {
			const matchEstado = estadoFiltro === 'todos' ? true : pago.estado === estadoFiltro;
			return matchEstado;
		});
	}, [pagos, estadoFiltro]);

	const resumenPorEstado = useMemo(() => {
		const estados = ['iniciado', 'completado', 'fallido'];
		return estados.reduce<Record<string, number>>((acc, estado) => {
			acc[estado] = pagos.filter((p) => p.estado === estado).length;
			return acc;
		}, {});
	}, [pagos]);

	const handleDelete = async (pago: Pago) => {
		if (!pago.id) return;
		const confirmed = window.confirm('¿Estás seguro de eliminar este pago? Esta acción no se puede deshacer.');
		if (!confirmed) return;
		setActionId(pago.id);
		try {
			await pagosService.eliminar(pago.id);
			setPagos((prev) => prev.filter((item) => item.id !== pago.id));
		} catch (err) {
			console.error(err);
			setError('No se pudo eliminar el pago.');
		} finally {
			setActionId(null);
		}
	};

	const handleConfirmar = async (pago: Pago) => {
		if (!pago.id) return;
		const confirmed = window.confirm('¿Confirmar este pago?');
		if (!confirmed) return;
		setActionId(pago.id);
		try {
			await pagosService.confirmarPago(pago.id);
			await fetchPagos();
		} catch (err) {
			console.error(err);
			setError('No se pudo confirmar el pago.');
		} finally {
			setActionId(null);
		}
	};

	return (
		<div className="min-h-screen bg-slate-950 text-white px-4 py-10">
			<div className="max-w-7xl mx-auto space-y-6">
				<header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
					<div>
						<p className="text-sm uppercase tracking-widest text-emerald-200">Pagos</p>
						<h1 className="text-3xl font-bold">Gestión de pagos</h1>
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
							onClick={fetchPagos}
							className="min-w-[10rem] rounded-lg bg-white/10 px-4 py-2 text-sm font-semibold text-emerald-100 hover:bg-white/20 disabled:opacity-60"
							disabled={loading}
						>
							{loading ? 'Actualizando...' : 'Refrescar'}
						</button>
						<button
							onClick={() => navigate('/pagos/registrar')}
							className="min-w-[10rem] rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400"
						>
							Registrar pago
						</button>
					</div>
				</header>

				<section className="grid grid-cols-2 gap-4 md:grid-cols-5">
					{Object.entries(resumenPorEstado).map(([estado, count]) => (
						<article key={estado} className="rounded-2xl border border-white/10 bg-white/5 p-3">
							<p className="text-xs uppercase tracking-wide text-emerald-200">{estado}</p>
							<p className="text-2xl font-bold">{count}</p>
						</article>
					))}
				</section>

				<section className="bg-white/10 backdrop-blur-md rounded-2xl p-4 shadow-lg border border-white/10">
					<div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-4">
						<label className="text-sm text-emerald-100">
							Filtrar por estado
							<select
								value={estadoFiltro}
								onChange={(e) => setEstadoFiltro(e.target.value)}
								className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
							>
						<option value="todos" className="bg-slate-900">Todos los estados</option>
						<option value="iniciado" className="bg-slate-900">Iniciado</option>
						<option value="completado" className="bg-slate-900">Completado</option>
						<option value="fallido" className="bg-slate-900">Fallido</option>
							</select>
						</label>
					</div>

					<div className="max-h-[65vh] overflow-y-auto rounded-2xl border border-white/5">
						<table className="min-w-full text-left text-sm">
							<thead className="sticky top-0 bg-slate-900/80 text-xs uppercase tracking-wide text-emerald-200">
								<tr>
									<th className="px-4 py-3">ID</th>
									<th className="px-4 py-3">Cliente</th>
									<th className="px-4 py-3">Turno</th>
									<th className="px-4 py-3">Monto Total</th>
									<th className="px-4 py-3">Método</th>
									<th className="px-4 py-3">Estado</th>
									<th className="px-4 py-3">Fecha</th>
									<th className="px-4 py-3">Acciones</th>
								</tr>
							</thead>
							<tbody>
								{loading ? (
									<tr>
										<td colSpan={8} className="px-4 py-6 text-center text-emerald-100">
											Cargando pagos...
										</td>
									</tr>
								) : filtered.length === 0 ? (
									<tr>
										<td colSpan={8} className="px-4 py-6 text-center text-emerald-100">
											No se encontraron pagos.
										</td>
									</tr>
								) : (
									filtered.map((pago) => {
										const cliente = pago.id_cliente ? clientes[pago.id_cliente] : null;
										return (
											<tr key={pago.id} className="border-t border-white/5 hover:bg-white/5">
												<td className="px-4 py-3 text-sm font-semibold">#{pago.id}</td>
												<td className="px-4 py-3 text-sm">
													{cliente 
														? `${cliente.nombre} ${cliente.apellido || ''}`
														: `Cliente ${pago.id_cliente}`
													}
												</td>
												<td className="px-4 py-3 text-sm text-emerald-100">
													{pago.id_turno ? `Turno #${pago.id_turno}` : '-'}
												</td>
												<td className="px-4 py-3 text-sm font-semibold">
													{formatCurrency(pago.monto_total)}
												</td>
												<td className="px-4 py-3 text-xs capitalize">
													{pago.metodo_pago || '-'}
												</td>
												<td className="px-4 py-3">
													<span className={`rounded-full px-3 py-1 text-xs capitalize ${estadoColors[pago.estado] || 'bg-gray-500/20 text-gray-200'}`}>
														{pago.estado}
													</span>
												</td>
												<td className="px-4 py-3 text-xs text-emerald-100">
													{formatDate(pago.fecha_creacion)}
												</td>
												<td className="px-4 py-3">
													<div className="flex flex-wrap gap-2 text-xs">
														{pago.estado === 'iniciado' && (
															<button
																onClick={() => handleConfirmar(pago)}
																disabled={actionId === pago.id}
																className="rounded-lg bg-green-500/80 px-3 py-1 text-xs font-semibold text-white hover:bg-green-500 disabled:opacity-60"
															>
																{actionId === pago.id ? 'Confirmando...' : 'Confirmar'}
															</button>
														)}
														<button
															onClick={() => handleDelete(pago)}
															disabled={actionId === pago.id}
															className="rounded-lg bg-red-500/80 px-3 py-1 text-xs font-semibold text-white hover:bg-red-500 disabled:opacity-60"
														>
															{actionId === pago.id ? 'Eliminando...' : 'Eliminar'}
														</button>
													</div>
												</td>
											</tr>
										);
									})
								)}
							</tbody>
						</table>
					</div>
				</section>
			</div>
		</div>
	);
}
