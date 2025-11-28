'use client'

import { Link } from 'react-router-dom'
import { useModal } from '../../contexts/ModalContext'
import { useAuth } from '../../contexts/AuthContext'
import { Bars3Icon, UserCircleIcon, ArrowRightOnRectangleIcon } from '@heroicons/react/24/outline'
import worldcup from './wc_si.png'

export default function Navbar() {
  const { openModal } = useModal()
  const { user, logout } = useAuth()

  return (
    <header className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 border-b border-slate-700/50 shadow-lg">
      <nav aria-label="Global" className="mx-auto relative flex max-w-7xl items-center justify-between px-4 py-4 lg:px-8">
        {/* Logo */}
        <div className="flex items-center gap-3">
          <Link to="/" className="flex items-center gap-3 group">
            <div className="relative">
              <div className="absolute inset-0 bg-emerald-500/20 blur-xl rounded-full group-hover:bg-emerald-500/30 transition-all"></div>
              <img
                alt="DeporteX"
                src={worldcup}
                className="relative h-12 w-12 sm:h-14 sm:w-14 object-contain transform group-hover:scale-110 transition-transform duration-300"
              />
            </div>
            <span className="hidden sm:block text-2xl font-bold bg-gradient-to-r from-emerald-400 to-teal-400 bg-clip-text text-transparent">
              DeporteX
            </span>
          </Link>
        </div>

        {/* Mobile menu button */}
        <div className="flex lg:hidden">
          <button
            type="button"
            onClick={() => openModal('login')}
            className="inline-flex items-center justify-center rounded-lg p-2.5 text-slate-400 hover:bg-slate-800 hover:text-white transition-colors"
          >
            <span className="sr-only">Open main menu</span>
            <Bars3Icon aria-hidden="true" className="h-6 w-6" />
          </button>
        </div>

        {/* Desktop menu */}
        <div className="hidden lg:flex lg:items-center lg:gap-4">
          {user ? (
            <div className="flex items-center gap-4">
              {/* User info */}
              <div className="flex items-center gap-3 px-4 py-2 bg-slate-800/50 rounded-lg border border-slate-700/50">
                <UserCircleIcon className="h-6 w-6 text-emerald-400" />
                <span className="text-sm font-medium text-white">
                  {user.nombre_usuario || user.email}
                </span>
              </div>
              
              {/* Logout button */}
              <button 
                onClick={() => { logout() }} 
                className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-slate-300 hover:text-white bg-slate-800/50 hover:bg-red-500/20 border border-slate-700/50 hover:border-red-500/50 rounded-lg transition-all duration-200"
              >
                <ArrowRightOnRectangleIcon className="h-5 w-5" />
                <span>Cerrar sesión</span>
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-3">
              {/* Register button */}
              <button 
                onClick={() => openModal('register')} 
                className="flex items-center justify-center gap-2 px-5 py-2.5 text-sm font-semibold text-slate-300 hover:text-white bg-slate-800/50 hover:bg-slate-700/80 border border-slate-700 hover:border-slate-600 rounded-lg transition-all duration-200 min-w-[140px]"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                </svg>
                <span>Registrarse</span>
              </button>

              {/* Login button */}
              <button 
                onClick={() => openModal('login')} 
                className="flex items-center justify-center gap-2 px-5 py-2.5 text-sm font-semibold text-white bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 rounded-lg shadow-lg hover:shadow-xl transform hover:scale-[1.02] transition-all duration-200 min-w-[140px]"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                </svg>
                <span>Ingresar</span>
              </button>
            </div>
          )}
        </div>
      </nav>
    </header>
  )
}