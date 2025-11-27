import http from './http';

export interface Equipo {
	id?: number;
	nombre_equipo: string;
	id_capitan?: number | null;
}

const endpoint = '/equipos';

const normalize = (raw: any): Equipo => ({
	id:
		raw?.id ??
		raw?.Id ??
		raw?.ID ??
		raw?.id_equipo ??
		raw?.idEquipo ??
		raw?.ID_EQUIPO ??
		undefined,
	nombre_equipo: raw?.nombre_equipo ?? raw?.nombre ?? raw?.nombreEquipo ?? raw?.Nombre ?? '',
	id_capitan: raw?.id_capitan ?? raw?.idCapitan ?? raw?.id_capitan ?? null,
});

const extractList = (data: any) => {
	const list = data?.Items ?? data?.items ?? data;
	return Array.isArray(list) ? list : [];
};

const getAllEquipos = async (): Promise<Equipo[]> => {
	const response = await http.get(`${endpoint}/`);
	return extractList(response.data).map(normalize);
};

const getEquipoByName = async (name: string): Promise<Equipo[]> => {
	const response = await http.get(`${endpoint}/`, { params: { nombre: name } });
	return extractList(response.data)
		.map(normalize)
		.filter((item) => item.nombre_equipo.toLowerCase().includes(name.toLowerCase()));
};

const getById = async (id: number): Promise<Equipo | null> => {
	try {
		const response = await http.get(`${endpoint}/${id}`);
		return normalize(response.data);
	} catch (error) {
		console.error('❌ Error obteniendo equipo por ID:', error);
		return null;
	}
};

const deleteEquipo = async (id: number) => {
	await http.delete(`${endpoint}/${id}`);
};

const putEquipo = async (id: number, payload: Partial<Equipo>) => {
	const response = await http.put(`${endpoint}/${id}`, payload);
	return normalize(response.data);
};

const creatEquipo = async (payload: Partial<Equipo>) => {
	const response = await http.post(`${endpoint}/`, payload);
	return normalize(response.data);
};

export default {
	getAllEquipos,
	getEquipoByName,
	deleteEquipo,
	getById,
	actualizarEquipo: putEquipo,
	creatEquipo,
};