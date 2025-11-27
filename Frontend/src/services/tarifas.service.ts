import axios from 'axios';
import http from './http';

export interface Tarifa {
  id?: number;
  id_cancha: number;
  descripcion?: string;
  precio_hora: number;
}

const BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000/api';
const endpoint = `${BASE}/tarifas`;

const normalizeTarifa = (raw: any): Tarifa => ({
  id: raw?.id ?? raw?.Id ?? raw?.ID ?? undefined,
  id_cancha: raw?.id_cancha ?? raw?.Id_cancha ?? raw?.Id_Cancha ?? 0,
  descripcion: raw?.descripcion ?? raw?.Descripcion ?? undefined,
  precio_hora: Number(raw?.precio_hora ?? raw?.Precio_hora ?? 0),
});

const list = async (): Promise<Tarifa[]> => {
  const response = await http.get(`${endpoint}/`);
  const raw = response.data?.Items ?? response.data?.items ?? response.data ?? [];
  const items = Array.isArray(raw) ? raw : [];
  return items.map(normalizeTarifa);
};

export default { list };
