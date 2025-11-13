import React, { createContext, useContext, useState } from 'react'
import Login from '../components/auth/Login'
import Register from '../components/auth/Register'
import Modal from '../components/ui/Modal'

type ModalName = 'login' | 'register' | null

type ModalContextShape = {
  openModal: (name: ModalName) => void
  closeModal: () => void
}

const ModalContext = createContext<ModalContextShape | undefined>(undefined)

export const useModal = (): ModalContextShape => {
  const ctx = useContext(ModalContext)
  if (!ctx) throw new Error('useModal must be used within ModalProvider')
  return ctx
}

export const ModalProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [modal, setModal] = useState<ModalName>(null)

  const openModal = (name: ModalName) => setModal(name)
  const closeModal = () => setModal(null)

  return (
    <ModalContext.Provider value={{ openModal, closeModal }}>
      {children}

      <Modal open={modal === 'login'} onClose={closeModal}>
        <Login />
      </Modal>

      <Modal open={modal === 'register'} onClose={closeModal}>
        <Register />
      </Modal>
    </ModalContext.Provider>
  )
}
