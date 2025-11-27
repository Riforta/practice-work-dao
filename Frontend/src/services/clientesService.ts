export interface Cliente {
  id_cliente?: number;
  nombre: string;
  apellido: string;
  dni: string;
  email: string;
  telefono?: string;
}

const BASE_URL = "/api/clientes";

export async function listarClientes(params?: Partial<Cliente>) {
  const query = params
    ? "?" + new URLSearchParams(
        Object.entries(params).reduce((acc, [k, v]) => {
          if (v !== undefined && v !== null && String(v).trim() !== "") acc[k] = String(v);
          return acc;
        }, {} as Record<string, string>)
      ).toString()
    : "";
  const res = await fetch(`${BASE_URL}${query}`, { credentials: "include" });
  if (!res.ok) throw new Error("Error obteniendo clientes");
  return res.json();
}

export async function crearCliente(data: Cliente) {
  const res = await fetch(BASE_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Error creando cliente");
  return res.json();
}

export async function actualizarCliente(id: number, data: Cliente) {
  const res = await fetch(`${BASE_URL}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Error actualizando cliente");
  return res.json();
}

export async function eliminarCliente(id: number) {
  const res = await fetch(`${BASE_URL}/${id}`, {
    method: "DELETE",
    credentials: "include",
  });
  if (!res.ok) throw new Error("Error eliminando cliente");
  return true;
}
