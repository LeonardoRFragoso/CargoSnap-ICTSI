import { Outlet, Navigate } from 'react-router-dom'
import { useAuthStore } from '../../store/authStore'

export default function AuthLayout() {
  const { isAuthenticated } = useAuthStore()

  if (isAuthenticated) {
    return <Navigate to="/" replace />
  }

  return (
    <div 
      className="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 relative"
      style={{
        backgroundImage: 'url(/bg-login.png)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat'
      }}
    >
      {/* Overlay branco translúcido */}
      <div className="absolute inset-0 bg-white/85 z-0"></div>
      
      {/* Conteúdo */}
      <div className="max-w-md w-full space-y-8 relative z-10 bg-white p-8 rounded-lg shadow-xl">
        <Outlet />
      </div>
    </div>
  )
}
