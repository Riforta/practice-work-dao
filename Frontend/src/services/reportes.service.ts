import http from './http';

export interface ResumenGeneral {
	total_canchas: number;
	total_clientes: number;
	clientes_activos: number;
	total_reservas: number;
	total_ingresos: number;
	ingreso_promedio_por_reserva: number;
	fecha_generacion: string;
}

export interface ReservaDetalle {
	id_turno: number;
	cancha: string;
	fecha_hora_inicio: string;
	fecha_hora_fin: string;
	precio_final: number;
	monto_servicios: number;
	total: number;
	reserva_created_at: string | null;
}

export interface ReservaPorCliente {
	id_cliente: number;
	nombre_cliente: string;
	dni: string;
	telefono: string;
	cantidad_reservas: number;
	total_gastado: number;
	total_servicios: number;
	reservas: ReservaDetalle[];
}

export interface ReservaCanchaDetalle {
	id_turno: number;
	fecha_hora_inicio: string;
	fecha_hora_fin: string;
	cliente: string;
	precio_final: number;
}

export interface ReservaPorCancha {
	id_cancha: number;
	nombre_cancha: string;
	tipo_cancha: string;
	cantidad_reservas: number;
	ingresos_totales: number;
	reservas: ReservaCanchaDetalle[];
}

export interface CanchaMasUtilizada {
	id_cancha: number;
	nombre_cancha: string;
	tipo_cancha: string;
	cantidad_reservas: number;
	ingresos_totales: number;
	precio_promedio: number;
}

export interface CanchaUtilizacion {
	id_cancha: number;
	nombre_cancha: string;
	cantidad_reservas: number;
	ingresos: number;
}

export interface UtilizacionMensual {
	mes: number;
	nombre_mes: string;
	anio: number;
	total_reservas: number;
	ingresos_totales: number;
	canchas: CanchaUtilizacion[];
}

class ReportesService {
	private readonly BASE_URL = '/reportes';

	async getResumenGeneral(): Promise<ResumenGeneral> {
		const response = await http.get<ResumenGeneral>(`${this.BASE_URL}/resumen`);
		return response.data;
	}

	async getReservasPorCliente(idCliente?: number): Promise<ReservaPorCliente[]> {
		const params = idCliente ? { id_cliente: idCliente } : {};
		const response = await http.get<ReservaPorCliente[]>(`${this.BASE_URL}/reservas-por-cliente`, { params });
		return response.data;
	}

	async getReservasPorCancha(
		fechaInicio: string,
		fechaFin: string,
		idCancha?: number
	): Promise<ReservaPorCancha[]> {
		const params: any = {
			fecha_inicio: fechaInicio,
			fecha_fin: fechaFin,
		};
		if (idCancha) {
			params.id_cancha = idCancha;
		}
		const response = await http.get<ReservaPorCancha[]>(`${this.BASE_URL}/reservas-por-cancha`, { params });
		return response.data;
	}

	async getCanchasMasUtilizadas(limite: number = 10): Promise<CanchaMasUtilizada[]> {
		const response = await http.get<CanchaMasUtilizada[]>(`${this.BASE_URL}/canchas-mas-utilizadas`, {
			params: { limite },
		});
		return response.data;
	}

	async getUtilizacionMensual(anio?: number): Promise<UtilizacionMensual[]> {
		const params = anio ? { anio } : {};
		const response = await http.get<UtilizacionMensual[]>(`${this.BASE_URL}/utilizacion-mensual`, { params });
		return response.data;
	}
}

const reportesService = new ReportesService();
export default reportesService;
