import './App.css'
import React, { Suspense } from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Navbar from './components/navbar/Navbar'
import Sidebar from './components/sidebar/Sidebar.tsx'
import Inicio from './components/inicio/Inicio.tsx'
import Cancha from './components/cancha/Cancha.tsx'
import ConsultarCanchaBasquet from './components/cancha/basquet/ConsultarCanchaBasquet.tsx'
import ModificarCanchaBasquet from './components/cancha/basquet/ModificarCanchaBasquet.tsx'
import RegistrarCanchaBasquet from './components/cancha/basquet/RegistrarCanchaBasquet.tsx'
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
                  <Route path="/canchas/basquet/RegistrarCancha" element={<RegistrarCanchaBasquet/>} />
                  {/* />
                  
                  <Route path="/canchas/basquet/eliminar" element={<EliminarCanchaBasquet/>} />
                  <Route path="/canchas/basquet/modificar" element={<ModificarCanchaBasquet/>} />
                  {/* Canchas de Padel */}
                  {/*<Route path="/canchas/padel" element={<CanchaPadel/>} />
                  <Route path="/canchas/padel/consulta" element={<ConsultarCanchaPadel/>} />
                  <Route path="/canchas/padel/crear" element={<CrearCanchaPadel/>} />
                  <Route path="/canchas/padel/eliminar" element={<EliminarCanchaPadel/>} />
                  <Route path="/canchas/padel/modificar" element={<ModificarCanchaPadel/>} />*/}
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
