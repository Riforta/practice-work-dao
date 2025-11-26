import './App.css'
import React, { Suspense } from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Navbar from './components/navbar/Navbar'
import Sidebar from './components/sidebar/Sidebar.tsx'
import Inicio from './components/inicio/Inicio.tsx'
import Cancha from './components/cancha/Cancha.tsx'
import ConsultarCanchaBasquet from './components/cancha/basquet/ConsultarCanchaBasquet.tsx'
import ModificarCanchaBasquet from './components/cancha/basquet/ModificarCanchaBasquet.tsx'
import ConsultarServicios from './components/servicios/ConsultarServicios.tsx'
import RegistrarServicios from './components/servicios/RegistrarServicios.tsx'
import ModificarServicios from './components/servicios/ModificarServicios.tsx'
import ConsultarTurnos from './components/turnos/ConsultarTurnos.tsx'
import RegistrarTurnos from './components/turnos/RegistrarTurnos.tsx'
import ModificarTurnos from './components/turnos/ModificarTurnos.tsx'
import { ModalProvider } from './contexts/ModalContext'
import { AuthProvider } from './contexts/AuthContext'


const Login = React.lazy(() => import('./components/auth/Login'))
const Register = React.lazy(() => import('./components/auth/Register'))

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <ModalProvider>
        <div className="min-h-screen flex flex-col">
          <Navbar />

          <div className="flex flex-1">
            {/* Sidebar */}
            <aside className="hidden lg:block">
              <Sidebar />
            </aside>

            {/* Main content area */}
            <main className="flex-1">
              <Suspense fallback={<div className="p-6">Cargando...</div>}>
                <Routes>
                  {/* Inicio  */}
                  <Route path="/" element={<Inicio />} />
                  {/* login y register */}
                  <Route path="/login" element={<Login />} />
                  <Route path="/register" element={<Register />} />
                  {/* Cancha */}
                  <Route path="/canchas" element={<Cancha/>} />
                  {/* Canchas de Futbol */}
                  {/*<Route path="/canchas/futbol" element={<CanchaFutbol/>} />
                  <Route path="/canchas/futbol/consulta" element={<ConsultarCanchaFutbol/>} />
                  <Route path="/canchas/futbol/crear" element={<CrearCanchaFutbol/>} />
                  <Route path="/canchas/futbol/eliminar" element={<EliminarCanchaFutbol/>} />
                  <Route path="/canchas/futbol/modificar" element={<ModificarCanchaFutbol/>} />
                  {/* Canchas de Basquet */}
                  <Route path="/canchas/basquet" element={<ConsultarCanchaBasquet/>} />
                  <Route path="/canchas/basquet/ModificarCanchaBasquet/:id" element={<ModificarCanchaBasquet/>} />
                  {/* />
                  <Route path="/canchas/basquet/crear" element={<CrearCanchaBasquet/>} />
                  <Route path="/canchas/basquet/eliminar" element={<EliminarCanchaBasquet/>} />
                  <Route path="/canchas/basquet/modificar" element={<ModificarCanchaBasquet/>} />
                  {/* Canchas de Padel */}
                  {/*<Route path="/canchas/padel" element={<CanchaPadel/>} />
                  <Route path="/canchas/padel/consulta" element={<ConsultarCanchaPadel/>} />
                  <Route path="/canchas/padel/crear" element={<CrearCanchaPadel/>} />
                  <Route path="/canchas/padel/eliminar" element={<EliminarCanchaPadel/>} />
                  <Route path="/canchas/padel/modificar" element={<ModificarCanchaPadel/>} />*/}
                  {/* Servicios adicionales */}
                  <Route path="/servicios" element={<ConsultarServicios />} />
                  <Route path="/servicios/nuevo" element={<RegistrarServicios />} />
                  <Route path="/servicios/:id/editar" element={<ModificarServicios />} />
                  {/* Turnos */}
                  <Route path="/turnos" element={<ConsultarTurnos />} />
                  <Route path="/turnos/nuevo" element={<RegistrarTurnos />} />
                  <Route path="/turnos/:id/editar" element={<ModificarTurnos />} />
                </Routes>
              </Suspense>
            </main>
          </div>
        </div>
        </ModalProvider>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App
