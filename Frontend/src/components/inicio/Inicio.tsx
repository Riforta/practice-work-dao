import messi from './messi_hd.jpg'
import curry from './curry_hs.jpg'
import tapia from './tapia.webp'
import tapia_hd from './tapia_salto_hd.jpg'
import messi_ch from './messi_ch_hd.jpg'
import night from './nightnight.jpg'
import  "./Inicio.css"

export default function Inicio() {
  return (
    <main className="h-screen">
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-0 auto-rows-[1fr] h-full holographic-container">

        <figure className="w-full h-full overflow-hidden holographic-card">
        <div className="card">
            <div className="card-inner">
                <div className="card-front"> <img src={messi} alt="Lionel Messi" className="w-full h-full object-cover" /> </div>
                <div className="card-back"><img src={messi_ch} alt="Lionel Messi" className="w-full h-full object-cover" /></div>
            </div>
        </div>
        <div className="liquid-morph-container">
            <div className="liquid-morph-element">
            <span>Canchas de Futbol</span>
            </div>
        </div>
        </figure>
        
        <figure className="w-full h-full overflow-hidden holographic-card">
        <div className="card">
            <div className="card-inner">
                <div className="card-front"> <img src={curry} alt="Stephen Curry" className="w-full h-full object-cover" /> </div>
                <div className="card-back"><img src={night} alt="Stephen Curry" className="w-full h-full object-cover" /></div>
            </div>
        </div>
          <div className="liquid-morph-container">
            <div className="liquid-morph-element">
              <span>Canchas de Basquet</span>
            </div>
          </div>
        </figure>

        <figure className="w-full h-full overflow-hidden holographic-card">
        <div className="card">
            <div className="card-inner">
                <div className="card-front"> <img src={tapia} alt="Agustin tapia" className="w-full h-full object-cover" /> </div>
                <div className="card-back"><img src={tapia_hd} alt="Agustin tapia" className="w-full h-full object-cover" /></div>
            </div>
        </div>
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
