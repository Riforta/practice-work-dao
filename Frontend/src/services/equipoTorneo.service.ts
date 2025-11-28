import http from './http';

export interface EquipoTorneo {
	id_equipo: number;
	id_torneo: number;
	fecha_inscripcion?: string | null;
}

const endpoint = '/equipo-torneo';

const normalize = (raw: any): EquipoTorneo => ({
	id_equipo: raw?.id_equipo ?? raw?.equipoId ?? raw?.idEquipo ?? 0,
	id_torneo: raw?.id_torneo ?? raw?.torneoId ?? raw?.idTorneo ?? 0,
	fecha_inscripcion: raw?.fecha_inscripcion ?? raw?.fechaInscripcion ?? null,
});

const extractList = (data: any) => {
	const raw = data?.items ?? data?.Items ?? data;
	return Array.isArray(raw) ? raw : [];
};

const inscribirEquipo = async (id_equipo: number, id_torneo: number): Promise<EquipoTorneo> => {
	const response = await http.post(`${endpoint}/inscribir`, { id_equipo, id_torneo });
	return normalize(response.data?.data ?? response.data);
};

const inscribirEquiposMasivo = async (ids_equipos: number[], id_torneo: number): Promise<number> => {
	if (!ids_equipos.length) return 0;
	const response = await http.post(`${endpoint}/inscribir-masivo`, { ids_equipos, id_torneo });
	return response.data?.count ?? ids_equipos.length;
};

const desinscribirEquipo = async (id_equipo: number, id_torneo: number): Promise<void> => {
	await http.delete(`${endpoint}/desinscribir`, { params: { id_equipo, id_torneo } });
};

const desinscribirEquiposMasivo = async (inscripciones: Array<[number, number]>): Promise<number> => {
	if (!inscripciones.length) return 0;
	const response = await http.delete(`${endpoint}/desinscribir-masivo`, { data: { inscripciones } });
	return response.data?.count ?? inscripciones.length;
};

const listarEquiposPorTorneo = async (id_torneo: number): Promise<EquipoTorneo[]> => {
	const response = await http.get(`${endpoint}/torneo/${id_torneo}`);
	return extractList(response.data).map(normalize);
};

const listarTorneosPorEquipo = async (id_equipo: number): Promise<EquipoTorneo[]> => {
	const response = await http.get(`${endpoint}/equipo/${id_equipo}`);
	return extractList(response.data).map(normalize);
};

const contarEquiposTorneo = async (id_torneo: number): Promise<number> => {
	const response = await http.get(`${endpoint}/torneo/${id_torneo}/count`);
	return response.data?.count ?? 0;
};

const eliminarTodasInscripcionesTorneo = async (id_torneo: number): Promise<number> => {
	const response = await http.delete(`${endpoint}/torneo/${id_torneo}/all`);
	return response.data?.count ?? 0;
};

const eliminarTodasInscripcionesEquipo = async (id_equipo: number): Promise<number> => {
	const response = await http.delete(`${endpoint}/equipo/${id_equipo}/all`);
	return response.data?.count ?? 0;
};

// Helper para asignar equipos a torneo (compatible con código existente)
const assignEquiposToTorneo = async (id_torneo: number, equipoIds: number[]): Promise<void> => {
	await inscribirEquiposMasivo(equipoIds, id_torneo);
};

export default {
	inscribirEquipo,
	inscribirEquiposMasivo,
	desinscribirEquipo,
	desinscribirEquiposMasivo,
	listarEquiposPorTorneo,
	listarTorneosPorEquipo,
	contarEquiposTorneo,
	eliminarTodasInscripcionesTorneo,
	eliminarTodasInscripcionesEquipo,
	assignEquiposToTorneo,
};
