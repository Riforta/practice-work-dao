import './App.css'
import React, { Suspense } from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Navbar from './components/navbar/Navbar'
import Sidebar from './components/sidebar/Sidebar.tsx'
import Inicio from './components/inicio/Inicio.tsx'
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
                  <Route path="/login" element={<Login />} />
                  <Route path="/register" element={<Register />} />
                  <Route path="/" element={<Inicio />} />
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
