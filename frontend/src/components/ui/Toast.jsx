import { useEffect } from 'react'
import { X, CheckCircle, AlertCircle, Info, AlertTriangle } from 'lucide-react'

/**
 * Toast Component
 * Displays notification messages with different types
 */
export default function Toast({ message, type = 'info', onClose, duration = 5000 }) {
  useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(() => {
        onClose()
      }, duration)
      
      return () => clearTimeout(timer)
    }
  }, [duration, onClose])

  const icons = {
    success: <CheckCircle className="h-5 w-5 text-green-500" />,
    error: <AlertCircle className="h-5 w-5 text-red-500" />,
    warning: <AlertTriangle className="h-5 w-5 text-yellow-500" />,
    info: <Info className="h-5 w-5 text-blue-500" />,
  }

  const bgColors = {
    success: 'bg-green-50 border-green-200',
    error: 'bg-red-50 border-red-200',
    warning: 'bg-yellow-50 border-yellow-200',
    info: 'bg-blue-50 border-blue-200',
  }

  const textColors = {
    success: 'text-green-800',
    error: 'text-red-800',
    warning: 'text-yellow-800',
    info: 'text-blue-800',
  }

  return (
    <div className={`fixed top-4 right-4 z-50 max-w-md w-full animate-slide-in-right`}>
      <div className={`flex items-start p-4 rounded-lg border shadow-lg ${bgColors[type]}`}>
        <div className="flex-shrink-0">
          {icons[type]}
        </div>
        <div className={`ml-3 flex-1 ${textColors[type]}`}>
          <p className="text-sm font-medium">{message}</p>
        </div>
        <button
          onClick={onClose}
          className={`ml-3 flex-shrink-0 inline-flex ${textColors[type]} hover:opacity-75 focus:outline-none`}
        >
          <X className="h-5 w-5" />
        </button>
      </div>
    </div>
  )
}
