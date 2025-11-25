import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import { useQuery } from '@tanstack/react-query'
import { Package, FileText, CheckCircle, Clock, AlertTriangle, TrendingUp, TrendingDown, Calendar, Users, ArrowRight, Plus } from 'lucide-react'
import api from '../services/api'
import PageContainer from '../components/layout/PageContainer'
import Card from '../components/layout/Card'
import EmptyState from '../components/layout/EmptyState'
import Button from '../components/ui/Button'

export default function Dashboard() {
  const navigate = useNavigate()
  const { user } = useAuthStore()

  // Buscar estatísticas da API
  const { data: dashboardStats, isLoading } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: async () => {
      try {
        const response = await api.get('/analytics/analytics/dashboard/')
        return response.data
      } catch (error) {
        // Endpoint não implementado, retornar dados mock
        console.log('Analytics endpoint not available, using mock data')
        return {
          total_inspections: 0,
          pending_inspections: 0,
          completed_inspections: 0,
          total_issues: 0
        }
      }
    },
  })

  // Buscar inspeções recentes
  const { data: recentInspections } = useQuery({
    queryKey: ['recent-inspections'],
    queryFn: async () => {
      const response = await api.get('/inspections/inspections/?ordering=-created_at&limit=5')
      return response.data.results || []
    },
  })

  const stats = [
    {
      name: 'Total de Inspeções',
      value: dashboardStats?.total_inspections || '0',
      icon: Package,
      color: 'bg-blue-500',
      trend: '+12%',
      trendUp: true,
    },
    {
      name: 'Pendentes',
      value: dashboardStats?.pending_inspections || '0',
      icon: Clock,
      color: 'bg-yellow-500',
      trend: '-5%',
      trendUp: false,
    },
    {
      name: 'Concluídas',
      value: dashboardStats?.completed_inspections || '0',
      icon: CheckCircle,
      color: 'bg-green-500',
      trend: '+18%',
      trendUp: true,
    },
    {
      name: 'Ocorrências',
      value: dashboardStats?.total_issues || '0',
      icon: AlertTriangle,
      color: 'bg-red-500',
      trend: '-3%',
      trendUp: false,
    },
  ]

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-blue-200 border-t-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600 font-medium">Carregando dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <PageContainer>
      <div className="space-y-8">
      {/* Header com gradiente aprimorado */}
      <div className="relative bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 rounded-2xl shadow-2xl p-8 text-white overflow-hidden">
        {/* Padrão de fundo decorativo */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 right-0 w-64 h-64 bg-white rounded-full blur-3xl transform translate-x-32 -translate-y-32"></div>
          <div className="absolute bottom-0 left-0 w-96 h-96 bg-blue-400 rounded-full blur-3xl transform -translate-x-48 translate-y-48"></div>
        </div>
        
        <div className="relative z-10">
          <h1 className="text-4xl font-bold mb-3 tracking-tight">
            Bem-vindo, {user?.first_name || user?.username}! 👋
          </h1>
          <div className="flex flex-col sm:flex-row sm:items-center gap-3 text-blue-50">
            <p className="flex items-center gap-2 text-base">
              <Users className="h-5 w-5" />
              <span className="font-medium">{user?.company?.name}</span>
              <span className="opacity-60">•</span>
              <span className="px-2.5 py-0.5 bg-white/20 rounded-full text-sm font-medium">{user?.role}</span>
            </p>
          </div>
          <p className="mt-2 text-sm text-blue-100 flex items-center gap-2">
            <Calendar className="h-4 w-4" />
            {new Date().toLocaleDateString('pt-BR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
          </p>
        </div>
      </div>

      {/* Stats Grid com design aprimorado */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat, index) => (
          <div
            key={stat.name}
            className="group relative overflow-hidden rounded-xl bg-white p-6 shadow-md hover:shadow-2xl transition-all duration-300 border border-gray-100 hover:border-gray-200 hover:-translate-y-1"
            style={{ animationDelay: `${index * 100}ms` }}
          >
            {/* Gradiente de fundo sutil no hover */}
            <div className="absolute inset-0 bg-gradient-to-br from-gray-50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            
            <div className="relative">
              <div className="flex items-start justify-between mb-4">
                <div className={`rounded-xl p-3 ${stat.color} shadow-lg group-hover:scale-110 transition-transform duration-300`}>
                  <stat.icon className="h-6 w-6 text-white" />
                </div>
                <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold ${
                  stat.trendUp 
                    ? 'bg-green-50 text-green-700 border border-green-200' 
                    : 'bg-red-50 text-red-700 border border-red-200'
                }`}>
                  {stat.trendUp ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
                  {stat.trend}
                </span>
              </div>
              
              <div>
                <p className="text-sm font-medium text-gray-600 mb-1">
                  {stat.name}
                </p>
                <p className="text-3xl font-bold text-gray-900 tracking-tight">
                  {stat.value}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Recent Inspections com header aprimorado */}
      <div className="bg-white shadow-lg rounded-xl overflow-hidden border border-gray-100">
        <div className="px-6 py-5 border-b border-gray-200 bg-gradient-to-r from-gray-50 to-white">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-gray-900 flex items-center gap-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Package className="h-5 w-5 text-blue-600" />
              </div>
              Inspeções Recentes
            </h2>
            <button 
              onClick={() => navigate('/inspections')}
              className="text-sm text-blue-600 hover:text-blue-700 font-medium flex items-center gap-1 hover:gap-2 transition-all"
            >
              Ver todas
              <ArrowRight className="h-4 w-4" />
            </button>
          </div>
        </div>
        <div className="overflow-x-auto">
          {recentInspections && recentInspections.length > 0 ? (
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                    Referência
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                    Título
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                    Data
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                    Ações
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-100">
                {recentInspections.map((inspection) => (
                  <tr key={inspection.id} className="hover:bg-blue-50/50 transition-colors duration-150">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm font-semibold text-gray-900">
                        {inspection.reference_number}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm text-gray-700">
                        {inspection.title || 'Sem título'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        inspection.status === 'COMPLETED' ? 'bg-green-100 text-green-700 border border-green-200' :
                        inspection.status === 'IN_PROGRESS' ? 'bg-yellow-100 text-yellow-700 border border-yellow-200' :
                        'bg-gray-100 text-gray-700 border border-gray-200'
                      }`}>
                        {inspection.status === 'COMPLETED' ? '✓ Concluída' :
                         inspection.status === 'IN_PROGRESS' ? '⏳ Em Progresso' :
                         '📝 Rascunho'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      {new Date(inspection.created_at).toLocaleDateString('pt-BR')}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button 
                        onClick={() => navigate(`/inspections/${inspection.id}`)}
                        className="text-blue-600 hover:text-blue-800 font-semibold flex items-center gap-1 hover:gap-2 transition-all"
                      >
                        Ver detalhes
                        <ArrowRight className="h-4 w-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="px-6 py-16 text-center">
              <div className="max-w-sm mx-auto">
                {/* Ilustração melhorada do estado vazio */}
                <div className="relative mb-6">
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="w-24 h-24 bg-blue-100 rounded-full animate-pulse"></div>
                  </div>
                  <div className="relative">
                    <Package className="mx-auto h-16 w-16 text-blue-400" strokeWidth={1.5} />
                  </div>
                </div>
                
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  Nenhuma inspeção encontrada
                </h3>
                <p className="text-sm text-gray-500 mb-6">
                  Comece criando sua primeira inspeção de container
                </p>
                
                <button 
                  onClick={() => navigate('/inspections/new')}
                  className="inline-flex items-center gap-2 px-6 py-3 border border-transparent text-sm font-semibold rounded-lg shadow-lg text-white bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 transform hover:scale-105 transition-all duration-200"
                >
                  <Plus className="h-5 w-5" />
                  Nova Inspeção
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Quick Actions com design aprimorado */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
        <button 
          onClick={() => navigate('/inspections/new')}
          className="group relative bg-white p-7 rounded-xl shadow-md hover:shadow-2xl transition-all duration-300 border border-gray-100 hover:border-blue-200 text-left overflow-hidden hover:-translate-y-1"
        >
          {/* Gradiente de fundo no hover */}
          <div className="absolute inset-0 bg-gradient-to-br from-blue-50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          
          <div className="relative">
            <div className="inline-flex p-3 bg-blue-100 rounded-xl mb-4 group-hover:scale-110 group-hover:bg-blue-600 transition-all duration-300">
              <Package className="h-7 w-7 text-blue-600 group-hover:text-white transition-colors duration-300" />
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-2 group-hover:text-blue-700 transition-colors">
              Nova Inspeção
            </h3>
            <p className="text-sm text-gray-600 mb-3">
              Criar uma nova inspeção de container
            </p>
            <div className="flex items-center text-blue-600 font-semibold text-sm group-hover:gap-2 transition-all">
              Começar agora
              <ArrowRight className="h-4 w-4 ml-1 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>
        </button>
        
        <button className="group relative bg-white p-7 rounded-xl shadow-md hover:shadow-2xl transition-all duration-300 border border-gray-100 hover:border-green-200 text-left overflow-hidden hover:-translate-y-1">
          <div className="absolute inset-0 bg-gradient-to-br from-green-50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          
          <div className="relative">
            <div className="inline-flex p-3 bg-green-100 rounded-xl mb-4 group-hover:scale-110 group-hover:bg-green-600 transition-all duration-300">
              <FileText className="h-7 w-7 text-green-600 group-hover:text-white transition-colors duration-300" />
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-2 group-hover:text-green-700 transition-colors">
              Relatórios
            </h3>
            <p className="text-sm text-gray-600 mb-3">
              Gerar e visualizar relatórios
            </p>
            <div className="flex items-center text-green-600 font-semibold text-sm group-hover:gap-2 transition-all">
              Acessar relatórios
              <ArrowRight className="h-4 w-4 ml-1 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>
        </button>
        
        <button className="group relative bg-white p-7 rounded-xl shadow-md hover:shadow-2xl transition-all duration-300 border border-gray-100 hover:border-red-200 text-left overflow-hidden hover:-translate-y-1">
          <div className="absolute inset-0 bg-gradient-to-br from-red-50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          
          <div className="relative">
            <div className="inline-flex p-3 bg-red-100 rounded-xl mb-4 group-hover:scale-110 group-hover:bg-red-600 transition-all duration-300">
              <AlertTriangle className="h-7 w-7 text-red-600 group-hover:text-white transition-colors duration-300" />
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-2 group-hover:text-red-700 transition-colors">
              Ocorrências
            </h3>
            <p className="text-sm text-gray-600 mb-3">
              Gerenciar ocorrências abertas
            </p>
            <div className="flex items-center text-red-600 font-semibold text-sm group-hover:gap-2 transition-all">
              Ver ocorrências
              <ArrowRight className="h-4 w-4 ml-1 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>
        </button>
      </div>
      </div>
    </PageContainer>
  )
}
