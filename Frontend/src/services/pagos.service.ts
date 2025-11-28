import http from './http';

export interface Pago {
	id?: number;
	id_turno?: number | null;
	monto_turno: number;
	monto_servicios: number;
	monto_total: number;
	id_cliente: number;
	id_usuario_registro?: number | null;
	estado: string;
	metodo_pago?: string | null;
	id_gateway_externo?: string | null;
	fecha_creacion?: string | null;
	fecha_expiracion?: string | null;
	fecha_completado?: string | null;
}

const endpoint = '/pagos';

const normalize = (raw: any): Pago => ({
	id: raw?.id ?? raw?.Id ?? raw?.ID,
	id_turno: raw?.id_turno ?? raw?.idTurno,
	monto_turno: raw?.monto_turno ?? raw?.montoTurno ?? 0,
	monto_servicios: raw?.monto_servicios ?? raw?.montoServicios ?? 0,
	monto_total: raw?.monto_total ?? raw?.montoTotal ?? 0,
	id_cliente: raw?.id_cliente ?? raw?.idCliente ?? 0,
	id_usuario_registro: raw?.id_usuario_registro ?? raw?.idUsuarioRegistro,
	estado: raw?.estado ?? 'iniciado',
	metodo_pago: raw?.metodo_pago ?? raw?.metodoPago,
	id_gateway_externo: raw?.id_gateway_externo ?? raw?.idGatewayExterno,
	fecha_creacion: raw?.fecha_creacion ?? raw?.fechaCreacion,
	fecha_expiracion: raw?.fecha_expiracion ?? raw?.fechaExpiracion,
	fecha_completado: raw?.fecha_completado ?? raw?.fechaCompletado,
});

const extractList = (data: any) => {
	const raw = data?.items ?? data?.Items ?? data;
	return Array.isArray(raw) ? raw : [];
};

const listarTodos = async (): Promise<Pago[]> => {
	const response = await http.get(`${endpoint}/`);
	return extractList(response.data).map(normalize);
};

const obtenerPorId = async (id: number): Promise<Pago> => {
	const response = await http.get(`${endpoint}/${id}`);
	return normalize(response.data);
};

const listarPorCliente = async (id_cliente: number): Promise<Pago[]> => {
	const response = await http.get(`${endpoint}/cliente/${id_cliente}`);
	return extractList(response.data).map(normalize);
};

const obtenerPorTurno = async (id_turno: number): Promise<Pago | null> => {
	try {
		const response = await http.get(`${endpoint}/turno/${id_turno}`);
		return normalize(response.data);
	} catch {
		return null;
	}
};

const crearPagoTurno = async (payload: {
	id_turno: number;
	id_cliente: number;
	monto_turno: number;
	monto_servicios?: number;
	servicios?: any[];
	metodo_pago?: string;
}): Promise<Pago> => {
	const response = await http.post(`${endpoint}/turno`, payload);
	return normalize(response.data);
};

const crearPagoManual = async (payload: Partial<Pago>): Promise<Pago> => {
	const response = await http.post(`${endpoint}/manual`, payload);
	return normalize(response.data);
};

const confirmarPago = async (
	pago_id: number,
	metodo_pago?: string,
	id_gateway_externo?: string
): Promise<Pago> => {
	const response = await http.post(`${endpoint}/${pago_id}/confirmar`, {
		metodo_pago,
		id_gateway_externo,
	});
	return normalize(response.data);
};

const marcarFallido = async (pago_id: number): Promise<void> => {
	await http.post(`${endpoint}/${pago_id}/marcar-fallido`);
};

const eliminar = async (pago_id: number): Promise<void> => {
	await http.delete(`${endpoint}/${pago_id}`);
};

export default {
	listarTodos,
	obtenerPorId,
	listarPorCliente,
	obtenerPorTurno,
	crearPagoTurno,
	crearPagoManual,
	confirmarPago,
	marcarFallido,
	eliminar,
};
