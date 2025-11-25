import { useAuthStore } from '../store/authStore'
import { User, Mail, Briefcase, Building } from 'lucide-react'

export default function Profile() {
  const { user } = useAuthStore()

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Meu Perfil</h1>

      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <div className="flex items-center mb-6">
            <div className="h-20 w-20 rounded-full bg-blue-600 flex items-center justify-center">
              <User className="h-10 w-10 text-white" />
            </div>
            <div className="ml-6">
              <h2 className="text-2xl font-bold text-gray-900">
                {user?.full_name}
              </h2>
              <p className="text-sm text-gray-500">{user?.role}</p>
            </div>
          </div>

          <div className="border-t border-gray-200 pt-6">
            <dl className="space-y-4">
              <div className="flex items-center">
                <User className="h-5 w-5 text-gray-400 mr-3" />
                <dt className="text-sm font-medium text-gray-500 w-32">Nome:</dt>
                <dd className="text-sm text-gray-900">{user?.full_name}</dd>
              </div>

              <div className="flex items-center">
                <Mail className="h-5 w-5 text-gray-400 mr-3" />
                <dt className="text-sm font-medium text-gray-500 w-32">Email:</dt>
                <dd className="text-sm text-gray-900">{user?.email}</dd>
              </div>

              <div className="flex items-center">
                <Briefcase className="h-5 w-5 text-gray-400 mr-3" />
                <dt className="text-sm font-medium text-gray-500 w-32">Função:</dt>
                <dd className="text-sm text-gray-900">{user?.role}</dd>
              </div>

              <div className="flex items-center">
                <Building className="h-5 w-5 text-gray-400 mr-3" />
                <dt className="text-sm font-medium text-gray-500 w-32">Empresa:</dt>
                <dd className="text-sm text-gray-900">{user?.company?.name}</dd>
              </div>
            </dl>
          </div>
        </div>
      </div>
    </div>
  )
}
