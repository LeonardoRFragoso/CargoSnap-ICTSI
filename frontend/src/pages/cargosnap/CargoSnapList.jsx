import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container, Package, Calendar, AlertCircle, Download,
  RefreshCw, Search, Filter, Eye, ImageIcon, CheckCircle2
} from 'lucide-react';
import api from '../../services/api';
import { useAuthStore } from '../../store/authStore';

const CargoSnapList = () => {
  const navigate = useNavigate();
  const [files, setFiles] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    has_damage: '',
    sync_status: '',
    date_from: '',
    date_to: ''
  });
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetchFiles();
    fetchStats();
  }, [page, filters]);

  const fetchFiles = async () => {
    try {
      setLoading(true);
      const params = {
        page,
        search: searchTerm,
        ...filters
      };
      
      const response = await api.get('/cargosnap/files/', { params });
      
      setFiles(response.data.results || []);
      setTotalPages(Math.ceil((response.data.count || 0) / 25));
    } catch (error) {
      console.error('Erro ao buscar arquivos:', error);
      setFiles([]);
      setTotalPages(1);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await api.get('/cargosnap/files/stats/');
      setStats(response.data);
    } catch (error) {
      console.error('Erro ao buscar estatísticas:', error);
    }
  };

  const handleSync = async () => {
    if (!confirm('Deseja sincronizar os dados do CargoSnap? Esta operação pode demorar alguns minutos.')) {
      return;
    }

    try {
      setSyncing(true);
      console.log('🚀 Iniciando sincronização...');
      
      const response = await api.post('/cargosnap/sync-logs/trigger_sync/', { download_images: true });
      console.log('✅ Resposta da API:', response.data);
      
      alert('Sincronização iniciada com sucesso!');
      fetchFiles();
      fetchStats();
    } catch (error) {
      console.error('❌ Erro ao sincronizar:', error);
      console.error('Detalhes do erro:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status
      });
      alert(`Erro ao iniciar sincronização: ${error.response?.data?.message || error.message}`);
    } finally {
      setSyncing(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    setPage(1);
    fetchFiles();
  };

  const StatusBadge = ({ status }) => {
    const colors = {
      pending: 'bg-yellow-100 text-yellow-800',
      syncing: 'bg-blue-100 text-blue-800',
      completed: 'bg-green-100 text-green-800',
      error: 'bg-red-100 text-red-800'
    };
    
    const labels = {
      pending: 'Pendente',
      syncing: 'Sincronizando',
      completed: 'Completo',
      error: 'Erro'
    };

    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[status]}`}>
        {labels[status]}
      </span>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-2">
                <Container className="w-8 h-8" />
                CargoSnap - Arquivos
              </h1>
              <p className="text-gray-600 mt-1">
                Dados sincronizados da API do CargoSnap
              </p>
            </div>
            <button
              onClick={handleSync}
              disabled={syncing}
              className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <RefreshCw className={`w-5 h-5 ${syncing ? 'animate-spin' : ''}`} />
              {syncing ? 'Sincronizando...' : 'Sincronizar Dados'}
            </button>
          </div>
        </div>

        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <div className="bg-white p-4 rounded-lg shadow">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Total de Arquivos</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.total_files}</p>
                </div>
                <Package className="w-10 h-10 text-blue-500" />
              </div>
            </div>
            
            <div className="bg-white p-4 rounded-lg shadow">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Total de Imagens</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.total_images}</p>
                </div>
                <ImageIcon className="w-10 h-10 text-purple-500" />
              </div>
            </div>
            
            <div className="bg-white p-4 rounded-lg shadow">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Imagens Baixadas</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.images_downloaded}</p>
                  <p className="text-xs text-gray-500">{stats.images_pending} pendentes</p>
                </div>
                <Download className="w-10 h-10 text-green-500" />
              </div>
            </div>
            
            <div className="bg-white p-4 rounded-lg shadow">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Com Avarias</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.files_with_damage}</p>
                  <p className="text-xs text-gray-500">{stats.total_damage_images} imagens</p>
                </div>
                <AlertCircle className="w-10 h-10 text-red-500" />
              </div>
            </div>
          </div>
        )}

        {/* Filters */}
        <div className="bg-white p-4 rounded-lg shadow mb-6">
          <form onSubmit={handleSearch} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Buscar Container
                </label>
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="text"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    placeholder="Código do container..."
                    className="pl-10 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Status
                </label>
                <select
                  value={filters.sync_status}
                  onChange={(e) => setFilters({ ...filters, sync_status: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">Todos</option>
                  <option value="pending">Pendente</option>
                  <option value="syncing">Sincronizando</option>
                  <option value="completed">Completo</option>
                  <option value="error">Erro</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Avarias
                </label>
                <select
                  value={filters.has_damage}
                  onChange={(e) => setFilters({ ...filters, has_damage: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">Todos</option>
                  <option value="true">Com Avarias</option>
                  <option value="false">Sem Avarias</option>
                </select>
              </div>

              <div className="flex items-end">
                <button
                  type="submit"
                  className="w-full flex items-center justify-center gap-2 bg-gray-700 text-white px-4 py-2 rounded-lg hover:bg-gray-800 transition-colors"
                >
                  <Filter className="w-5 h-5" />
                  Filtrar
                </button>
              </div>
            </div>
          </form>
        </div>

        {/* Files List */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          {loading ? (
            <div className="flex items-center justify-center p-12">
              <RefreshCw className="w-8 h-8 animate-spin text-blue-500" />
            </div>
          ) : !files || files.length === 0 ? (
            <div className="text-center p-12">
              <Package className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500 text-lg">Nenhum arquivo encontrado</p>
              <p className="text-gray-400 text-sm mt-2">
                Clique em "Sincronizar Dados" para buscar arquivos do CargoSnap
              </p>
            </div>
          ) : (
            <>
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Container
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Data
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Fotos
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Avarias
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Ações
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {files && files.map((file) => (
                    <tr key={file.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <Container className="w-5 h-5 text-gray-400 mr-2" />
                          <div>
                            <div className="text-sm font-medium text-gray-900">
                              {file.scan_code}
                            </div>
                            <div className="text-xs text-gray-500">
                              ID: {file.cargosnap_id}
                            </div>
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center text-sm text-gray-900">
                          <Calendar className="w-4 h-4 text-gray-400 mr-2" />
                          {new Date(file.created_at).toLocaleDateString('pt-BR')}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center gap-2">
                          <ImageIcon className="w-4 h-4 text-gray-400" />
                          <span className="text-sm text-gray-900">{file.snap_count}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {file.snap_count_with_damage > 0 ? (
                          <span className="flex items-center gap-1 text-sm text-red-600">
                            <AlertCircle className="w-4 h-4" />
                            {file.snap_count_with_damage}
                          </span>
                        ) : (
                          <span className="flex items-center gap-1 text-sm text-green-600">
                            <CheckCircle2 className="w-4 h-4" />
                            Sem avarias
                          </span>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <StatusBadge status={file.sync_status} />
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <button
                          onClick={() => navigate(`/cargosnap/${file.id}`)}
                          className="flex items-center gap-1 text-blue-600 hover:text-blue-800 transition-colors"
                        >
                          <Eye className="w-4 h-4" />
                          Ver Detalhes
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {/* Pagination */}
              {totalPages > 1 && (
                <div className="px-6 py-4 border-t border-gray-200 flex items-center justify-between">
                  <button
                    onClick={() => setPage(Math.max(1, page - 1))}
                    disabled={page === 1}
                    className="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Anterior
                  </button>
                  <span className="text-sm text-gray-700">
                    Página {page} de {totalPages}
                  </span>
                  <button
                    onClick={() => setPage(Math.min(totalPages, page + 1))}
                    disabled={page === totalPages}
                    className="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Próxima
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default CargoSnapList;
