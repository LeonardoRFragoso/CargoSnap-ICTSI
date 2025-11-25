import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import { Loader2 } from 'lucide-react'
import { authService } from '../../services/authService'
import { useAuthStore } from '../../store/authStore'

export default function Login() {
  const navigate = useNavigate()
  const setAuth = useAuthStore((state) => state.setAuth)
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  })

  const loginMutation = useMutation({
    mutationFn: ({ username, password }) => authService.login(username, password),
    onSuccess: (data) => {
      setAuth(data)
      navigate('/', { replace: true })
    },
    onError: (error) => {
      console.error('Login error:', error)
      alert(error.response?.data?.detail || 'Erro ao fazer login. Verifique suas credenciais.')
    },
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    loginMutation.mutate(formData)
  }

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }))
  }

  return (
    <div>
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900">CargoSnap ICTSI</h2>
        <p className="mt-2 text-sm text-gray-600">
          Sistema de Inspeção de Cargas
        </p>
      </div>

      <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
        <div className="space-y-4 rounded-md shadow-sm">
          <div>
            <label htmlFor="username" className="sr-only">
              Usuário
            </label>
            <input
              id="username"
              name="username"
              type="text"
              autoComplete="username"
              required
              className="relative block w-full appearance-none rounded-md border border-gray-300 px-3 py-3 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-blue-500 focus:outline-none focus:ring-blue-500 tap-target"
              placeholder="Usuário"
              value={formData.username}
              onChange={handleChange}
              disabled={loginMutation.isPending}
            />
          </div>
          <div>
            <label htmlFor="password" className="sr-only">
              Senha
            </label>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="current-password"
              required
              className="relative block w-full appearance-none rounded-md border border-gray-300 px-3 py-3 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-blue-500 focus:outline-none focus:ring-blue-500 tap-target"
              placeholder="Senha"
              value={formData.password}
              onChange={handleChange}
              disabled={loginMutation.isPending}
            />
          </div>
        </div>

        <div>
          <button
            type="submit"
            disabled={loginMutation.isPending}
            className="group relative flex w-full justify-center rounded-md border border-transparent bg-blue-600 py-3 px-4 text-sm font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed tap-target"
          >
            {loginMutation.isPending ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                Entrando...
              </>
            ) : (
              'Entrar'
            )}
          </button>
        </div>
      </form>
    </div>
  )
}
