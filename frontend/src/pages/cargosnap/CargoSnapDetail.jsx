import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  ArrowLeft, Container, Calendar, MapPin, User, AlertCircle,
  CheckCircle2, Download, RefreshCw, ImageIcon, Workflow,
  ExternalLink, ZoomIn
} from 'lucide-react';
import api from '../../services/api';

const CargoSnapDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedImage, setSelectedImage] = useState(null);
  const [activeTab, setActiveTab] = useState('images');

  useEffect(() => {
    fetchFileDetails();
  }, [id]);

  const fetchFileDetails = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/cargosnap/files/${id}/`);
      setFile(response.data);
    } catch (error) {
      console.error('Erro ao buscar detalhes:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadImages = async () => {
    if (!confirm('Deseja baixar todas as imagens deste arquivo?')) {
      return;
    }

    try {
      await api.post(`/cargosnap/files/${id}/download_images/`, {});
      alert('Download de imagens iniciado!');
      fetchFileDetails();
    } catch (error) {
      console.error('Erro ao baixar imagens:', error);
      alert('Erro ao iniciar download de imagens.');
    }
  };

  const handleSync = async () => {
    try {
      await api.post(`/cargosnap/files/${id}/sync/`, { download_images: true });
      alert('Sincronização iniciada!');
      fetchFileDetails();
    } catch (error) {
      console.error('Erro ao sincronizar:', error);
      alert('Erro ao sincronizar arquivo.');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <RefreshCw className="w-8 h-8 animate-spin text-blue-500" />
      </div>
    );
  }

  if (!file) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <p className="text-gray-500 text-lg">Arquivo não encontrado</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <button
            onClick={() => navigate('/cargosnap')}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
          >
            <ArrowLeft className="w-5 h-5" />
            Voltar
          </button>

          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-start justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-2">
                  <Container className="w-8 h-8" />
                  {file.scan_code}
                </h1>
                <p className="text-gray-600 mt-1">
                  ID: {file.cargosnap_id} • Formato: {file.scan_code_format || 'N/A'}
                </p>
              </div>
              <div className="flex gap-2 flex-wrap">
                <button
                  onClick={handleCreateInspection}
                  className="flex items-center gap-2 bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors font-semibold"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                  Criar Inspeção ICTSI
                </button>
                <button
                  onClick={handleDownloadImages}
                  className="flex items-center gap-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
                >
                  <Download className="w-5 h-5" />
                  Baixar Imagens
                </button>
                <button
                  onClick={handleSync}
                  className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  <RefreshCw className="w-5 h-5" />
                  Sincronizar
                </button>
              </div>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mt-6">
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600">Total de Fotos</p>
                <p className="text-2xl font-bold text-gray-900">{file.total_images}</p>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600">Fotos Baixadas</p>
                <p className="text-2xl font-bold text-gray-900">{file.downloaded_images}</p>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600">Com Avarias</p>
                <p className="text-2xl font-bold text-gray-900">{file.images_with_damage}</p>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600">Data de Criação</p>
                <p className="text-lg font-bold text-gray-900">
                  {new Date(file.created_at).toLocaleDateString('pt-BR')}
                </p>
              </div>
            </div>

            {/* Locations */}
            {file.locations && file.locations.length > 0 && (
              <div className="mt-4">
                <h3 className="text-sm font-medium text-gray-700 mb-2">Localizações:</h3>
                <div className="flex flex-wrap gap-2">
                  {file.locations.map((loc) => (
                    <span
                      key={loc.id}
                      className="flex items-center gap-1 px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                    >
                      <MapPin className="w-4 h-4" />
                      {loc.location}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="border-b border-gray-200">
            <nav className="flex -mb-px">
              <button
                onClick={() => setActiveTab('images')}
                className={`px-6 py-3 text-sm font-medium border-b-2 transition-colors ${
                  activeTab === 'images'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <ImageIcon className="w-5 h-5 inline mr-2" />
                Imagens ({file.total_images})
              </button>
              <button
                onClick={() => setActiveTab('workflows')}
                className={`px-6 py-3 text-sm font-medium border-b-2 transition-colors ${
                  activeTab === 'workflows'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <Workflow className="w-5 h-5 inline mr-2" />
                Workflows ({file.workflow_runs?.length || 0})
              </button>
            </nav>
          </div>

          {/* Images Tab */}
          {activeTab === 'images' && (
            <div className="p-6">
              {file.uploads && file.uploads.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {file.uploads.map((upload) => (
                    <div
                      key={upload.id}
                      className="bg-gray-50 rounded-lg overflow-hidden border border-gray-200 hover:shadow-lg transition-shadow"
                    >
                      {/* Image */}
                      <div className="relative bg-gray-900 aspect-video">
                        <img
                          src={upload.image_thumb || upload.image_url}
                          alt={upload.workflow_step_description || 'Imagem'}
                          className="w-full h-full object-contain cursor-pointer"
                          onClick={() => setSelectedImage(upload)}
                        />
                        <button
                          onClick={() => setSelectedImage(upload)}
                          className="absolute top-2 right-2 bg-white bg-opacity-90 p-2 rounded-lg hover:bg-opacity-100 transition-opacity"
                        >
                          <ZoomIn className="w-4 h-4 text-gray-700" />
                        </button>
                        {upload.has_damage && (
                          <div className="absolute top-2 left-2 bg-red-500 text-white px-2 py-1 rounded text-xs font-medium">
                            Com Avaria
                          </div>
                        )}
                      </div>

                      {/* Info */}
                      <div className="p-4">
                        {upload.workflow_step_description && (
                          <h4 className="font-medium text-gray-900 mb-2">
                            {upload.workflow_step_description}
                          </h4>
                        )}
                        
                        <div className="space-y-1 text-sm text-gray-600">
                          <div className="flex items-center gap-2">
                            <Calendar className="w-4 h-4" />
                            {new Date(upload.scan_date_time).toLocaleString('pt-BR')}
                          </div>
                          
                          {upload.device_nick && (
                            <div className="flex items-center gap-2">
                              <User className="w-4 h-4" />
                              {upload.device_nick}
                            </div>
                          )}
                          
                          {upload.latitude && upload.longitude && (
                            <div className="flex items-center gap-2">
                              <MapPin className="w-4 h-4" />
                              {upload.latitude}, {upload.longitude}
                            </div>
                          )}
                          
                          <div className="flex items-center gap-2 mt-2">
                            {upload.image_downloaded ? (
                              <span className="flex items-center gap-1 text-green-600">
                                <CheckCircle2 className="w-4 h-4" />
                                Baixada
                              </span>
                            ) : (
                              <span className="flex items-center gap-1 text-yellow-600">
                                <AlertCircle className="w-4 h-4" />
                                Não baixada
                              </span>
                            )}
                          </div>
                        </div>

                        {upload.comment && (
                          <div className="mt-3 p-2 bg-yellow-50 border border-yellow-200 rounded">
                            <p className="text-sm text-yellow-800">{upload.comment}</p>
                          </div>
                        )}

                        <div className="mt-3 flex gap-2">
                          <a
                            href={upload.image_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="flex items-center gap-1 text-blue-600 hover:text-blue-800 text-sm"
                          >
                            <ExternalLink className="w-4 h-4" />
                            Ver Original
                          </a>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <ImageIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-500">Nenhuma imagem encontrada</p>
                </div>
              )}
            </div>
          )}

          {/* Workflows Tab */}
          {activeTab === 'workflows' && (
            <div className="p-6">
              {file.workflow_runs && file.workflow_runs.length > 0 ? (
                <div className="space-y-6">
                  {file.workflow_runs.map((run) => (
                    <div key={run.id} className="bg-gray-50 rounded-lg p-6 border border-gray-200">
                      <div className="flex items-start justify-between mb-4">
                        <div>
                          <h3 className="text-lg font-bold text-gray-900">
                            {run.workflow?.name || 'Workflow'}
                          </h3>
                          <p className="text-sm text-gray-600 mt-1">
                            Iniciado em: {new Date(run.submit_date_time).toLocaleString('pt-BR')}
                          </p>
                          {run.completed_at && (
                            <p className="text-sm text-gray-600">
                              Concluído em: {new Date(run.completed_at).toLocaleString('pt-BR')}
                            </p>
                          )}
                        </div>
                      </div>

                      {/* Workflow Steps */}
                      {run.run_steps && run.run_steps.length > 0 && (
                        <div className="space-y-2">
                          <h4 className="text-sm font-medium text-gray-700 mb-2">Etapas:</h4>
                          {run.run_steps.map((step, idx) => (
                            <div
                              key={step.id}
                              className="flex items-center gap-3 p-3 bg-white rounded border border-gray-200"
                            >
                              <div className="flex-shrink-0 w-8 h-8 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center font-medium text-sm">
                                {idx + 1}
                              </div>
                              <div className="flex-grow">
                                <p className="text-sm font-medium text-gray-900">
                                  {step.workflow_step?.description || 'Etapa'}
                                </p>
                                <p className="text-xs text-gray-500">
                                  {new Date(step.submit_date_time).toLocaleString('pt-BR')}
                                </p>
                              </div>
                              <span className={`px-2 py-1 rounded text-xs font-medium ${
                                step.status === 'done'
                                  ? 'bg-green-100 text-green-800'
                                  : 'bg-yellow-100 text-yellow-800'
                              }`}>
                                {step.status === 'done' ? 'Concluído' : step.status}
                              </span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <Workflow className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-500">Nenhum workflow encontrado</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Image Modal */}
      {selectedImage && (
        <div
          className="fixed inset-0 bg-black bg-opacity-90 z-50 flex items-center justify-center p-4"
          onClick={() => setSelectedImage(null)}
        >
          <div className="max-w-5xl w-full">
            <img
              src={selectedImage.image_url}
              alt={selectedImage.workflow_step_description || 'Imagem'}
              className="w-full h-auto max-h-[90vh] object-contain"
            />
            <div className="mt-4 text-white text-center">
              <p className="font-medium">{selectedImage.workflow_step_description}</p>
              <p className="text-sm text-gray-300 mt-1">
                {new Date(selectedImage.scan_date_time).toLocaleString('pt-BR')}
              </p>
              <button
                onClick={() => setSelectedImage(null)}
                className="mt-4 px-6 py-2 bg-white text-gray-900 rounded-lg hover:bg-gray-100"
              >
                Fechar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CargoSnapDetail;
