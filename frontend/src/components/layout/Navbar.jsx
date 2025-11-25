import { Bell, User, Home, FileText, BarChart3, Settings, LogOut, ChevronDown, Container } from 'lucide-react'
import { useAuthStore } from '../../store/authStore'
import { Link, useLocation } from 'react-router-dom'
import { useState } from 'react'
import { cn } from '../../utils/cn'

const navigation = [
  { name: 'Dashboard', href: '/', icon: Home },
  { name: 'Inspeções', href: '/inspections', icon: FileText },
  { name: 'CargoSnap', href: '/cargosnap', icon: Container },
  { name: 'Analytics', href: '/analytics', icon: BarChart3 },
  { name: 'Configurações', href: '/settings', icon: Settings },
]

export default function Navbar() {
  const { user, logout } = useAuthStore()
  const location = useLocation()
  const [userMenuOpen, setUserMenuOpen] = useState(false)

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
    <nav className={cn("flex h-16 w-full flex-shrink-0 shadow-lg z-20", bgColor)}>
      <div className="max-w-[1600px] mx-auto w-full flex items-center justify-between px-6">
        {/* Logo e Nome */}
        <div className="flex items-center gap-8">
          <Link to="/" className="flex items-center gap-3">
            <h1 className="text-2xl font-bold text-white">
              {user?.company?.name || 'CargoSnap'}
            </h1>
          </Link>
          
          {/* Navigation Links - Desktop */}
          <div className="hidden md:flex items-center gap-1">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={cn(
                    "flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200",
                    isActive
                      ? 'bg-white/20 text-white shadow-lg'
                      : 'text-white/80 hover:bg-white/10 hover:text-white'
                  )}
                >
                  <item.icon className="h-4 w-4" />
                  {item.name}
                </Link>
              )
            })}
          </div>
        </div>
        
        {/* Right Side - Notifications & User Menu */}
        <div className="flex items-center gap-4">
          {/* Notifications */}
          <button className="relative rounded-full p-2 text-white/80 hover:text-white hover:bg-white/10 transition-all tap-target">
            <span className="sr-only">Notificações</span>
            <Bell className="h-5 w-5" />
            <span className="absolute top-1 right-1 h-2 w-2 bg-red-500 rounded-full"></span>
          </button>
          
          {/* User Menu */}
          <div className="relative">
            <button
              onClick={() => setUserMenuOpen(!userMenuOpen)}
              className="flex items-center gap-3 rounded-lg px-3 py-2 text-white hover:bg-white/10 transition-all tap-target"
            >
              {user?.avatar ? (
                <img
                  className="h-8 w-8 rounded-full ring-2 ring-white/20"
                  src={user.avatar}
                  alt={user.full_name}
                />
              ) : (
                <div className="h-8 w-8 rounded-full bg-white/20 flex items-center justify-center ring-2 ring-white/20">
                  <User className="h-5 w-5 text-white" />
                </div>
              )}
              <div className="hidden md:block text-left">
                <p className="text-sm font-semibold">{user?.first_name || user?.username}</p>
                <p className="text-xs text-white/70">{user?.role}</p>
              </div>
              <ChevronDown className={cn(
                "h-4 w-4 transition-transform duration-200",
                userMenuOpen && "rotate-180"
              )} />
            </button>
            
            {/* Dropdown Menu */}
            {userMenuOpen && (
              <>
                <div 
                  className="fixed inset-0 z-10" 
                  onClick={() => setUserMenuOpen(false)}
                />
                <div className="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-xl border border-gray-200 py-2 z-20">
                  <Link
                    to="/profile"
                    className="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                    onClick={() => setUserMenuOpen(false)}
                  >
                    <User className="h-4 w-4" />
                    Meu Perfil
                  </Link>
                  <Link
                    to="/settings"
                    className="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                    onClick={() => setUserMenuOpen(false)}
                  >
                    <Settings className="h-4 w-4" />
                    Configurações
                  </Link>
                  <hr className="my-2 border-gray-200" />
                  <button
                    onClick={handleLogout}
                    className="flex items-center gap-3 px-4 py-2.5 text-sm text-red-600 hover:bg-red-50 transition-colors w-full text-left"
                  >
                    <LogOut className="h-4 w-4" />
                    Sair
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}
