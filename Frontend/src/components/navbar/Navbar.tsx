'use client'

import { Link } from 'react-router-dom'
import { useModal } from '../../contexts/ModalContext'
import { useAuth } from '../../contexts/AuthContext'
import { Bars3Icon } from '@heroicons/react/24/outline'
import worldcup from './wc_si.png'

export default function Navbar() {
  const { openModal } = useModal()
  const { user, logout } = useAuth()

  return (
    <header className="bg-gray-900">
      <nav aria-label="Global" className="mx-auto relative flex max-w-7xl items-center justify-between p-6 lg:px-8">
        <div className="flex lg:flex-1 align-items-left">
          <a href="/" className="-ml-24 sm:-ml-0 p-0">
            <img
              alt=""
              src={worldcup}
              className="h-16 w-auto object-contain"
            />
          </a>
        </div>
        {/* Centered title */}
        <div className="absolute left-1/2 transform -translate-x-1/2">
          <Link to="/" className="pointer-events-auto">
            <span className="text-2xl md:text-3xl font-serif font-semibold text-white">DeporteX</span>
          </Link>
        </div>
        <div className="flex lg:hidden">
          <button
            type="button"
            onClick={() => openModal('login')}
            className="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-400"
          >
            <span className="sr-only">Open main menu</span>
            <Bars3Icon aria-hidden="true" className="h-6 w-6" />
          </button>
        </div>
        <div className="hidden lg:flex lg:flex-1 lg:justify-end items-center space-x-4">
          {user ? (
            <div className="flex items-center space-x-4">
              <span className="text-sm text-white/90">{user.nombre_usuario || user.email}</span>
              <button onClick={() => { logout() }} className="text-sm text-white/80 hover:underline">Cerrar sesión</button>
            </div>
          ) : (
            <>
              <button onClick={() => openModal('register')} className="text-sm font-medium text-white/90 hover:underline">Registrarse</button>
              <button onClick={() => openModal('login')} className="text-sm font-semibold text-white">Ingresar <span aria-hidden="true">&rarr;</span></button>
            </>
          )}
        </div>
      </nav>
    </header>
  )
}