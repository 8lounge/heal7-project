'use client'

import * as React from "react"

interface ToastProps {
  title?: string
  description?: string
  variant?: 'default' | 'destructive'
}

const toastVariants = {
  default: 'bg-white border border-gray-200 text-gray-900',
  destructive: 'bg-red-500 border border-red-600 text-white'
}

export function Toaster() {
  const [toasts, setToasts] = React.useState<ToastProps[]>([])

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2">
      {toasts.map((toast, index) => (
        <div
          key={index}
          className={`px-4 py-3 rounded-md shadow-lg ${toastVariants[toast.variant || 'default']}`}
        >
          {toast.title && <div className="font-semibold">{toast.title}</div>}
          {toast.description && <div className="text-sm">{toast.description}</div>}
        </div>
      ))}
    </div>
  )
}

export { type ToastProps }