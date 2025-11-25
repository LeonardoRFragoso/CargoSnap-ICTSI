import React, { useRef, useState, useEffect } from 'react';
import { Camera, X, FlipHorizontal, Check } from 'lucide-react';

/**
 * Componente de câmera mobile-first com captura de geolocalização
 * Suporta câmera frontal e traseira
 */
const MobileCamera = ({ onCapture, onClose }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [stream, setStream] = useState(null);
  const [facingMode, setFacingMode] = useState('environment'); // 'user' ou 'environment'
  const [capturedImage, setCapturedImage] = useState(null);
  const [location, setLocation] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    startCamera();
    getLocation();
    
    return () => {
      stopCamera();
    };
  }, [facingMode]);

  const getLocation = () => {
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLocation({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            accuracy: position.coords.accuracy
          });
        },
        (error) => {
          console.warn('Geolocation error:', error);
        }
      );
    }
  };

  const startCamera = async () => {
    try {
      const constraints = {
        video: {
          facingMode: facingMode,
          width: { ideal: 1920 },
          height: { ideal: 1080 }
        }
      };

      const mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
      setStream(mediaStream);
      setError(null);
    } catch (err) {
      console.error('Error accessing camera:', err);
      setError('Não foi possível acessar a câmera. Verifique as permissões.');
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
    }
  };

  const toggleCamera = () => {
    setFacingMode(prev => prev === 'user' ? 'environment' : 'user');
  };

  const capturePhoto = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;

    if (video && canvas) {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      
      const context = canvas.getContext('2d');
      context.drawImage(video, 0, 0);

      canvas.toBlob((blob) => {
        const file = new File([blob], `photo_${Date.now()}.jpg`, { type: 'image/jpeg' });
        const preview = canvas.toDataURL('image/jpeg');
        
        setCapturedImage({
          file,
          preview,
          location,
          timestamp: new Date().toISOString(),
          deviceInfo: {
            userAgent: navigator.userAgent,
            platform: navigator.platform
          }
        });
      }, 'image/jpeg', 0.9);
    }
  };

  const confirmPhoto = () => {
    if (capturedImage) {
      onCapture(capturedImage);
      setCapturedImage(null);
    }
  };

  const retakePhoto = () => {
    setCapturedImage(null);
  };

  if (error) {
    return (
      <div className="fixed inset-0 bg-black z-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg p-6 max-w-md">
          <h3 className="text-lg font-bold text-red-600 mb-2">Erro na Câmera</h3>
          <p className="text-gray-700 mb-4">{error}</p>
          <button
            onClick={onClose}
            className="w-full bg-gray-600 text-white py-2 rounded-lg hover:bg-gray-700"
          >
            Fechar
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-black z-50 flex flex-col">
      {/* Header */}
      <div className="bg-black bg-opacity-70 p-4 flex items-center justify-between">
        <button
          onClick={onClose}
          className="text-white p-2 hover:bg-white hover:bg-opacity-20 rounded-full transition-colors"
        >
          <X className="w-6 h-6" />
        </button>
        
        <h2 className="text-white font-semibold">Tirar Foto</h2>
        
        <button
          onClick={toggleCamera}
          className="text-white p-2 hover:bg-white hover:bg-opacity-20 rounded-full transition-colors"
          disabled={!!capturedImage}
        >
          <FlipHorizontal className="w-6 h-6" />
        </button>
      </div>

      {/* Camera View / Preview */}
      <div className="flex-1 relative bg-black">
        {!capturedImage ? (
          <>
            <video
              ref={videoRef}
              autoPlay
              playsInline
              className="w-full h-full object-cover"
            />
            <canvas ref={canvasRef} className="hidden" />
            
            {/* Location indicator */}
            {location && (
              <div className="absolute top-4 left-4 bg-black bg-opacity-60 text-white text-xs px-3 py-2 rounded-full">
                📍 GPS: {location.latitude.toFixed(6)}, {location.longitude.toFixed(6)}
              </div>
            )}
          </>
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <img
              src={capturedImage.preview}
              alt="Captured"
              className="max-w-full max-h-full object-contain"
            />
          </div>
        )}
      </div>

      {/* Controls */}
      <div className="bg-black bg-opacity-70 p-6">
        {!capturedImage ? (
          <div className="flex items-center justify-center">
            <button
              onClick={capturePhoto}
              className="w-20 h-20 bg-white rounded-full flex items-center justify-center hover:bg-opacity-90 transition-all shadow-lg"
            >
              <Camera className="w-10 h-10 text-gray-800" />
            </button>
          </div>
        ) : (
          <div className="flex items-center justify-center gap-4">
            <button
              onClick={retakePhoto}
              className="flex-1 bg-gray-600 text-white py-3 rounded-lg hover:bg-gray-700 transition-colors font-semibold"
            >
              <X className="w-5 h-5 inline mr-2" />
              Refazer
            </button>
            <button
              onClick={confirmPhoto}
              className="flex-1 bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 transition-colors font-semibold"
            >
              <Check className="w-5 h-5 inline mr-2" />
              Usar Foto
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default MobileCamera;
