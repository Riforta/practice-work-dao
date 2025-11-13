import messi from './messi_hd.jpg'
import curry from './curry_hs.jpg'
import tapia from './tapia.webp'
import  "./Inicio.css"

export default function Inicio() {
  return (
    <main className="h-screen">
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-0 auto-rows-[1fr] h-full holographic-container">
        <figure className="w-full h-full overflow-hidden holographic-card">
          <img src={messi} alt="Lionel Messi" className="w-full h-full object-cover" />
          <div className="liquid-morph-container">
            <div className="liquid-morph-element">
              <span>Canchas de Futbol</span>
            </div>
          </div>
        </figure>
        <figure className="w-full h-full overflow-hidden holographic-card">
          <img src={curry} alt="Stephen Curry" className="w-full h-full object-cover" />
          <div className="liquid-morph-container">
            <div className="liquid-morph-element">
              <span>Canchas de Basquet</span>
            </div>
          </div>
        </figure>
        <figure className="w-full h-full overflow-hidden holographic-card">
          <img src={tapia} alt="Tapia" className="w-full h-full object-cover" />
          <div className="liquid-morph-container">
            <div className="liquid-morph-element">
              <span>Canchas de Padel</span>
            </div>
          </div>
        </figure>
      </div>
    </main>
  )
}
