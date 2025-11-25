import React, { useState } from 'react';
import { Camera, Upload, X, Loader } from 'lucide-react';
import MobileCamera from './MobileCamera';
import api from '../services/api';

/**
 * Componente de upload de fotos com suporte a câmera mobile
 * Envia fotos diretamente para a inspeção com geolocalização
 */
const MobilePhotoUpload = ({ inspectionId, onUploadComplete, onClose }) => {
  const [showCamera, setShowCamera] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [photos, setPhotos] = useState([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  const handleCameraCapture = (capturedImage) => {
    setPhotos([...photos, capturedImage]);
    setShowCamera(false);
  };

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files);
    
    // Get location
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const newPhotos = files.map(file => ({
            file,
            preview: URL.createObjectURL(file),
            location: {
              latitude: position.coords.latitude,
              longitude: position.coords.longitude
            },
            timestamp: new Date().toISOString(),
            deviceInfo: {
              userAgent: navigator.userAgent,
              platform: navigator.platform
            }
          }));
          
          setPhotos([...photos, ...newPhotos]);
        },
        () => {
          // Without location
          const newPhotos = files.map(file => ({
            file,
            preview: URL.createObjectURL(file),
            timestamp: new Date().toISOString(),
            deviceInfo: {
              userAgent: navigator.userAgent,
              platform: navigator.platform
            }
          }));
          
          setPhotos([...photos, ...newPhotos]);
        }
      );
    } else {
      const newPhotos = files.map(file => ({
        file,
        preview: URL.createObjectURL(file),
        timestamp: new Date().toISOString(),
        deviceInfo: {
          userAgent: navigator.userAgent,
          platform: navigator.platform
        }
      }));
      
      setPhotos([...photos, ...newPhotos]);
    }
  };

  const removePhoto = (index) => {
    const newPhotos = photos.filter((_, i) => i !== index);
    setPhotos(newPhotos);
  };

  const uploadPhotos = async () => {
    if (photos.length === 0) {
      alert('Selecione pelo menos uma foto');
      return;
    }

    try {
      setUploading(true);

      for (const photo of photos) {
        const formData = new FormData();
        formData.append('inspection_id', inspectionId);
        formData.append('photo', photo.file);
        formData.append('title', title || 'Foto Mobile');
        formData.append('description', description || '');
        
        if (photo.location) {
          formData.append('latitude', photo.location.latitude);
          formData.append('longitude', photo.location.longitude);
        }
        
        if (photo.deviceInfo) {
          formData.append('device_model', photo.deviceInfo.platform || '');
          formData.append('device_os', photo.deviceInfo.userAgent || '');
        }

        await api.post('/inspections/photos/upload_from_mobile/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
      }

      alert(`${photos.length} foto(s) enviada(s) com sucesso!`);
      
      if (onUploadComplete) {
        onUploadComplete();
      }
      
      if (onClose) {
        onClose();
      }

    } catch (error) {
      console.error('Erro ao enviar fotos:', error);
      alert(`Erro ao enviar fotos: ${error.response?.data?.error || error.message}`);
    } finally {
      setUploading(false);
    }
  };

  if (showCamera) {
    return (
      <MobileCamera
        onCapture={handleCameraCapture}
        onClose={() => setShowCamera(false)}
      />
    );
  }

  return (
    <div className="fixed inset-0 bg-white z-50 flex flex-col overflow-hidden">
      {/* Header */}
      <div className="bg-blue-600 text-white p-4 flex items-center justify-between shadow-lg">
        <button
          onClick={onClose}
          disabled={uploading}
          className="p-2 hover:bg-blue-700 rounded-full transition-colors"
        >
          <X className="w-6 h-6" />
        </button>
        <h2 className="font-semibold text-lg">Adicionar Fotos</h2>
        <div className="w-10" /> {/* Spacer */}
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {/* Input fields */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Título
          </label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Ex: Porta lateral"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={uploading}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Descrição (opcional)
          </label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Descreva o que está sendo fotografado..."
            rows={3}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            disabled={uploading}
          />
        </div>

        {/* Photos Grid */}
        {photos.length > 0 && (
          <div className="grid grid-cols-2 gap-3">
            {photos.map((photo, index) => (
              <div key={index} className="relative aspect-square bg-gray-100 rounded-lg overflow-hidden">
                <img
                  src={photo.preview}
                  alt={`Foto ${index + 1}`}
                  className="w-full h-full object-cover"
                />
                {!uploading && (
                  <button
                    onClick={() => removePhoto(index)}
                    className="absolute top-2 right-2 bg-red-600 text-white p-1.5 rounded-full hover:bg-red-700 transition-colors shadow-lg"
                  >
                    <X className="w-4 h-4" />
                  </button>
                )}
                {photo.location && (
                  <div className="absolute bottom-2 left-2 bg-black bg-opacity-60 text-white text-xs px-2 py-1 rounded">
                    📍 GPS
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {photos.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            <Camera className="w-16 h-16 mx-auto mb-4 text-gray-300" />
            <p>Nenhuma foto selecionada</p>
            <p className="text-sm">Use os botões abaixo para adicionar fotos</p>
          </div>
        )}
      </div>

      {/* Footer Actions */}
      <div className="border-t border-gray-200 p-4 space-y-3">
        {/* Action Buttons */}
        <div className="grid grid-cols-2 gap-3">
          <button
            onClick={() => setShowCamera(true)}
            disabled={uploading}
            className="flex items-center justify-center gap-2 bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-semibold"
          >
            <Camera className="w-5 h-5" />
            Câmera
          </button>

          <label className="flex items-center justify-center gap-2 bg-gray-600 text-white py-3 rounded-lg hover:bg-gray-700 disabled:opacity-50 cursor-pointer transition-colors font-semibold">
            <Upload className="w-5 h-5" />
            Galeria
            <input
              type="file"
              accept="image/*"
              multiple
              onChange={handleFileSelect}
              className="hidden"
              disabled={uploading}
            />
          </label>
        </div>

        {/* Upload Button */}
        {photos.length > 0 && (
          <button
            onClick={uploadPhotos}
            disabled={uploading}
            className="w-full bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-semibold flex items-center justify-center gap-2"
          >
            {uploading ? (
              <>
                <Loader className="w-5 h-5 animate-spin" />
                Enviando {photos.length} foto(s)...
              </>
            ) : (
              <>
                <Upload className="w-5 h-5" />
                Enviar {photos.length} foto(s)
              </>
            )}
          </button>
        )}
      </div>
    </div>
  );
};

export default MobilePhotoUpload;
