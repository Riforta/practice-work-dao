import http from './http';

export interface ServicioAdicional {
  id?: number;
  nombre: string;
  precio_actual: number;
  activo: boolean;
}

const BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000/api';
const endpoint = `${BASE}/servicios_adicionales`;

const normalizeServicio = (raw: any): ServicioAdicional => ({
  id: raw?.id ?? raw?.Id ?? raw?.ID ?? undefined,
  nombre: raw?.nombre ?? raw?.Nombre ?? '',
  precio_actual: Number(raw?.precio_actual ?? raw?.precio ?? 0),
  activo: Boolean(raw?.activo ?? raw?.Activo ?? raw?.activa ?? raw?.Activa ?? false),
});

const buildPayload = (data: Partial<ServicioAdicional>) => {
  const payload: Record<string, unknown> = {
    nombre: data.nombre,
    precio_actual: data.precio_actual,
  };

  if (data.activo !== undefined) {
    payload.activo = data.activo ? 1 : 0;
  }

  return payload;
};

const list = async (): Promise<ServicioAdicional[]> => {
  const response = await http.get(`${endpoint}/`);
  const raw = response.data?.Items ?? response.data?.items ?? response.data ?? [];
  const items = Array.isArray(raw) ? raw : [];
  return items.map(normalizeServicio);
};

const searchByName = async (term: string): Promise<ServicioAdicional[]> => {
  const all = await list();
  const needle = term.trim().toLowerCase();
  if (!needle) return all;
  return all.filter((s) => s.nombre.toLowerCase().includes(needle));
};

const getById = async (id: number): Promise<ServicioAdicional> => {
  const response = await http.get(`${endpoint}/${id}`);
  return normalizeServicio(response.data);
};

const create = async (data: Omit<ServicioAdicional, 'id'>): Promise<ServicioAdicional> => {
  const response = await http.post(`${endpoint}/`, buildPayload(data));
  return normalizeServicio(response.data);
};

const update = async (
  id: number,
  data: Partial<Omit<ServicioAdicional, 'id'>>
): Promise<ServicioAdicional> => {
  const response = await http.put(`${endpoint}/${id}`, buildPayload(data));
  return normalizeServicio(response.data);
};

const remove = async (id: number): Promise<void> => {
  await http.delete(`${endpoint}/${id}`);
};

export default {
  list,
  searchByName,
  getById,
  create,
  update,
  remove,
};
