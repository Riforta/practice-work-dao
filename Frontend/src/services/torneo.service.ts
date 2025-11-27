import http from './http';

export interface Torneo {
	id?: number;
	nombre: string;
	tipo_deporte: string;
	created_at?: string | null;
	fecha_inicio?: string | null;
	fecha_fin?: string | null;
	costo_inscripcion?: number;
	cupos?: number | null;
	reglas?: string | null;
	estado?: string | null;
}

const endpoint = '/torneos';
const turnosEndpoint = '/turnos';
const torneoTagPrefix = 'Torneo:';

const normalize = (raw: any): Torneo => ({
	id: raw?.id ?? raw?.Id ?? undefined,
	nombre: raw?.nombre ?? '',
	tipo_deporte: raw?.tipo_deporte ?? raw?.tipoDeporte ?? '',
	created_at: raw?.created_at ?? raw?.createdAt ?? null,
	fecha_inicio: raw?.fecha_inicio ?? raw?.fechaInicio ?? null,
	fecha_fin: raw?.fecha_fin ?? raw?.fechaFin ?? null,
	costo_inscripcion: raw?.costo_inscripcion != null ? Number(raw?.costo_inscripcion) : undefined,
	cupos: raw?.cupos != null ? Number(raw?.cupos) : null,
	reglas: raw?.reglas ?? null,
	estado: raw?.estado ?? null,
});

const list = async (): Promise<Torneo[]> => {
	const response = await http.get(`${endpoint}/`);
	const raw = response.data?.Items ?? response.data?.items ?? response.data ?? [];
	return (Array.isArray(raw) ? raw : []).map(normalize);
};

const getById = async (id: number): Promise<Torneo> => {
	const response = await http.get(`${endpoint}/${id}`);
	return normalize(response.data);
};

const create = async (data: Omit<Torneo, 'id'>): Promise<Torneo> => {
	const response = await http.post(`${endpoint}/`, data);
	return normalize(response.data);
};

const update = async (id: number, data: Partial<Omit<Torneo, 'id'>>): Promise<Torneo> => {
	const response = await http.put(`${endpoint}/${id}`, data);
	return normalize(response.data);
};

const remove = async (id: number): Promise<void> => {
	await http.delete(`${endpoint}/${id}`);
};

export const buildTorneoTurnoTag = (torneoId: number) => `${torneoTagPrefix}${torneoId}`;

const mapTurnoUpdatePayload = (estado: string, motivo: string | null, userId?: number | null) => ({
	estado,
	motivo_bloqueo: motivo,
	id_usuario_bloqueo: userId ?? null,
});

const getTorneoIdFromMotivo = (motivo?: string | null): number | null => {
	if (!motivo?.startsWith(torneoTagPrefix)) return null;
	const raw = motivo.substring(torneoTagPrefix.length);
	const value = Number(raw);
	return Number.isFinite(value) ? value : null;
};

const assignTurnosToTorneo = async (torneoId: number, turnoIds: number[], userId?: number | null) => {
	if (!turnoIds?.length) return;
	const motivo = buildTorneoTurnoTag(torneoId);
	await Promise.all(
		turnoIds.map((turnoId) =>
			http.put(`${turnosEndpoint}/${turnoId}`, mapTurnoUpdatePayload('bloqueado', motivo, userId))
		)
	);
};

const releaseTurnosFromTorneo = async (turnoIds: number[]) => {
	if (!turnoIds?.length) return;
	await Promise.all(
		turnoIds.map((turnoId) => http.put(`${turnosEndpoint}/${turnoId}`, mapTurnoUpdatePayload('disponible', null)))
	);
};

export default {
	list,
	getById,
	create,
	update,
	remove,
	assignTurnosToTorneo,
	releaseTurnosFromTorneo,
	buildTorneoTurnoTag,
	getTorneoIdFromMotivo,
};

export { getTorneoIdFromMotivo };
