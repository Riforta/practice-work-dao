import { Navigate } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'

interface ProtectedRouteProps {
  children: React.ReactNode
  requireAdmin?: boolean
  requireAuth?: boolean
}

/**
 * Componente para proteger rutas basado en autenticación y roles
 * 
 * @param requireAuth - Si true, requiere que el usuario esté logueado
 * @param requireAdmin - Si true, requiere que el usuario sea administrador (id_rol === 1)
 */
export default function ProtectedRoute({ 
  children, 
  requireAdmin = false,
  requireAuth = false 
}: ProtectedRouteProps) {
  const { user, token } = useAuth()

  // Si requiere autenticación y no hay usuario logueado
  if (requireAuth && !token) {
    return <Navigate to="/" replace />
  }

  // Si requiere admin y el usuario no es admin
  if (requireAdmin && (!user || user.id_rol !== 1)) {
    return <Navigate to="/" replace />
  }

  return <>{children}</>
}
