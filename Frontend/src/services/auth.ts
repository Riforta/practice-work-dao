export interface LoginResponse {
  token?: string
  user?: any
}

// If VITE_API_BASE is not set during dev, default to the backend common dev port.
// Adjust this if your backend runs on a different host/port.
const BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export async function login(usuario: string, password: string): Promise<LoginResponse> {
  // Enviamos 'usuario' como campo identificador (puede ser username o email según backend)
  const res = await fetch(`${BASE}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ usuario, password }),
  })

  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || 'Error en autenticación')
  }

  const data = await res.json()
  return data
}

export function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
}

export async function register(username: string, email: string, password: string): Promise<LoginResponse> {
  // Backend router exposes POST /usuarios/ to create users
  const res = await fetch(`${BASE}/usuarios/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  // Send multiple keys to be compatible with small inconsistencies in the backend:
  // - 'username' (used by some service helpers)
  // - 'nombre_usuario' (the Usuario model field)
  // - 'password' (plain password; backend will hash it)
  body: JSON.stringify({ username, nombre_usuario: username, email, password }),
  })

  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || 'Error en el registro')
  }

  const data = await res.json()
  return data
}
