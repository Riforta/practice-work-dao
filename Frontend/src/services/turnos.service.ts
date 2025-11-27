import axios from 'axios';
import http from './http';

export type TurnoEstado =
  | 'disponible'
  | 'reservado'
  | 'bloqueado'
  | 'cancelado'
  | 'finalizado'
  | 'no_disponible'
  | string;

export interface Turno {
  id?: number;
  id_cancha: number;
  fecha_hora_inicio: string;
  fecha_hora_fin: string;
  estado: TurnoEstado;
  precio_final: number;
  id_cliente?: number;
  id_usuario_registro?: number;
  reserva_created_at?: string;
  id_usuario_bloqueo?: number;
  motivo_bloqueo?: string;
  pago?: {
    id: number;
    monto_turno: number;
    monto_servicios: number;
    monto_total: number;
    estado: string;
    metodo_pago?: string;
    fecha_creacion?: string;
    fecha_completado?: string;
  };
  servicios?: Array<{
    id_servicio: number;
    cantidad: number;
    precio_unitario: number;
  }>;
}

export interface CanchaRef {
  id: number;
  nombre: string;
  tipo_deporte?: string;
}

// No se usa mas
/*const BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000/api';*/
const endpoint = `/turnos`;
const canchasEndpoint = `/canchas`;

const normalizeTurno = (raw: any): Turno => ({
  id: raw?.id ?? raw?.Id ?? raw?.ID ?? undefined,
  id_cancha: raw?.id_cancha ?? raw?.Id_cancha ?? raw?.Id_Cancha ?? 0,
  fecha_hora_inicio: raw?.fecha_hora_inicio ?? raw?.Fecha_hora_inicio ?? raw?.fecha_inicio ?? '',
  fecha_hora_fin: raw?.fecha_hora_fin ?? raw?.Fecha_hora_fin ?? raw?.fecha_fin ?? '',
  estado: (raw?.estado ?? raw?.Estado ?? 'disponible') as TurnoEstado,
  precio_final: Number(raw?.precio_final ?? raw?.Precio_final ?? 0),
  id_cliente: raw?.id_cliente ?? raw?.Id_cliente ?? raw?.Id_Cliente ?? undefined,
  id_usuario_registro: raw?.id_usuario_registro ?? raw?.Id_usuario_registro ?? undefined,
  reserva_created_at: raw?.reserva_created_at,
  id_usuario_bloqueo: raw?.id_usuario_bloqueo ?? undefined,
  motivo_bloqueo: raw?.motivo_bloqueo ?? undefined,
  // Mantener campos adicionales que vienen del backend (pago y servicios)
  pago: raw?.pago,
  servicios: raw?.servicios,
});

const normalizeCancha = (raw: any): CanchaRef => ({
  id: raw?.id ?? raw?.Id ?? raw?.ID ?? 0,
  nombre: raw?.nombre ?? raw?.Nombre ?? '',
  tipo_deporte: raw?.tipo_deporte ?? raw?.Tipo_deporte ?? raw?.deporte,
});

// -------- Turnos CRUD --------

const list = async (): Promise<Turno[]> => {
  const response = await http.get(`${endpoint}/`);
  const raw = response.data?.Items ?? response.data?.items ?? response.data ?? [];
  const items = Array.isArray(raw) ? raw : [];
  return items.map(normalizeTurno);
};

const listByCancha = async (id_cancha: number): Promise<Turno[]> => {
  const response = await http.get(`${endpoint}/cancha/${id_cancha}`);
  const items = Array.isArray(response.data) ? response.data : response.data?.Items ?? response.data?.items ?? [];
  return items.map(normalizeTurno);
};

const listByEstado = async (estado: string): Promise<Turno[]> => {
  const response = await http.get(`${endpoint}/estado/${estado}`);
  const items = Array.isArray(response.data) ? response.data : response.data?.Items ?? response.data?.items ?? [];
  return items.map(normalizeTurno);
};

const listByCliente = async (id_cliente: number): Promise<Turno[]> => {
  const response = await http.get(`${endpoint}/cliente/${id_cliente}`);
  const items = Array.isArray(response.data) ? response.data : response.data?.Items ?? response.data?.items ?? [];
  return items.map(normalizeTurno);
};

const searchDisponibles = async (id_cancha: number, fecha_inicio: string, fecha_fin: string): Promise<Turno[]> => {
  const response = await http.get(`${endpoint}/disponibles`, {
    params: { id_cancha, fecha_inicio, fecha_fin },
  });
  const items = Array.isArray(response.data) ? response.data : response.data?.Items ?? response.data?.items ?? [];
  return items.map(normalizeTurno);
};

const getById = async (id: number): Promise<Turno> => {
  const response = await http.get(`${endpoint}/${id}`);
  return normalizeTurno(response.data);
};

const create = async (data: Omit<Turno, 'id' | 'reserva_created_at'>): Promise<Turno> => {
  const response = await http.post(`${endpoint}/`, data);
  return normalizeTurno(response.data);
};

const update = async (id: number, data: Partial<Omit<Turno, 'id'>>): Promise<Turno> => {
  const response = await http.put(`${endpoint}/${id}`, data);
  return normalizeTurno(response.data);
};

const remove = async (id: number): Promise<void> => {
  await http.delete(`${endpoint}/${id}`);
};

// -------- Acciones de reserva/estado --------

const reservarSimple = async (turno_id: number, id_cliente: number, id_usuario_registro?: number): Promise<Turno> => {
  const response = await http.post(`${endpoint}/${turno_id}/reservar`, {
    id_cliente,
    id_usuario_registro,
  });
  return normalizeTurno(response.data);
};

const cancelarReserva = async (turno_id: number): Promise<Turno> => {
  const response = await http.post(`${endpoint}/${turno_id}/cancelar-reserva`);
  return normalizeTurno(response.data);
};

const cambiarEstado = async (turno_id: number, estado: TurnoEstado): Promise<void> => {
  await http.patch(`${endpoint}/${turno_id}/estado`, { estado });
};

// -------- Canchas helpers (para selects) --------

const listCanchas = async (): Promise<CanchaRef[]> => {
  const response = await http.get(`${canchasEndpoint}/`);
  const raw = response.data?.Items ?? response.data?.items ?? response.data ?? [];
  const items = Array.isArray(raw) ? raw : [];
  return items.map(normalizeCancha);
};

export default {
  list,
  listByCancha,
  listByEstado,
  listByCliente,
  searchDisponibles,
  getById,
  create,
  update,
  remove,
  reservarSimple,
  cancelarReserva,
  cambiarEstado,
  listCanchas,
};
