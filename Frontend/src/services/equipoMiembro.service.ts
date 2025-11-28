import http from './http';

export interface EquipoMiembro {
	id_equipo: number;
	id_cliente: number;
}

const endpoint = '/equipo_miembros';

const normalize = (raw: any): EquipoMiembro => ({
	id_equipo: raw?.id_equipo ?? raw?.equipoId ?? raw?.idEquipo ?? 0,
	id_cliente: raw?.id_cliente ?? raw?.clienteId ?? raw?.idCliente ?? 0,
});

const extractList = (data: any) => {
	const raw = data?.items ?? data?.Items ?? data;
	return Array.isArray(raw) ? raw : [];
};

const agregarMiembro = async (id_equipo: number, id_cliente: number): Promise<void> => {
	await http.post(`${endpoint}/`, { id_equipo, id_cliente });
};

const agregarMiembrosMasivo = async (id_equipo: number, ids_clientes: number[]): Promise<void> => {
	if (!ids_clientes.length) return;
	await Promise.all(
		ids_clientes.map((id_cliente) => agregarMiembro(id_equipo, id_cliente))
	);
};

const listarMiembrosPorEquipo = async (equipo_id: number): Promise<EquipoMiembro[]> => {
	const response = await http.get(`${endpoint}/`, { params: { equipo_id } });
	return extractList(response.data).map(normalize);
};

const eliminarMiembro = async (id_equipo: number, id_cliente: number): Promise<void> => {
	await http.delete(`${endpoint}/${id_equipo}/${id_cliente}`);
};

const eliminarMiembrosMasivo = async (miembros: Array<[number, number]>): Promise<void> => {
	if (!miembros.length) return;
	await Promise.all(
		miembros.map(([id_equipo, id_cliente]) => eliminarMiembro(id_equipo, id_cliente))
	);
};

export default {
	agregarMiembro,
	agregarMiembrosMasivo,
	listarMiembrosPorEquipo,
	eliminarMiembro,
	eliminarMiembrosMasivo,
};
