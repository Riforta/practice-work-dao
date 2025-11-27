import React, { createContext, useContext, useEffect, useState } from 'react'
import { logout as logoutService } from '../services/auth.service'

type User = any

type AuthShape = {
  user: User | null
  token: string | null
  setAuth: (token: string | null, user: User | null) => void
  logout: () => void
}

const AuthContext = createContext<AuthShape | undefined>(undefined)

export const useAuth = () => {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('token'))
  const [user, setUser] = useState<User | null>(() => {
    const raw = localStorage.getItem('user')
    return raw ? JSON.parse(raw) : null
  })

  useEffect(() => {
    if (token) localStorage.setItem('token', token)
    else localStorage.removeItem('token')
  }, [token])

  useEffect(() => {
    if (user) localStorage.setItem('user', JSON.stringify(user))
    else localStorage.removeItem('user')
  }, [user])

  const setAuth = (t: string | null, u: User | null) => {
    setToken(t)
    setUser(u)
  }

  const logout = async () => {
    await logoutService(token)
    setToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, token, setAuth, logout }}>{children}</AuthContext.Provider>
  )
}
