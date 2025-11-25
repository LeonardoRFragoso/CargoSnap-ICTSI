import { Link, useLocation } from 'react-router-dom'
import { X, Home, FileText, Settings, LogOut, BarChart3 } from 'lucide-react'
import { useAuthStore } from '../../store/authStore'
import { cn } from '../../utils/cn'

const navigation = [
  { name: 'Dashboard', href: '/', icon: Home },
  { name: 'Inspeções', href: '/inspections', icon: FileText },
  { name: 'Analytics', href: '/analytics', icon: BarChart3 },
  { name: 'Configurações', href: '/settings', icon: Settings },
]

export default function Sidebar({ open, onClose }) {
  const location = useLocation()
  const { user, logout } = useAuthStore()

  const handleLogout = () => {
    logout()
    window.location.href = '/login'
  }

  const companyColors = {
    ICTSI: 'bg-ictsi-primary',
    ITRACKER: 'bg-itracker-primary',
    CLIA: 'bg-clia-primary',
  }

  const bgColor = companyColors[user?.company?.company_type] || 'bg-blue-600'

  return (
    <>
      {/* Mobile overlay */}
      {open && (
        <div className="fixed inset-0 z-40 bg-gray-600 bg-opacity-75 md:hidden" onClick={onClose} />
      )}

      {/* Sidebar */}
      <div className={cn(
        "fixed inset-y-0 left-0 w-64 transform transition-transform duration-300 ease-in-out md:relative md:translate-x-0 z-50",
        open ? "translate-x-0" : "-translate-x-full md:translate-x-0",
        bgColor
      )}>
        <div className="flex h-full flex-col safe-top safe-bottom">
          {/* Logo */}
          <div className="flex h-16 items-center justify-between px-6">
            <span className="text-2xl font-bold text-white">
              {user?.company?.name}
            </span>
            <button
              className="md:hidden text-white tap-target"
              onClick={onClose}
            >
              <X className="h-6 w-6" />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 space-y-1 px-3 py-4">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  onClick={onClose}
                  className={cn(
                    isActive
                      ? 'bg-white bg-opacity-20 text-white'
                      : 'text-white text-opacity-80 hover:bg-white hover:bg-opacity-10',
                    'group flex items-center px-3 py-3 text-base font-medium rounded-md tap-target'
                  )}
                >
                  <item.icon
                    className={cn(
                      isActive ? 'text-white' : 'text-white text-opacity-80',
                      'mr-3 h-6 w-6 flex-shrink-0'
                    )}
                  />
                  {item.name}
                </Link>
              )
            })}
          </nav>

          {/* User info and logout */}
          <div className="border-t border-white border-opacity-20 p-4">
            <div className="flex items-center mb-4">
              <div className="flex-shrink-0">
                <div className="h-10 w-10 rounded-full bg-white bg-opacity-20 flex items-center justify-center text-white font-bold">
                  {user?.first_name?.[0]}{user?.last_name?.[0]}
                </div>
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-white">{user?.full_name}</p>
                <p className="text-xs text-white text-opacity-80">{user?.role}</p>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="flex w-full items-center px-3 py-2 text-sm font-medium text-white text-opacity-80 hover:bg-white hover:bg-opacity-10 rounded-md tap-target"
            >
              <LogOut className="mr-3 h-5 w-5" />
              Sair
            </button>
          </div>
        </div>
      </div>
    </>
  )
}
