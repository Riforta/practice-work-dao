import { Link } from 'react-router-dom'
import libertadores from './imagenes/libertadores.jpg'
import "./Torneo.css"

export default function Equipo() {
  return (
    // CAMBIO CLAVE:
    // En lugar de 'h-full' o 'h-screen', usamos un cálculo:
    // h-[calc(100vh-64px)] -> "100% de la pantalla MENOS 64 pixeles del menú"
    <div className="w-full h-[calc(100vh-80px)] overflow-hidden relative">
        
        <div className="h-full w-full holographic-container">
          <Link to="/torneos/ConsultarTorneos" className="block w-full h-full">
              <figure className="w-full aspect-[4/3] overflow-hidden relative holographic-card">
              
              <img 
                  src={libertadores} 
                  alt="Torneos" 
                  // object-cover recorta la imagen para que encaje perfecto
                  className="w-full h-full object-cover object-top" 
              />
              
              <div className="liquid-morph-container absolute inset-0 flex items-center justify-center pointer-events-none">
                <div className="liquid-morph-element pointer-events-auto">
                  <span>Torneos</span>
                </div>
              </div>
            </figure>
          </Link>
      </div>
    </div>
  )
}