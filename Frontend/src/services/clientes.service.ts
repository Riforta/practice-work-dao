import axios from 'axios';
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

export default {
  list,
  searchByName,
  getById,
  async create(data: Omit<Cliente, 'id'>): Promise<Cliente> {
    // Enviar solo los campos necesarios, limpios
    const payload = {
      nombre: data.nombre?.trim() || '',
      apellido: data.apellido?.trim() || '',
      dni: data.dni?.toString().trim() || '',
      telefono: data.telefono?.toString().trim() || '',
      email: data.email?.trim() || '',
    };

    const response = await axios.post(`${endpoint}`, payload, {
      headers: { 'Content-Type': 'application/json' },
    });
    return normalizeCliente(response.data);
  },
  async update(id: number, data: Partial<Omit<Cliente, 'id'>>): Promise<Cliente> {
    const payload = {
      nombre: data.nombre?.trim(),
      apellido: data.apellido?.trim(),
      dni: data.dni?.toString().trim(),
      telefono: data.telefono?.toString().trim(),
      email: data.email?.trim(),
    };
    // Remover campos undefined
    Object.keys(payload).forEach(k => payload[k as keyof typeof payload] === undefined && delete payload[k as keyof typeof payload]);

    const response = await axios.put(`${endpoint}/${id}`, payload, {
      headers: { 'Content-Type': 'application/json' },
    });
    return normalizeCliente(response.data);
  },
  async delete(id: number): Promise<void> {
    await axios.delete(`${endpoint}/${id}`);
  },
};
