import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { login as authLogin } from '../../services/auth.service'
import { useModal } from '../../contexts/ModalContext'
import { useAuth } from '../../contexts/AuthContext'

const Login: React.FC = () => {
  const [usuario, setUsuario] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()
  const { openModal, closeModal } = useModal()
  const { setAuth } = useAuth()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    if (!usuario || !password) {
      setError('Completa usuario y contraseña')
      return
    }

    try {
      setLoading(true)
      const data = await authLogin(usuario, password)
      // esperar que el backend responda con { token, user }
      if (data?.token) {
        // use AuthContext to store auth state
        setAuth(data.token, data.user ?? null)
        // close modal then navigate
        closeModal()
        navigate('/')
      } else {
        setError('Respuesta inválida del servidor')
      }
    } catch (err: any) {
      setError(err?.message || 'Error al iniciar sesión')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex items-center justify-center">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-md bg-white/90 dark:bg-gray-800/80 rounded-lg shadow-md p-6 space-y-4"
        aria-label="login-form"
      >
        <h2 className="text-2xl font-semibold text-center text-gray-800 dark:text-gray-100">Iniciar sesión</h2>

        {error && (
          <div className="text-sm text-red-700 bg-red-100 px-3 py-2 rounded">{error}</div>
        )}

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-200">Usuario</label>
            <input
              type="text"
              value={usuario}
              onChange={(e) => setUsuario(e.target.value)}
              placeholder="usuario o email"
              required
              className="mt-1 block w-full rounded-md border-gray-200 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-200">Contraseña</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Contraseña"
            required
            className="mt-1 block w-full rounded-md border-gray-200 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          />
        </div>

        <div className="flex items-center justify-between">
          <button
            type="submit"
            disabled={loading}
            className="inline-flex items-center justify-center rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-60"
          >
            {loading ? 'Ingresando...' : 'Ingresar'}
          </button>

          <div className="text-sm text-gray-500">
            ¿No tiene cuenta?{' '}
            <button
              type="button"
              onClick={() => openModal('register')}
              className="text-indigo-600 hover:underline"
            >
              Crear cuenta
            </button>
          </div>
        </div>
      </form>
    </div>
  )
}

export default Login
