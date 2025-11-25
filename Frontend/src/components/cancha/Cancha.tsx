
import { Link } from 'react-router-dom'
import cilindro from './imagenes/cilindro_hd.jpg'
import nba from './imagenes/nba_court_hd.jpg'
import padel from './imagenes/cancha_padel_hd.webp'
import "./Cancha.css"


// ...existing code...
export default function Cancha() {
  return (
    <main className="h-screen">
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-0 auto-rows-[1fr] h-full holographic-container">

        <Link to="/canchas/futbol" className="block w-full h-full">
          <figure className="w-full h-full overflow-hidden relative holographic-card">
            <img src={cilindro} alt="Canchas de Futbol" className="w-full h-full object-cover object-center" />
            <div className="liquid-morph-container absolute inset-0 flex items-center justify-center pointer-events-none">
              <div className="liquid-morph-element pointer-events-auto">
                <span>Canchas de Futbol</span>
              </div>
            </div>
          </figure>
        </Link>

        <Link to="/canchas/basquet" className="block w-full h-full">
          <figure className="w-full h-full overflow-hidden relative holographic-card">
            <img src={nba} alt="Canchas de Basquet" className="w-full h-full object-cover object-center" />
            <div className="liquid-morph-container absolute inset-0 flex items-center justify-center pointer-events-none">
              <div className="liquid-morph-element pointer-events-auto">
                <span>Canchas de Basquet</span>
              </div>
            </div>
          </figure>
        </Link>

        <Link to="/canchas/padel" className="block w-full h-full">
          <figure className="w-full h-full overflow-hidden relative holographic-card">
            <img src={padel} alt="Canchas de Padel" className="w-full h-full object-cover object-center" />
            <div className="liquid-morph-container absolute inset-0 flex items-center justify-center pointer-events-none">
              <div className="liquid-morph-element pointer-events-auto">
                <span>Canchas de Padel</span>
              </div>
            </div>
          </figure>
        </Link>
        
      </div>
    </main>
  )
}
