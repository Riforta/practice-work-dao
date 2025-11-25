import "./Basquet.css"
import curry from './imagenes/curry_hd_si.jpg';



export default function Basquet() {
        return (
                                <div className="w-full h-screen bg-no-repeat bg-cover bg-center"
  					style={{ backgroundImage: `url(${curry})` }}>
                <div className="basquet-root">
                        <div className="image-wrapper">

                                <div className="left-buttons">
                                        <div className="liquid-morph-element pointer-events-auto ">
                                                <span className='left-btn'>Consultar canchas</span>
                                        </div>

										<div className="liquid-morph-element pointer-events-auto ">
                                                <span className='left-btn'>Registrar canchas</span>
                                        </div>

										<div className="liquid-morph-element pointer-events-auto ">
                                                <span className='left-btn'>Modificar canchas</span>
                                        </div>
										<div className="liquid-morph-element pointer-events-auto ">
                                                <span className='left-btn'>Eliminar canchas</span>
                                        </div>
                                </div>
                        </div>
                </div>
		</div>
        )
}
