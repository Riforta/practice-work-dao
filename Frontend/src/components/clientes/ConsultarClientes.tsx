import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import clientesService, { type Cliente } from '../../services/clientes.service';

export default function ConsultarClientes() {
	const navigate = useNavigate();
	const [clientes, setClientes] = useState<Cliente[]>([]);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState('');
	const [searchTerm, setSearchTerm] = useState('');
	const [deleteId, setDeleteId] = useState<number | null>(null);

	const fetchClientes = async () => {
		setLoading(true);
		setError('');
		try {
			const data = await clientesService.list();
			setClientes(data);
		} catch (err) {
			console.error(err);
			setError('No se pudieron cargar los clientes.');
		} finally {
			setLoading(false);
		}
	};

	useEffect(() => {
		void fetchClientes();
	}, []);

	const clientesFiltrados = clientes.filter((cliente) => {
		if (!searchTerm.trim()) return true;
		const term = searchTerm.toLowerCase();
		const nombreCompleto = `${cliente.nombre} ${cliente.apellido || ''}`.toLowerCase();
		const dni = cliente.dni?.toLowerCase() || '';
		const telefono = cliente.telefono?.toLowerCase() || '';
		const email = cliente.email?.toLowerCase() || '';
		return (
			nombreCompleto.includes(term) ||
			dni.includes(term) ||
			telefono.includes(term) ||
			email.includes(term)
		);
	});

	const handleDelete = async (cliente: Cliente) => {
		if (!cliente.id) return;
		
		const nombreCompleto = `${cliente.nombre} ${cliente.apellido || ''}`.trim();
		const confirmed = window.confirm(
			`¿Estás seguro de eliminar al cliente ${nombreCompleto}?\n\nEsta acción no se puede deshacer y puede fallar si el cliente tiene reservas o pagos asociados.`
		);
		
		if (!confirmed) return;
		
		setDeleteId(cliente.id);
		try {
			await clientesService.remove(cliente.id);
			setClientes((prev) => prev.filter((c) => c.id !== cliente.id));
		} catch (err) {
			console.error(err);
			setError('No se pudo eliminar el cliente. Puede que tenga reservas o pagos asociados.');
		} finally {
			setDeleteId(null);
		}
	};

	return (
		<div className="min-h-screen bg-slate-950 text-white px-4 py-10">
			<div className="max-w-7xl mx-auto space-y-6">
				<header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
					<div>
						<p className="text-sm uppercase tracking-widest text-emerald-200">Clientes</p>
						<h1 className="text-3xl font-bold">Gestión de clientes</h1>
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
							onClick={fetchClientes}
							className="min-w-[10rem] rounded-lg bg-white/10 px-4 py-2 text-sm font-semibold text-emerald-100 hover:bg-white/20 disabled:opacity-60"
							disabled={loading}
						>
							{loading ? 'Actualizando...' : 'Refrescar'}
						</button>
						<button
							onClick={() => navigate('/clientes/registrar')}
							className="min-w-[10rem] rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400"
						>
							Registrar cliente
						</button>
					</div>
				</header>

				<section className="rounded-2xl border border-white/10 bg-white/5 p-4">
					<div className="mb-4">
						<input
							type="search"
							value={searchTerm}
							onChange={(e) => setSearchTerm(e.target.value)}
							placeholder="Buscar por nombre, DNI, teléfono o email..."
							className="w-full rounded-lg bg-slate-900/80 px-4 py-2 text-sm"
						/>
					</div>

					{loading ? (
						<p className="text-center text-emerald-100 py-8">Cargando clientes...</p>
					) : clientesFiltrados.length === 0 ? (
						<p className="text-center text-emerald-100 py-8">
							{searchTerm.trim() ? 'No se encontraron clientes con ese criterio.' : 'No hay clientes registrados.'}
						</p>
					) : (
						<div className="overflow-x-auto">
							<table className="w-full text-sm">
								<thead>
								<tr className="border-b border-white/10">
									<th className="text-left py-3 px-2 font-semibold text-emerald-200">Nombre</th>
									<th className="text-left py-3 px-2 font-semibold text-emerald-200">Apellido</th>
									<th className="text-left py-3 px-2 font-semibold text-emerald-200">DNI</th>
									<th className="text-left py-3 px-2 font-semibold text-emerald-200">Teléfono</th>
									<th className="text-left py-3 px-2 font-semibold text-emerald-200">Email</th>
									<th className="text-center py-3 px-2 font-semibold text-emerald-200">Acciones</th>
								</tr>
								</thead>
								<tbody>
									{clientesFiltrados.map((cliente) => (
										<tr
										key={cliente.id}
										className="border-b border-white/5 hover:bg-white/5 transition-colors"
									>
										<td className="py-3 px-2 font-semibold">{cliente.nombre}</td>
										<td className="py-3 px-2">{cliente.apellido || '-'}</td>
											<td className="py-3 px-2">{cliente.dni || '-'}</td>
											<td className="py-3 px-2">{cliente.telefono || '-'}</td>
											<td className="py-3 px-2 text-xs">
												{cliente.email ? (
													<a
														href={`mailto:${cliente.email}`}
														className="text-emerald-200 hover:underline"
													>
														{cliente.email}
													</a>
												) : (
													'-'
												)}
											</td>
										<td className="py-3 px-2">
											<div className="flex items-center justify-center gap-2">
												<button
													onClick={() => navigate(`/clientes/modificar/${cliente.id}`)}
													className="rounded-lg bg-emerald-500/20 px-3 py-1 text-xs font-semibold text-emerald-200 hover:bg-emerald-500/30"
												>
													Editar
												</button>
												<button
													onClick={() => handleDelete(cliente)}
													disabled={deleteId === cliente.id}
													className="rounded-lg bg-red-500/20 px-3 py-1 text-xs font-semibold text-red-200 hover:bg-red-500/30 disabled:opacity-50"
												>
													{deleteId === cliente.id ? 'Eliminando...' : 'Eliminar'}
												</button>
											</div>
										</td>
										</tr>
									))}
								</tbody>
							</table>
						</div>
					)}
				</section>

				<div className="rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-4">
					<p className="text-sm text-emerald-200">
						<span className="font-semibold">Total de clientes:</span> {clientesFiltrados.length}
						{searchTerm.trim() && clientes.length !== clientesFiltrados.length && (
							<span className="ml-2 text-emerald-100/70">
								(filtrados de {clientes.length})
							</span>
						)}
					</p>
				</div>
			</div>
		</div>
	);
}
