import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { register as authRegister } from '../../services/auth.service'
import { useModal } from '../../contexts/ModalContext'
import { useAuth } from '../../contexts/AuthContext'

const Register: React.FC = () => {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [name, setName] = useState('')
  const [lastname, setLastname] = useState('')
  const [phone, setPhone] = useState('')
  const [dni, setDni] = useState('')


  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const navigate = useNavigate()
  const { openModal, closeModal } = useModal()
  const { setAuth } = useAuth()

  const validateEmail = (value: string) => /\S+@\S+\.\S+/.test(value)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)

    if (!name ||!dni||!username || !email || !password) {
      setError('Completa todos los campos')
      return
    }

    if (!validateEmail(email)) {
      setError('Ingresa un email válido')
      return
    }

    const phoneNumber = Number(phone)
    if (!Number.isFinite(phoneNumber)) {
      setError('Ingresa un teléfono válido (solo números)')
      return
    }

    const dniNumber = Number(dni)
    if (!Number.isFinite(dniNumber)) {
      setError('Ingresa un DNI válido (solo números)')
      return
    }

    try {
      setLoading(true)
      const data = await authRegister(name, lastname, phoneNumber, dniNumber, username, email, password)

      if (data?.token) {
        // establish session
        setAuth(data.token, data.user ?? null)
        setSuccess('Registro completado. Redirigiendo...')
        setTimeout(() => {
          closeModal()
          navigate('/')
        }, 800)
        return
      }

      setSuccess('Cuenta creada correctamente. Puedes iniciar sesión.')
      setTimeout(() => {
        closeModal()
        navigate('/login')
      }, 800)
    } catch (err: any) {
      setError(err?.message || 'Error al registrar usuario')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex items-center justify-center">
      <form onSubmit={handleSubmit} className="w-full max-w-md bg-white/90 dark:bg-gray-800/80 rounded-lg shadow-md p-6 space-y-4" aria-label="register-form">
        <h2 className="text-2xl font-semibold text-center text-gray-800 dark:text-gray-100">Crear cuenta</h2>

        {error && <div className="text-sm text-red-700 bg-red-100 px-3 py-2 rounded">{error}</div>}
        {success && <div className="text-sm text-green-700 bg-green-100 px-3 py-2 rounded">{success}</div>}

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-200">Nombre</label>
          <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Nombre" required className="mt-1 block w-full rounded-md border-gray-200 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-200">Apellido</label>
          <input type="text" value={lastname} onChange={(e) => setLastname(e.target.value)} placeholder="Apellido" className="mt-1 block w-full rounded-md border-gray-200 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-200">Telefono</label>
          <input type="text" value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="Telefono" required className="mt-1 block w-full rounded-md border-gray-200 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-200">DNI</label>
          <input type="text" value={dni} onChange={(e) => setDni(e.target.value)} placeholder="DNI" className="mt-1 block w-full rounded-md border-gray-200 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-200">Nombre Usuario</label>
          <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Nombre de usuario" required className="mt-1 block w-full rounded-md border-gray-200 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-200">Email</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="tu@ejemplo.com" required className="mt-1 block w-full rounded-md border-gray-200 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-200">Contraseña</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Contraseña" required className="mt-1 block w-full rounded-md border-gray-200 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100" />
        </div>

        <div className="flex items-center justify-between">
          <button type="submit" disabled={loading} className="inline-flex items-center justify-center rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-60">{loading ? 'Registrando...' : 'Registrarse'}</button>

          <div className="text-sm text-gray-500">¿Ya tenés cuenta? <button type="button" onClick={() => openModal('login')} className="text-indigo-600 hover:underline">Ingresar</button></div>
        </div>
      </form>
    </div>
  )
}

export default Register
