import './App.css'
import React, { Suspense } from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Navbar from './components/navbar/Navbar'
import Sidebar from './components/sidebar/Sidebar.tsx'
import Inicio from './components/inicio/Inicio.tsx'
import CanchasPublicas from './components/inicio/CanchasPublicas.tsx'
import Cancha from './components/cancha/Cancha.tsx'
import ConsultarCanchaBasquet from './components/cancha/basquet/ConsultarCanchaBasquet.tsx'
import ModificarCanchaBasquet from './components/cancha/basquet/ModificarCanchaBasquet.tsx'
import RegistrarCanchaBasquet from './components/cancha/basquet/RegistrarCanchaBasquet.tsx'
import ConsultarCanchaFutbol from './components/cancha/futbol/ConsultarCanchaFutbol.tsx'
import ModificarCanchaFutbol from './components/cancha/futbol/ModificarCanchaFutbol.tsx'
import RegistrarCanchaFutbol from './components/cancha/futbol/RegistrarCanchaFutbol.tsx'
import ConsultarCanchaPadel from './components/cancha/padel/ConsultarCanchaPadel.tsx'
import ModificarCanchaPadel from './components/cancha/padel/ModificarCanchaPadel.tsx'
import RegistrarCanchaPadel from './components/cancha/padel/RegistrarCanchaPadel.tsx'
import Equipo from './components/equipo/Equipo.tsx'
import ConsultarEquipo from './components/equipo/ConsultarEquipo.tsx'
import ModificarEquipo from './components/equipo/ModificarEquipo.tsx'
import RegistrarEquipo from './components/equipo/RegistrarEquipo.tsx'
import ConsultarServicios from './components/servicios/ConsultarServicios.tsx'
import RegistrarServicios from './components/servicios/RegistrarServicios.tsx'
import ModificarServicios from './components/servicios/ModificarServicios.tsx'
import ConsultarTurnos from './components/turnos/ConsultarTurnos.tsx'
import RegistrarTurnos from './components/turnos/RegistrarTurnos.tsx'
import ModificarTurnos from './components/turnos/ModificarTurnos.tsx'
import ReservasCliente from './components/turnos/ReservasCliente.tsx'
import MisReservas from './components/turnos/MisReservas.tsx'
import PagoReserva from './components/turnos/PagoReserva.tsx'
import Torneo from './components/torneo/Torneo.tsx'
import ConsultarTorneo from './components/torneo/ConsultarTorneo.tsx'
import RegistrarTorneo from './components/torneo/RegistrarTorneo.tsx'
import ModificarTorneo from './components/torneo/ModificarTorneo.tsx'
import ConsultarPagos from './components/pagos/ConsultarPagos.tsx'
import RegistrarPago from './components/pagos/RegistrarPago.tsx'
import ConsultarClientes from './components/clientes/ConsultarClientes.tsx'
import RegistrarCliente from './components/clientes/RegistrarCliente.tsx'
import ModificarCliente from './components/clientes/ModificarCliente.tsx'
import { ModalProvider } from './contexts/ModalContext'
import { AuthProvider } from './contexts/AuthContext'
import ProtectedRoute from './components/common/ProtectedRoute.tsx'


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
                  {/* Rutas públicas (sin autenticación) */}
                  <Route path="/" element={<Inicio />} />
                  <Route path="/login" element={<Login />} />
                  <Route path="/register" element={<Register />} />
                  <Route path="/canchas-publicas" element={<CanchasPublicas />} />
                  
                  {/* Rutas de cliente (requieren autenticación) */}
                  <Route path="/mis-reservas" element={
                    <ProtectedRoute requireAuth>
                      <MisReservas />
                    </ProtectedRoute>
                  } />
                  <Route path="/reservas/pago" element={
                    <ProtectedRoute requireAuth>
                      <PagoReserva />
                    </ProtectedRoute>
                  } />
                  
                  {/* Rutas de administrador (requieren rol admin) */}
                  <Route path="/reservas" element={
                    <ProtectedRoute requireAdmin>
                      <ReservasCliente />
                    </ProtectedRoute>
                  } />
                  
                  {/* Cancha - Admin */}
                  <Route path="/canchas" element={
                    <ProtectedRoute requireAdmin>
                      <Cancha/>
                    </ProtectedRoute>
                  } />
                  
                  {/* Canchas de Futbol - Admin */}
                  <Route path="/canchas/futbol" element={
                    <ProtectedRoute requireAdmin>
                      <ConsultarCanchaFutbol/>
                    </ProtectedRoute>
                  } />
                  <Route path="/canchas/futbol/RegistrarCancha" element={
                    <ProtectedRoute requireAdmin>
                      <RegistrarCanchaFutbol/>
                    </ProtectedRoute>
                  } />
                  <Route path="/canchas/futbol/ModificarCanchaFutbol/:id" element={
                    <ProtectedRoute requireAdmin>
                      <ModificarCanchaFutbol/>
                    </ProtectedRoute>
                  } />
                  
                  {/* Canchas de Basquet - Admin */}
                  <Route path="/canchas/basquet" element={
                    <ProtectedRoute requireAdmin>
                      <ConsultarCanchaBasquet/>
                    </ProtectedRoute>
                  } />
                  <Route path="/canchas/basquet/ModificarCanchaBasquet/:id" element={
                    <ProtectedRoute requireAdmin>
                      <ModificarCanchaBasquet/>
                    </ProtectedRoute>
                  } />
                  <Route path="/canchas/basquet/RegistrarCancha" element={
                    <ProtectedRoute requireAdmin>
                      <RegistrarCanchaBasquet/>
                    </ProtectedRoute>
                  } />
                  
                  {/* Canchas de Padel - Admin */}
                  <Route path="/canchas/padel" element={
                    <ProtectedRoute requireAdmin>
                      <ConsultarCanchaPadel/>
                    </ProtectedRoute>
                  } />
                  <Route path="/canchas/padel/RegistrarCancha" element={
                    <ProtectedRoute requireAdmin>
                      <RegistrarCanchaPadel/>
                    </ProtectedRoute>
                  } />
                  <Route path="/canchas/padel/ModificarCanchaPadel/:id" element={
                    <ProtectedRoute requireAdmin>
                      <ModificarCanchaPadel/>
                    </ProtectedRoute>
                  } />
                  
                  {/* Equipo - Admin */}
                  <Route path="/equipos" element={
                    <ProtectedRoute requireAdmin>
                      <Equipo/>
                    </ProtectedRoute>
                  } />
                  <Route path="/equipos/ConsultarEquipo" element={
                    <ProtectedRoute requireAdmin>
                      <ConsultarEquipo/>
                    </ProtectedRoute>
                  } />
                  <Route path="/equipos/RegistrarEquipo" element={
                    <ProtectedRoute requireAdmin>
                      <RegistrarEquipo/>
                    </ProtectedRoute>
                  } />
                  <Route path="/equipos/ModificarEquipo/:id" element={
                    <ProtectedRoute requireAdmin>
                      <ModificarEquipo/>
                    </ProtectedRoute>
                  } />
                  
                  {/* Servicios adicionales - Admin */}
                  <Route path="/servicios" element={
                    <ProtectedRoute requireAdmin>
                      <ConsultarServicios />
                    </ProtectedRoute>
                  } />
                  <Route path="/servicios/nuevo" element={
                    <ProtectedRoute requireAdmin>
                      <RegistrarServicios />
                    </ProtectedRoute>
                  } />
                  <Route path="/servicios/:id/editar" element={
                    <ProtectedRoute requireAdmin>
                      <ModificarServicios />
                    </ProtectedRoute>
                  } />
                  
                  {/* Torneos - Admin */}
                  <Route path="/torneos" element={
                    <ProtectedRoute requireAdmin>
                      <Torneo/>
                    </ProtectedRoute>
                  } />
                  <Route path="/torneos/ConsultarTorneos" element={
                    <ProtectedRoute requireAdmin>
                      <ConsultarTorneo/>
                    </ProtectedRoute>
                  } />
                  <Route path="/torneos/RegistrarTorneo" element={
                    <ProtectedRoute requireAdmin>
                      <RegistrarTorneo/>
                    </ProtectedRoute>
                  } />
                  <Route path="/torneos/ModificarTorneo/:id" element={
                    <ProtectedRoute requireAdmin>
                      <ModificarTorneo/>
                    </ProtectedRoute>
                  } />
                  
                  {/* Turnos - Admin */}
                  <Route path="/turnos" element={
                    <ProtectedRoute requireAdmin>
                      <ConsultarTurnos />
                    </ProtectedRoute>
                  } />
                  <Route path="/turnos/nuevo" element={
                    <ProtectedRoute requireAdmin>
                      <RegistrarTurnos />
                    </ProtectedRoute>
                  } />
                  <Route path="/turnos/:id/editar" element={
                    <ProtectedRoute requireAdmin>
                      <ModificarTurnos />
                    </ProtectedRoute>
                  } />
                  
                  {/* Pagos - Admin */}
                  <Route path="/pagos" element={
                    <ProtectedRoute requireAdmin>
                      <ConsultarPagos />
                    </ProtectedRoute>
                  } />
                  <Route path="/pagos/registrar" element={
                    <ProtectedRoute requireAdmin>
                      <RegistrarPago />
                    </ProtectedRoute>
                  } />
                  
                  {/* Clientes - Admin */}
                  <Route path="/clientes" element={
                    <ProtectedRoute requireAdmin>
                      <ConsultarClientes />
                    </ProtectedRoute>
                  } />
                  <Route path="/clientes/registrar" element={
                    <ProtectedRoute requireAdmin>
                      <RegistrarCliente />
                    </ProtectedRoute>
                  } />
                  <Route path="/clientes/modificar/:id" element={
                    <ProtectedRoute requireAdmin>
                      <ModificarCliente />
                    </ProtectedRoute>
                  } />
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
