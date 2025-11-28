import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import reportesService, {
	type ResumenGeneral,
	type ReservaPorCliente,
	type ReservaPorCancha,
	type CanchaMasUtilizada,
	type UtilizacionMensual,
} from '../../services/reportes.service';
import clientesService, { type Cliente } from '../../services/clientes.service';
import turnosService, { type CanchaRef } from '../../services/turnos.service';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import {
	BarChart,
	Bar,
	XAxis,
	YAxis,
	CartesianGrid,
	Tooltip,
	Legend,
	ResponsiveContainer,
	LineChart,
	Line,
	PieChart,
	Pie,
	Cell,
} from 'recharts';

const COLORS = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

const formatCurrency = (value: number) => {
	return new Intl.NumberFormat('es-AR', {
		style: 'currency',
		currency: 'ARS',
	}).format(value);
};

const formatDate = (value?: string | null) => {
	if (!value) return '-';
	try {
		return new Intl.DateTimeFormat('es-AR', {
			dateStyle: 'short',
			timeStyle: 'short',
		}).format(new Date(value));
	} catch {
		return value;
	}
};

type TipoReporte = 'resumen' | 'reservas-cliente' | 'reservas-cancha' | 'canchas-utilizadas' | 'utilizacion-mensual';

export default function Reportes() {
	const navigate = useNavigate();
	const reporteRef = useRef<HTMLDivElement>(null);

	const [tipoReporte, setTipoReporte] = useState<TipoReporte>('resumen');
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState('');
	const [exportando, setExportando] = useState(false);

	// Datos de reportes
	const [resumen, setResumen] = useState<ResumenGeneral | null>(null);
	const [reservasCliente, setReservasCliente] = useState<ReservaPorCliente[]>([]);
	const [reservasCancha, setReservasCancha] = useState<ReservaPorCancha[]>([]);
	const [canchasUtilizadas, setCanchasUtilizadas] = useState<CanchaMasUtilizada[]>([]);
	const [utilizacionMensual, setUtilizacionMensual] = useState<UtilizacionMensual[]>([]);

	// Filtros
	const [clienteSeleccionado, setClienteSeleccionado] = useState<number | ''>('');
	const [canchaSeleccionada, setCanchaSeleccionada] = useState<number | ''>('');
	const [fechaInicio, setFechaInicio] = useState('');
	const [fechaFin, setFechaFin] = useState('');
	const [anioSeleccionado, setAnioSeleccionado] = useState<number>(new Date().getFullYear());
	const [limiteTop, setLimiteTop] = useState(10);

	// Datos auxiliares
	const [clientes, setClientes] = useState<Cliente[]>([]);
	const [canchas, setCanchas] = useState<CanchaRef[]>([]);

	useEffect(() => {
		const loadData = async () => {
			try {
				const [clientesData, canchasData] = await Promise.all([
					clientesService.list(),
					turnosService.listCanchas(),
				]);
				setClientes(clientesData);
				setCanchas(canchasData);
			} catch (err) {
				console.error(err);
			}
		};
		void loadData();
	}, []);

	const cargarReporte = async () => {
		setLoading(true);
		setError('');
		try {
			switch (tipoReporte) {
				case 'resumen':
					const resumenData = await reportesService.getResumenGeneral();
					setResumen(resumenData);
					break;

				case 'reservas-cliente':
					const reservasClienteData = await reportesService.getReservasPorCliente(
						clienteSeleccionado || undefined
					);
					setReservasCliente(reservasClienteData);
					break;

				case 'reservas-cancha':
					if (!fechaInicio || !fechaFin) {
						setError('Debe seleccionar un rango de fechas');
						return;
					}
					const reservasCanchaData = await reportesService.getReservasPorCancha(
						fechaInicio,
						fechaFin,
						canchaSeleccionada || undefined
					);
					setReservasCancha(reservasCanchaData);
					break;

				case 'canchas-utilizadas':
					const canchasUtilizadasData = await reportesService.getCanchasMasUtilizadas(limiteTop);
					setCanchasUtilizadas(canchasUtilizadasData);
					break;

				case 'utilizacion-mensual':
					const utilizacionMensualData = await reportesService.getUtilizacionMensual(anioSeleccionado);
					setUtilizacionMensual(utilizacionMensualData);
					break;
			}
		} catch (err: any) {
			console.error(err);
			setError(err.response?.data?.detail || 'Error al cargar el reporte');
		} finally {
			setLoading(false);
		}
	};

	const exportarPDF = async () => {
		if (!reporteRef.current) return;

		setExportando(true);
		setError('');
		try {
			// Crear un clon temporal del elemento para modificar estilos
			const clone = reporteRef.current.cloneNode(true) as HTMLElement;
			clone.style.position = 'absolute';
			clone.style.left = '-9999px';
			clone.style.top = '0';
			clone.style.width = reporteRef.current.offsetWidth + 'px';
			document.body.appendChild(clone);

			// Mapeo de colores comunes de Tailwind
			const colorMap: Record<string, string> = {
				'emerald': '#10b981',
				'blue': '#3b82f6',
				'red': '#ef4444',
				'green': '#22c55e',
				'yellow': '#eab308',
				'purple': '#a855f7',
				'pink': '#ec4899',
				'gray': '#6b7280',
				'slate': '#64748b',
			};

			// Función recursiva para convertir colores oklab/oklch a rgb
			const convertOklabColors = (element: HTMLElement) => {
				const computedStyle = window.getComputedStyle(element);
				
				// Convertir color de texto
				if (computedStyle.color && (computedStyle.color.includes('oklab') || computedStyle.color.includes('oklch'))) {
					// Intentar detectar el color por clase
					let newColor = '#ffffff';
					for (const [name, hex] of Object.entries(colorMap)) {
						if (element.className.includes(`text-${name}`)) {
							newColor = hex;
							break;
						}
					}
					element.style.color = newColor;
					element.style.setProperty('color', newColor, 'important');
				}
				
				// Forzar texto blanco si no tiene color específico
				if (!element.style.color || element.style.color === '' || element.style.color === 'inherit') {
					element.style.color = '#ffffff';
					element.style.setProperty('color', '#ffffff', 'important');
				}
				
				// Convertir background
				if (computedStyle.backgroundColor && (computedStyle.backgroundColor.includes('oklab') || computedStyle.backgroundColor.includes('oklch'))) {
					let newBg = 'rgba(255, 255, 255, 0.1)';
					
					// Detectar fondo oscuro principal
					if (element.className.includes('bg-slate-950')) {
						newBg = '#020617';
					} else if (element.className.includes('bg-white/5')) {
						newBg = 'rgba(255, 255, 255, 0.05)';
					} else if (element.className.includes('bg-white/10')) {
						newBg = 'rgba(255, 255, 255, 0.1)';
					} else {
						// Detectar colores temáticos
						for (const [name, hex] of Object.entries(colorMap)) {
							if (element.className.includes(`bg-${name}`)) {
								// Si tiene opacidad
								if (element.className.includes('/20')) {
									newBg = hex + '33'; // 20% opacity
								} else if (element.className.includes('/10')) {
									newBg = hex + '1A'; // 10% opacity
								} else {
									newBg = hex;
								}
								break;
							}
						}
					}
					element.style.backgroundColor = newBg;
				}
				
				// Convertir border
				if (computedStyle.borderColor && (computedStyle.borderColor.includes('oklab') || computedStyle.borderColor.includes('oklch'))) {
					element.style.borderColor = 'rgba(255, 255, 255, 0.1)';
				}

				// Aplicar a todos los hijos
				Array.from(element.children).forEach(child => {
					if (child instanceof HTMLElement) {
						convertOklabColors(child);
					}
				});
			};

			// Convertir colores en el clon
			convertOklabColors(clone);

			const canvas = await html2canvas(clone, {
				scale: 2,
				useCORS: true,
				logging: false,
				backgroundColor: '#020617',
				width: clone.offsetWidth,
				height: clone.offsetHeight,
			});

			// Remover el clon
			document.body.removeChild(clone);

			const imgData = canvas.toDataURL('image/png');
			const pdf = new jsPDF('p', 'mm', 'a4');
			
			const pdfWidth = pdf.internal.pageSize.getWidth();
			const pdfHeight = pdf.internal.pageSize.getHeight();
			
			// Calcular dimensiones con márgenes
			const margin = 10;
			const contentWidth = pdfWidth - (2 * margin);
			
			// Calcular altura proporcional
			const imgRatio = canvas.height / canvas.width;
			const contentHeight = contentWidth * imgRatio;
			
			// Si cabe en una página
			if (contentHeight <= pdfHeight - (2 * margin)) {
				pdf.addImage(imgData, 'PNG', margin, margin, contentWidth, contentHeight);
			} else {
				// Dividir en múltiples páginas
				const pageHeight = pdfHeight - (2 * margin);
				const totalPages = Math.ceil(contentHeight / pageHeight);
				
				for (let page = 0; page < totalPages; page++) {
					if (page > 0) {
						pdf.addPage();
					}
					
					// Calcular qué porción de la imagen mostrar
					const sourceY = (canvas.height / totalPages) * page;
					const sourceHeight = canvas.height / totalPages;
					
					// Crear canvas temporal con la porción
					const tempCanvas = document.createElement('canvas');
					tempCanvas.width = canvas.width;
					tempCanvas.height = sourceHeight;
					const tempCtx = tempCanvas.getContext('2d');
					
					if (tempCtx) {
						tempCtx.drawImage(
							canvas,
							0, sourceY,
							canvas.width, sourceHeight,
							0, 0,
							canvas.width, sourceHeight
						);
						
						const pageImgData = tempCanvas.toDataURL('image/png');
						const pageContentHeight = contentWidth * (sourceHeight / canvas.width);
						pdf.addImage(pageImgData, 'PNG', margin, margin, contentWidth, pageContentHeight);
					}
				}
			}
			
			pdf.save(`reporte-${tipoReporte}-${Date.now()}.pdf`);
		} catch (err) {
			console.error('Error al exportar PDF:', err);
			setError(`Error al exportar el PDF: ${err instanceof Error ? err.message : 'Error desconocido'}`);
		} finally {
			setExportando(false);
		}
	};

	useEffect(() => {
		if (tipoReporte === 'resumen') {
			void cargarReporte();
		}
	}, [tipoReporte]);

	return (
		<div className="min-h-screen bg-slate-950 text-white px-4 py-10">
			<div className="max-w-7xl mx-auto space-y-6">
				<header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
					<div>
						<p className="text-sm uppercase tracking-widest text-emerald-200">Reportes</p>
						<h1 className="text-3xl font-bold">Sistema de Reportes</h1>
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
							onClick={exportarPDF}
							disabled={exportando || loading}
							className="min-w-[10rem] rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400 disabled:opacity-50"
						>
							{exportando ? 'Exportando...' : 'Exportar PDF'}
						</button>
					</div>
				</header>

				<section className="bg-white/10 backdrop-blur-md rounded-2xl p-6 shadow-lg border border-white/10">
					<h2 className="text-xl font-semibold mb-4">Seleccionar Tipo de Reporte</h2>
					<div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
						<button
							onClick={() => setTipoReporte('resumen')}
							className={`p-4 rounded-lg border-2 transition-all ${
								tipoReporte === 'resumen'
									? 'border-emerald-500 bg-emerald-500/20'
									: 'border-white/20 bg-white/5 hover:bg-white/10'
							}`}
						>
							<h3 className="font-semibold">Resumen General</h3>
							<p className="text-sm text-gray-300 mt-1">Métricas principales del sistema</p>
						</button>
						<button
							onClick={() => setTipoReporte('reservas-cliente')}
							className={`p-4 rounded-lg border-2 transition-all ${
								tipoReporte === 'reservas-cliente'
									? 'border-emerald-500 bg-emerald-500/20'
									: 'border-white/20 bg-white/5 hover:bg-white/10'
							}`}
						>
							<h3 className="font-semibold">Reservas por Cliente</h3>
							<p className="text-sm text-gray-300 mt-1">Historial de reservas de clientes</p>
						</button>
						<button
							onClick={() => setTipoReporte('reservas-cancha')}
							className={`p-4 rounded-lg border-2 transition-all ${
								tipoReporte === 'reservas-cancha'
									? 'border-emerald-500 bg-emerald-500/20'
									: 'border-white/20 bg-white/5 hover:bg-white/10'
							}`}
						>
							<h3 className="font-semibold">Reservas por Cancha</h3>
							<p className="text-sm text-gray-300 mt-1">Reservas en un período</p>
						</button>
						<button
							onClick={() => setTipoReporte('canchas-utilizadas')}
							className={`p-4 rounded-lg border-2 transition-all ${
								tipoReporte === 'canchas-utilizadas'
									? 'border-emerald-500 bg-emerald-500/20'
									: 'border-white/20 bg-white/5 hover:bg-white/10'
							}`}
						>
							<h3 className="font-semibold">Canchas Más Utilizadas</h3>
							<p className="text-sm text-gray-300 mt-1">Ranking de canchas</p>
						</button>
						<button
							onClick={() => setTipoReporte('utilizacion-mensual')}
							className={`p-4 rounded-lg border-2 transition-all ${
								tipoReporte === 'utilizacion-mensual'
									? 'border-emerald-500 bg-emerald-500/20'
									: 'border-white/20 bg-white/5 hover:bg-white/10'
							}`}
						>
							<h3 className="font-semibold">Utilización Mensual</h3>
							<p className="text-sm text-gray-300 mt-1">Gráfico estadístico mensual</p>
						</button>
					</div>

					{/* Filtros según tipo de reporte */}
					<div className="space-y-4">
						{tipoReporte === 'reservas-cliente' && (
							<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
								<label className="text-sm">
									Cliente (opcional)
									<select
										value={clienteSeleccionado}
										onChange={(e) => setClienteSeleccionado(e.target.value ? Number(e.target.value) : '')}
										className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
									>
										<option value="">Todos los clientes</option>
										{clientes.map((c) => (
											<option key={c.id} value={c.id}>
												{c.nombre} {c.apellido} - {c.dni}
											</option>
										))}
									</select>
								</label>
							</div>
						)}

						{tipoReporte === 'reservas-cancha' && (
							<div className="grid grid-cols-1 md:grid-cols-3 gap-4">
								<label className="text-sm">
									Fecha Inicio *
									<input
										type="date"
										value={fechaInicio}
										onChange={(e) => setFechaInicio(e.target.value)}
										className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
									/>
								</label>
								<label className="text-sm">
									Fecha Fin *
									<input
										type="date"
										value={fechaFin}
										onChange={(e) => setFechaFin(e.target.value)}
										className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
									/>
								</label>
								<label className="text-sm">
									Cancha (opcional)
									<select
										value={canchaSeleccionada}
										onChange={(e) => setCanchaSeleccionada(e.target.value ? Number(e.target.value) : '')}
										className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
									>
										<option value="">Todas las canchas</option>
										{canchas.map((c) => (
											<option key={c.id} value={c.id}>
												{c.nombre}
											</option>
										))}
									</select>
								</label>
							</div>
						)}

						{tipoReporte === 'canchas-utilizadas' && (
							<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
								<label className="text-sm">
									Cantidad de canchas
									<input
										type="number"
										min="1"
										max="50"
										value={limiteTop}
										onChange={(e) => setLimiteTop(Number(e.target.value))}
										className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
									/>
								</label>
							</div>
						)}

						{tipoReporte === 'utilizacion-mensual' && (
							<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
								<label className="text-sm">
									Año
									<input
										type="number"
										min="2000"
										max="2100"
										value={anioSeleccionado}
										onChange={(e) => setAnioSeleccionado(Number(e.target.value))}
										className="mt-2 w-full rounded-lg bg-slate-900/80 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
									/>
								</label>
							</div>
						)}

						{tipoReporte !== 'resumen' && (
							<button
								onClick={cargarReporte}
								disabled={loading}
								className="w-full md:w-auto min-w-[200px] rounded-lg bg-emerald-500 px-6 py-3 text-sm font-semibold text-slate-950 hover:bg-emerald-400 disabled:opacity-50"
							>
								{loading ? 'Generando...' : 'Generar Reporte'}
							</button>
						)}
					</div>
			</section>

			{/* Área de reporte */}
			<div ref={reporteRef} data-reporte-content className="bg-white/10 backdrop-blur-md rounded-2xl p-6 shadow-lg border border-white/10">
				{loading && (
						<div className="text-center py-12">
							<p className="text-gray-300">Cargando reporte...</p>
						</div>
					)}

					{!loading && tipoReporte === 'resumen' && resumen && (
						<ResumenGeneralView data={resumen} />
					)}

					{!loading && tipoReporte === 'reservas-cliente' && reservasCliente.length > 0 && (
						<ReservasPorClienteView data={reservasCliente} />
					)}

					{!loading && tipoReporte === 'reservas-cancha' && reservasCancha.length > 0 && (
						<ReservasPorCanchaView data={reservasCancha} />
					)}

					{!loading && tipoReporte === 'canchas-utilizadas' && canchasUtilizadas.length > 0 && (
						<CanchasMasUtilizadasView data={canchasUtilizadas} />
					)}

					{!loading && tipoReporte === 'utilizacion-mensual' && utilizacionMensual.length > 0 && (
						<UtilizacionMensualView data={utilizacionMensual} />
					)}

					{!loading &&
						((tipoReporte === 'reservas-cliente' && reservasCliente.length === 0) ||
							(tipoReporte === 'reservas-cancha' && reservasCancha.length === 0) ||
							(tipoReporte === 'canchas-utilizadas' && canchasUtilizadas.length === 0) ||
							(tipoReporte === 'utilizacion-mensual' && utilizacionMensual.length === 0)) && (
							<div className="text-center py-12">
								<p className="text-gray-300">No hay datos para mostrar</p>
							</div>
						)}
				</div>
			</div>
		</div>
	);
}

// Componentes de visualización de cada reporte

function ResumenGeneralView({ data }: { data: ResumenGeneral }) {
	return (
		<div className="space-y-6">
			<h2 className="text-2xl font-bold text-emerald-400">Resumen General del Sistema</h2>
			<div className="grid grid-cols-2 md:grid-cols-3 gap-4">
				<div className="bg-white/5 rounded-lg p-4 border border-white/10">
					<p className="text-xs uppercase text-emerald-200">Total Canchas</p>
					<p className="text-3xl font-bold mt-2">{data.total_canchas}</p>
				</div>
				<div className="bg-white/5 rounded-lg p-4 border border-white/10">
					<p className="text-xs uppercase text-emerald-200">Total Clientes</p>
					<p className="text-3xl font-bold mt-2">{data.total_clientes}</p>
				</div>
				<div className="bg-white/5 rounded-lg p-4 border border-white/10">
					<p className="text-xs uppercase text-emerald-200">Clientes Activos</p>
					<p className="text-3xl font-bold mt-2">{data.clientes_activos}</p>
				</div>
				<div className="bg-white/5 rounded-lg p-4 border border-white/10">
					<p className="text-xs uppercase text-emerald-200">Total Reservas</p>
					<p className="text-3xl font-bold mt-2">{data.total_reservas}</p>
				</div>
				<div className="bg-white/5 rounded-lg p-4 border border-white/10">
					<p className="text-xs uppercase text-emerald-200">Ingresos Totales</p>
					<p className="text-3xl font-bold mt-2">{formatCurrency(data.total_ingresos)}</p>
				</div>
				<div className="bg-white/5 rounded-lg p-4 border border-white/10">
					<p className="text-xs uppercase text-emerald-200">Ingreso Promedio</p>
					<p className="text-3xl font-bold mt-2">{formatCurrency(data.ingreso_promedio_por_reserva)}</p>
				</div>
			</div>
			<p className="text-xs text-gray-400 text-right">
				Generado: {formatDate(data.fecha_generacion)}
			</p>
		</div>
	);
}

function ReservasPorClienteView({ data }: { data: ReservaPorCliente[] }) {
	return (
		<div className="space-y-6">
			<h2 className="text-2xl font-bold text-emerald-400">Reservas por Cliente</h2>
			<p className="text-sm text-gray-300">Total de clientes con reservas: {data.length}</p>
			<div className="space-y-4">
				{data.map((cliente) => (
					<div key={cliente.id_cliente} className="bg-white/5 rounded-lg p-4 border border-white/10">
						<div className="flex justify-between items-start mb-3">
							<div>
								<h3 className="text-lg font-semibold">{cliente.nombre_cliente}</h3>
								<p className="text-sm text-gray-400">
									DNI: {cliente.dni} | Tel: {cliente.telefono}
								</p>
							</div>
							<div className="text-right">
								<span className="bg-emerald-500/20 text-emerald-200 px-3 py-1 rounded-full text-sm block mb-1">
									{cliente.cantidad_reservas} reservas
								</span>
								<p className="text-xs text-gray-400">Total gastado:</p>
								<p className="text-lg font-semibold text-emerald-400">{formatCurrency(cliente.total_gastado)}</p>
								{cliente.total_servicios > 0 && (
									<p className="text-xs text-gray-400">
										(incluye {formatCurrency(cliente.total_servicios)} en servicios)
									</p>
								)}
							</div>
						</div>
						<div className="overflow-x-auto">
							<table className="w-full text-sm">
								<thead className="border-b border-white/10">
									<tr className="text-left text-gray-400">
										<th className="pb-2">Cancha</th>
										<th className="pb-2">Inicio</th>
										<th className="pb-2">Fin</th>
										<th className="pb-2">Turno</th>
										<th className="pb-2">Servicios</th>
										<th className="pb-2">Total</th>
									</tr>
								</thead>
								<tbody>
									{cliente.reservas.slice(0, 5).map((reserva) => (
										<tr key={reserva.id_turno} className="border-b border-white/5">
											<td className="py-2">{reserva.cancha}</td>
											<td className="py-2">{formatDate(reserva.fecha_hora_inicio)}</td>
											<td className="py-2">{formatDate(reserva.fecha_hora_fin)}</td>
											<td className="py-2">{formatCurrency(reserva.precio_final)}</td>
											<td className="py-2">
												{reserva.monto_servicios > 0 ? (
													<span className="text-blue-300">{formatCurrency(reserva.monto_servicios)}</span>
												) : (
													<span className="text-gray-500">-</span>
												)}
											</td>
											<td className="py-2 font-semibold">{formatCurrency(reserva.total)}</td>
										</tr>
									))}
								</tbody>
							</table>
							{cliente.reservas.length > 5 && (
								<p className="text-xs text-gray-400 mt-2">
									Mostrando 5 de {cliente.reservas.length} reservas
								</p>
							)}
						</div>
					</div>
				))}
			</div>
		</div>
	);
}

function ReservasPorCanchaView({ data }: { data: ReservaPorCancha[] }) {
	return (
		<div className="space-y-6">
			<h2 className="text-2xl font-bold text-emerald-400">Reservas por Cancha</h2>
			<p className="text-sm text-gray-300">Total de canchas con reservas: {data.length}</p>
			
			{/* Gráfico de barras */}
			<div className="bg-white/5 rounded-lg p-4 border border-white/10">
				<h3 className="text-lg font-semibold mb-4">Cantidad de Reservas por Cancha</h3>
				<ResponsiveContainer width="100%" height={300}>
					<BarChart data={data}>
						<CartesianGrid strokeDasharray="3 3" stroke="#ffffff20" />
						<XAxis dataKey="nombre_cancha" stroke="#fff" />
						<YAxis stroke="#fff" />
						<Tooltip
							contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #ffffff20' }}
							labelStyle={{ color: '#fff' }}
						/>
						<Legend />
						<Bar dataKey="cantidad_reservas" fill="#10b981" name="Reservas" />
					</BarChart>
				</ResponsiveContainer>
			</div>

			<div className="space-y-4">
				{data.map((cancha) => (
					<div key={cancha.id_cancha} className="bg-white/5 rounded-lg p-4 border border-white/10">
						<div className="flex justify-between items-start mb-3">
							<div>
								<h3 className="text-lg font-semibold">{cancha.nombre_cancha}</h3>
								<p className="text-sm text-gray-400">Tipo: {cancha.tipo_cancha}</p>
							</div>
							<div className="text-right">
								<p className="text-sm text-gray-400">{cancha.cantidad_reservas} reservas</p>
								<p className="text-lg font-semibold text-emerald-400">
									{formatCurrency(cancha.ingresos_totales)}
								</p>
							</div>
						</div>
						<div className="overflow-x-auto">
							<table className="w-full text-sm">
								<thead className="border-b border-white/10">
									<tr className="text-left text-gray-400">
										<th className="pb-2">Cliente</th>
										<th className="pb-2">Inicio</th>
										<th className="pb-2">Fin</th>
										<th className="pb-2">Precio</th>
									</tr>
								</thead>
								<tbody>
									{cancha.reservas.slice(0, 5).map((reserva) => (
										<tr key={reserva.id_turno} className="border-b border-white/5">
											<td className="py-2">{reserva.cliente}</td>
											<td className="py-2">{formatDate(reserva.fecha_hora_inicio)}</td>
											<td className="py-2">{formatDate(reserva.fecha_hora_fin)}</td>
											<td className="py-2">{formatCurrency(reserva.precio_final)}</td>
										</tr>
									))}
								</tbody>
							</table>
							{cancha.reservas.length > 5 && (
								<p className="text-xs text-gray-400 mt-2">
									Mostrando 5 de {cancha.reservas.length} reservas
								</p>
							)}
						</div>
					</div>
				))}
			</div>
		</div>
	);
}

function CanchasMasUtilizadasView({ data }: { data: CanchaMasUtilizada[] }) {
	return (
		<div className="space-y-6">
			<h2 className="text-2xl font-bold text-emerald-400">Canchas Más Utilizadas</h2>
			
			{/* Gráfico de torta */}
			<div className="bg-white/5 rounded-lg p-4 border border-white/10">
				<h3 className="text-lg font-semibold mb-4">Distribución de Reservas</h3>
				<ResponsiveContainer width="100%" height={300}>
					<PieChart>
						<Pie
							data={data as any}
							dataKey="cantidad_reservas"
							nameKey="nombre_cancha"
							cx="50%"
							cy="50%"
							outerRadius={100}
							label
						>
							{data.map((_, index) => (
								<Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
							))}
						</Pie>
						<Tooltip
							contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #ffffff20' }}
							labelStyle={{ color: '#fff' }}
						/>
						<Legend />
					</PieChart>
				</ResponsiveContainer>
			</div>

			<div className="overflow-x-auto">
				<table className="w-full">
					<thead className="border-b border-white/20">
						<tr className="text-left text-gray-400">
								<th className="pb-3">#</th>
								<th className="pb-3">Cancha</th>
								<th className="pb-3">Tipo</th>
								<th className="pb-3">Reservas</th>
								<th className="pb-3">Ingresos</th>
								<th className="pb-3">Precio Prom.</th>
						</tr>
					</thead>
					<tbody>
						{data.map((cancha, index) => (
							<tr key={cancha.id_cancha} className="border-b border-white/10">
								<td className="py-3">
									<span
										className={`inline-flex items-center justify-center w-8 h-8 rounded-full font-bold ${
											index === 0
												? 'bg-yellow-500 text-slate-950'
												: index === 1
												? 'bg-gray-300 text-slate-950'
												: index === 2
												? 'bg-orange-600 text-white'
												: 'bg-white/10 text-white'
										}`}
									>
										{index + 1}
									</span>
								</td>
								<td className="py-3 font-semibold">{cancha.nombre_cancha}</td>
								<td className="py-3">{cancha.tipo_cancha}</td>
								<td className="py-3">
									<span className="bg-emerald-500/20 text-emerald-200 px-2 py-1 rounded text-sm">
										{cancha.cantidad_reservas}
									</span>
								</td>
								<td className="py-3 font-semibold">{formatCurrency(cancha.ingresos_totales)}</td>
								<td className="py-3 text-gray-400">{formatCurrency(cancha.precio_promedio)}</td>
							</tr>
						))}
					</tbody>
				</table>
			</div>
		</div>
	);
}

function UtilizacionMensualView({ data }: { data: UtilizacionMensual[] }) {
	return (
		<div className="space-y-6">
			<h2 className="text-2xl font-bold text-emerald-400">Utilización Mensual de Canchas</h2>
			<p className="text-sm text-gray-300">Año: {data[0]?.anio}</p>

			{/* Gráfico de líneas */}
			<div className="bg-white/5 rounded-lg p-4 border border-white/10">
				<h3 className="text-lg font-semibold mb-4">Reservas por Mes</h3>
				<ResponsiveContainer width="100%" height={300}>
					<LineChart data={data}>
						<CartesianGrid strokeDasharray="3 3" stroke="#ffffff20" />
						<XAxis dataKey="nombre_mes" stroke="#fff" />
						<YAxis stroke="#fff" />
						<Tooltip
							contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #ffffff20' }}
							labelStyle={{ color: '#fff' }}
						/>
						<Legend />
						<Line
							type="monotone"
							dataKey="total_reservas"
							stroke="#10b981"
							strokeWidth={2}
							name="Reservas"
						/>
					</LineChart>
				</ResponsiveContainer>
			</div>

			{/* Gráfico de ingresos */}
			<div className="bg-white/5 rounded-lg p-4 border border-white/10">
				<h3 className="text-lg font-semibold mb-4">Ingresos por Mes</h3>
				<ResponsiveContainer width="100%" height={300}>
					<BarChart data={data}>
						<CartesianGrid strokeDasharray="3 3" stroke="#ffffff20" />
						<XAxis dataKey="nombre_mes" stroke="#fff" />
						<YAxis stroke="#fff" />
						<Tooltip
							contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #ffffff20' }}
							labelStyle={{ color: '#fff' }}
							formatter={(value: number) => formatCurrency(value)}
						/>
						<Legend />
						<Bar dataKey="ingresos_totales" fill="#3b82f6" name="Ingresos" />
					</BarChart>
				</ResponsiveContainer>
			</div>

			<div className="space-y-4">
				{data.filter((mes) => mes.total_reservas > 0).map((mes) => (
					<div key={mes.mes} className="bg-white/5 rounded-lg p-4 border border-white/10">
						<div className="flex justify-between items-center mb-3">
							<h3 className="text-lg font-semibold">{mes.nombre_mes}</h3>
							<div className="text-right">
								<p className="text-sm text-gray-400">{mes.total_reservas} reservas</p>
								<p className="text-lg font-semibold text-emerald-400">
									{formatCurrency(mes.ingresos_totales)}
								</p>
							</div>
						</div>
						{mes.canchas.length > 0 && (
							<div className="grid grid-cols-2 md:grid-cols-4 gap-2">
								{mes.canchas.map((cancha) => (
									<div key={cancha.id_cancha} className="bg-white/5 rounded p-2 text-sm">
										<p className="font-medium truncate">{cancha.nombre_cancha}</p>
										<p className="text-xs text-gray-400">{cancha.cantidad_reservas} reservas</p>
										<p className="text-xs text-emerald-400">{formatCurrency(cancha.ingresos)}</p>
									</div>
								))}
							</div>
						)}
					</div>
				))}
			</div>
		</div>
	);
}
