import { useNavigate } from 'react-router-dom'
import { useEffect } from 'react'

export default function Torneo() {
  const navigate = useNavigate()
  
  // Redirigir automáticamente al componente de administración
  useEffect(() => {
    navigate('/torneos/ConsultarTorneos')
  }, [navigate])

  return null
}