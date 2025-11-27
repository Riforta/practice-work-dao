import http from './http';

export interface Inscripcion {
	id?: number;
	id_equipo: number;
	id_torneo: number;
	fecha_inscripcion?: string | null;
	estado?: string | null;
}

const endpoint = '/inscripciones';

const normalize = (raw: any): Inscripcion => ({
	id: raw?.id ?? raw?.Id ?? raw?.ID ?? undefined,
	id_equipo: raw?.id_equipo ?? raw?.equipoId ?? raw?.idEquipo ?? 0,
	id_torneo: raw?.id_torneo ?? raw?.torneoId ?? raw?.idTorneo ?? 0,
	fecha_inscripcion: raw?.fecha_inscripcion ?? raw?.fechaInscripcion ?? null,
	estado: raw?.estado ?? null,
});

const extractList = (data: any) => {
	const raw = data?.Items ?? data?.items ?? data;
	return Array.isArray(raw) ? raw : [];
};

const list = async (): Promise<Inscripcion[]> => {
	const response = await http.get(`${endpoint}/`);
	return extractList(response.data).map(normalize);
};

const listByTorneo = async (torneoId: number): Promise<Inscripcion[]> => {
	const response = await http.get(`${endpoint}/torneo/${torneoId}`);
	const raw = response.data?.Items ?? response.data?.items ?? response.data ?? [];
	return (Array.isArray(raw) ? raw : []).map(normalize);
};

const create = async (payload: Omit<Inscripcion, 'id'>): Promise<Inscripcion> => {
	const response = await http.post(`${endpoint}/`, payload);
	return normalize(response.data);
};

const remove = async (id: number): Promise<void> => {
	await http.delete(`${endpoint}/${id}`);
};

const removeMany = async (ids: number[]): Promise<void> => {
	await Promise.all(ids.map((inscripcionId) => http.delete(`${endpoint}/${inscripcionId}`)));
};

const assignEquiposToTorneo = async (
	torneoId: number,
	equipoIds: number[],
	opts?: { estado?: string; fecha?: string }
) => {
	if (!equipoIds.length) return;
	const now = opts?.fecha ?? new Date().toISOString();
	const estado = opts?.estado ?? 'confirmada';
	await Promise.all(
		equipoIds.map((equipoId) =>
			create({
				id_equipo: equipoId,
				id_torneo: torneoId,
				fecha_inscripcion: now,
				estado,
			})
		)
	);
};

export default {
	list,
	listByTorneo,
	create,
	remove,
	removeMany,
	assignEquiposToTorneo,
};
