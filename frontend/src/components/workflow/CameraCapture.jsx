import { useState, useRef, useEffect } from 'react'
import { Camera, X, RotateCw, Check, Upload } from 'lucide-react'

/**
 * CameraCapture Component
 * Allows users to capture photos directly from device camera or upload files
 */
export default function CameraCapture({ onCapture, onClose, maxPhotos = 10, currentCount = 0 }) {
  const [stream, setStream] = useState(null)
  const [capturedPhoto, setCapturedPhoto] = useState(null)
  const [cameraActive, setCameraActive] = useState(false)
  const [facingMode, setFacingMode] = useState('environment') // 'user' or 'environment'
  const [error, setError] = useState(null)
  
  const videoRef = useRef(null)
  const canvasRef = useRef(null)
  const fileInputRef = useRef(null)

  // Start camera
  const startCamera = async () => {
    try {
      setError(null)
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: facingMode,
          width: { ideal: 1920 },
          height: { ideal: 1080 }
        }
      })
      
      setStream(mediaStream)
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream
      }
      setCameraActive(true)
    } catch (err) {
      console.error('Error accessing camera:', err)
      setError('Não foi possível acessar a câmera. Verifique as permissões.')
    }
  }

  // Stop camera
  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop())
      setStream(null)
      setCameraActive(false)
    }
  }

  // Capture photo
  const capturePhoto = () => {
    if (!videoRef.current || !canvasRef.current) return

    const video = videoRef.current
    const canvas = canvasRef.current
    
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    
    const context = canvas.getContext('2d')
    context.drawImage(video, 0, 0, canvas.width, canvas.height)
    
    canvas.toBlob((blob) => {
      const url = URL.createObjectURL(blob)
      setCapturedPhoto({
        blob,
        url,
        file: new File([blob], `photo_${Date.now()}.jpg`, { type: 'image/jpeg' })
      })
      stopCamera()
    }, 'image/jpeg', 0.95)
  }

  // Switch camera (front/back)
  const switchCamera = () => {
    stopCamera()
    setFacingMode(prev => prev === 'user' ? 'environment' : 'user')
    setTimeout(() => startCamera(), 100)
  }

  // Confirm captured photo
  const confirmPhoto = () => {
    if (capturedPhoto) {
      onCapture(capturedPhoto.file, capturedPhoto.url)
      setCapturedPhoto(null)
      if (currentCount + 1 < maxPhotos) {
        startCamera() // Continue capturing
      } else {
        onClose()
      }
    }
  }

  // Retake photo
  const retakePhoto = () => {
    if (capturedPhoto) {
      URL.revokeObjectURL(capturedPhoto.url)
      setCapturedPhoto(null)
    }
    startCamera()
  }

  // Handle file upload
  const handleFileUpload = (e) => {
    const files = Array.from(e.target.files)
    files.forEach(file => {
      const url = URL.createObjectURL(file)
      onCapture(file, url)
    })
    if (currentCount + files.length >= maxPhotos) {
      onClose()
    }
  }

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      stopCamera()
      if (capturedPhoto) {
        URL.revokeObjectURL(capturedPhoto.url)
      }
    }
  }, [])

  return (
    <div className="fixed inset-0 z-50 bg-black">
      {/* Header */}
      <div className="absolute top-0 left-0 right-0 z-10 flex items-center justify-between p-4 bg-gradient-to-b from-black/70 to-transparent">
        <button
          onClick={onClose}
          className="p-2 text-white hover:bg-white/20 rounded-full transition-colors"
        >
          <X className="h-6 w-6" />
        </button>
        
        <div className="text-white text-sm font-medium">
          {currentCount}/{maxPhotos} fotos
        </div>
        
        {cameraActive && !capturedPhoto && (
          <button
            onClick={switchCamera}
            className="p-2 text-white hover:bg-white/20 rounded-full transition-colors"
          >
            <RotateCw className="h-6 w-6" />
          </button>
        )}
      </div>

      {/* Main Content */}
      <div className="h-full flex flex-col items-center justify-center">
        {error && (
          <div className="absolute top-20 left-4 right-4 bg-red-500 text-white p-4 rounded-lg">
            {error}
          </div>
        )}

        {!cameraActive && !capturedPhoto && (
          <div className="flex flex-col items-center gap-4 p-8">
            <Camera className="h-24 w-24 text-white/50" />
            <h2 className="text-white text-xl font-semibold">Capturar Foto</h2>
            <p className="text-white/70 text-center">
              Escolha como deseja adicionar a foto
            </p>
            
            <div className="flex flex-col gap-3 w-full max-w-xs mt-4">
              <button
                onClick={startCamera}
                className="flex items-center justify-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Camera className="h-5 w-5" />
                Abrir Câmera
              </button>
              
              <button
                onClick={() => fileInputRef.current?.click()}
                className="flex items-center justify-center gap-2 px-6 py-3 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors"
              >
                <Upload className="h-5 w-5" />
                Escolher da Galeria
              </button>
              
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                multiple
                className="hidden"
                onChange={handleFileUpload}
              />
            </div>
          </div>
        )}

        {cameraActive && !capturedPhoto && (
          <div className="relative w-full h-full">
            <video
              ref={videoRef}
              autoPlay
              playsInline
              className="w-full h-full object-cover"
            />
            
            {/* Capture Button */}
            <div className="absolute bottom-8 left-0 right-0 flex justify-center">
              <button
                onClick={capturePhoto}
                className="w-20 h-20 rounded-full bg-white border-4 border-gray-300 hover:bg-gray-100 transition-all active:scale-95"
              >
                <div className="w-full h-full rounded-full border-2 border-gray-400" />
              </button>
            </div>
          </div>
        )}

        {capturedPhoto && (
          <div className="relative w-full h-full">
            <img
              src={capturedPhoto.url}
              alt="Captured"
              className="w-full h-full object-contain"
            />
            
            {/* Action Buttons */}
            <div className="absolute bottom-8 left-0 right-0 flex justify-center gap-4 px-4">
              <button
                onClick={retakePhoto}
                className="flex items-center gap-2 px-6 py-3 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors"
              >
                <RotateCw className="h-5 w-5" />
                Refazer
              </button>
              
              <button
                onClick={confirmPhoto}
                className="flex items-center gap-2 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                <Check className="h-5 w-5" />
                Confirmar
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Hidden canvas for photo capture */}
      <canvas ref={canvasRef} className="hidden" />
    </div>
  )
}
