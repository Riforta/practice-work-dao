import { useNavigate } from 'react-router-dom'
import { useEffect } from 'react'

export default function Equipo() {
  const navigate = useNavigate()
  
  // Redirigir automáticamente al componente de administración
  useEffect(() => {
    navigate('/equipos/ConsultarEquipo')
  }, [navigate])

  return null
}