import React, { useEffect, useRef } from 'react'

type ModalProps = {
  open: boolean
  onClose: () => void
  children: React.ReactNode
}

export default function Modal({ open, onClose, children }: ModalProps) {
  const containerRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    if (!open) return

    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }
    document.addEventListener('keydown', onKey)

    // focus first input inside modal for accessibility
    const timer = setTimeout(() => {
      const el = containerRef.current?.querySelector('input,button,select,textarea') as HTMLElement | null
      if (el) el.focus()
    }, 50)

    return () => {
      clearTimeout(timer)
      document.removeEventListener('keydown', onKey)
    }
  }, [open, onClose])

  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center px-4">
      <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={onClose} />

      <div ref={containerRef} className="relative z-10 w-full max-w-md">
        <div className="transform transition-all duration-200 ease-out scale-100 opacity-100">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-2xl overflow-hidden">
            <div className="p-6">{children}</div>
          </div>
        </div>
      </div>
    </div>
  )
}
