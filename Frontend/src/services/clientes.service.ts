import http from './http';

export interface Cliente {
  id: number;
  nombre: string;
  apellido?: string;
  dni?: string;
  telefono?: string;
  email?: string;
}

const BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000/api';
const endpoint = `${BASE}/clientes`;

const normalizeCliente = (raw: any): Cliente => ({
  id: raw?.id ?? raw?.Id ?? raw?.ID ?? 0,
  nombre: raw?.nombre ?? raw?.Nombre ?? '',
  apellido: raw?.apellido ?? raw?.Apellido ?? '',
  dni: raw?.dni ?? raw?.Dni ?? raw?.DNI,
  telefono: raw?.telefono ?? raw?.Telefono ?? '',
  email: raw?.email ?? raw?.Email ?? '',
});

const list = async (): Promise<Cliente[]> => {
  const response = await http.get(`${endpoint}/`);
  const raw = response.data?.Items ?? response.data?.items ?? response.data ?? [];
  const items = Array.isArray(raw) ? raw : [];
  return items.map(normalizeCliente);
};

const searchByName = async (term: string): Promise<Cliente[]> => {
  if (!term.trim()) return [];
  const response = await http.get(`${endpoint}/search`, { params: { nombre: term } });
  const raw = response.data?.Items ?? response.data?.items ?? response.data ?? [];
  const items = Array.isArray(raw) ? raw : [];
  return items.map(normalizeCliente);
};

const getById = async (id: number): Promise<Cliente> => {
  const response = await http.get(`${endpoint}/${id}`);
  return normalizeCliente(response.data);
};

const create = async (data: Omit<Cliente, 'id'>): Promise<Cliente> => {
  const payload = {
    nombre: data.nombre,
    apellido: data.apellido || null,
    dni: data.dni || null,
    telefono: data.telefono || null,
    email: data.email || null,
  };
  const response = await http.post(`${endpoint}/`, payload);
  return normalizeCliente(response.data);
};

const update = async (id: number, data: Partial<Omit<Cliente, 'id'>>): Promise<Cliente> => {
  const payload: Record<string, any> = {};
  if (data.nombre !== undefined) payload.nombre = data.nombre;
  if (data.apellido !== undefined) payload.apellido = data.apellido || null;
  if (data.dni !== undefined) payload.dni = data.dni || null;
  if (data.telefono !== undefined) payload.telefono = data.telefono || null;
  if (data.email !== undefined) payload.email = data.email || null;
  
  const response = await http.put(`${endpoint}/${id}`, payload);
  return normalizeCliente(response.data);
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
