import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowLeft, Save, MapPin, User, Calendar, Cloud, Thermometer, Hash, Upload, X, Loader2, Image as ImageIcon } from 'lucide-react'
import { inspectionTypeService, inspectionService, photoService } from '../../services/inspectionService'
import { useToast } from '../../hooks/useToast'
import Toast from '../../components/ui/Toast'

export default function CreateInspection() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    inspection_type: 1, // Default type ID
    external_reference: '',
    status: 'DRAFT',
    
    // Location
    location: '',
    latitude: '',
    longitude: '',
    
    // Environment
    weather_condition: '',
    temperature: '',
    
    // Scheduling
    scheduled_date: '',
    
    // Customer
    customer_name: '',
    customer_email: '',
    customer_phone: '',
  })

  const [inspectionTypes, setInspectionTypes] = useState([])
  const [useGeolocation, setUseGeolocation] = useState(false)
  const [loading, setLoading] = useState(false)
  const [loadingTypes, setLoadingTypes] = useState(true)
  const [photos, setPhotos] = useState([])
  const [uploadingPhotos, setUploadingPhotos] = useState(false)
  const [errors, setErrors] = useState({})
  
  const { toasts, hideToast, success, error: showError, warning } = useToast()

  // Load inspection types from API
  useEffect(() => {
    const fetchInspectionTypes = async () => {
      try {
        setLoadingTypes(true)
        console.log('Fetching inspection types...')
        const data = await inspectionTypeService.getAll()
        console.log('Inspection types received:', data)
        
        // Handle different response formats
        let types = []
        if (Array.isArray(data)) {
          types = data
        } else if (data.results && Array.isArray(data.results)) {
          types = data.results
        } else if (data.data && Array.isArray(data.data)) {
          types = data.data
        }
        
        console.log('Processed types:', types)
        
        if (types.length > 0) {
          setInspectionTypes(types)
          setFormData(prev => ({ ...prev, inspection_type: types[0].id }))
        } else {
          // Fallback to mock data if no types found
          console.warn('No inspection types found, using fallback data')
          const fallbackTypes = [
            { id: 1, name: 'Inspeção de Carga' },
            { id: 2, name: 'Inspeção de Container' },
            { id: 3, name: 'Inspeção de Veículo' },
            { id: 4, name: 'Inspeção de Recebimento' },
            { id: 5, name: 'Inspeção de Expedição' },
          ]
          setInspectionTypes(fallbackTypes)
          setFormData(prev => ({ ...prev, inspection_type: fallbackTypes[0].id }))
        }
      } catch (err) {
        console.error('Error loading inspection types:', err)
        showError('Erro ao carregar tipos de inspeção. Usando dados padrão.')
        // Fallback to mock data
        const fallbackTypes = [
          { id: 1, name: 'Inspeção de Carga' },
          { id: 2, name: 'Inspeção de Container' },
          { id: 3, name: 'Inspeção de Veículo' },
          { id: 4, name: 'Inspeção de Recebimento' },
          { id: 5, name: 'Inspeção de Expedição' },
        ]
        setInspectionTypes(fallbackTypes)
        setFormData(prev => ({ ...prev, inspection_type: fallbackTypes[0].id }))
      } finally {
        setLoadingTypes(false)
      }
    }
    
    fetchInspectionTypes()
  }, [])

  // Get current location
  const getCurrentLocation = () => {
    if (navigator.geolocation) {
      setUseGeolocation(true)
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setFormData(prev => ({
            ...prev,
            latitude: position.coords.latitude.toFixed(6),
            longitude: position.coords.longitude.toFixed(6),
          }))
          setUseGeolocation(false)
        },
        (error) => {
          console.error('Error getting location:', error)
          showError('Não foi possível obter a localização')
          setUseGeolocation(false)
        }
      )
    } else {
      showError('Geolocalização não suportada pelo navegador')
    }
  }

  // Validate form
  const validateForm = () => {
    const newErrors = {}
    
    if (!formData.title.trim()) {
      newErrors.title = 'Título é obrigatório'
    }
    
    if (formData.customer_email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.customer_email)) {
      newErrors.customer_email = 'Email inválido'
    }
    
    if (formData.latitude && (formData.latitude < -90 || formData.latitude > 90)) {
      newErrors.latitude = 'Latitude deve estar entre -90 e 90'
    }
    
    if (formData.longitude && (formData.longitude < -180 || formData.longitude > 180)) {
      newErrors.longitude = 'Longitude deve estar entre -180 e 180'
    }
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!validateForm()) {
      warning('Por favor, corrija os erros no formulário')
      return
    }
    
    try {
      setLoading(true)
      
      // Prepare data for API
      const dataToSend = {
        ...formData,
        latitude: formData.latitude ? parseFloat(formData.latitude) : null,
        longitude: formData.longitude ? parseFloat(formData.longitude) : null,
        temperature: formData.temperature ? parseFloat(formData.temperature) : null,
      }
      
      // Create inspection
      const createdInspection = await inspectionService.create(dataToSend)
      
      // Upload photos if any
      if (photos.length > 0) {
        setUploadingPhotos(true)
        await uploadPhotos(createdInspection.id)
      }
      
      success('Inspeção criada com sucesso!')
      
      // Navigate to inspection detail or list
      setTimeout(() => {
        navigate(`/inspections/${createdInspection.id}`)
      }, 1000)
      
    } catch (err) {
      console.error('Error creating inspection:', err)
      const errorMessage = err.response?.data?.detail || 
                          err.response?.data?.message || 
                          'Erro ao criar inspeção'
      showError(errorMessage)
    } finally {
      setLoading(false)
      setUploadingPhotos(false)
    }
  }
  
  // Upload photos
  const uploadPhotos = async (inspectionId) => {
    const uploadPromises = photos.map((photo, index) => {
      return photoService.upload({
        inspection: inspectionId,
        photo: photo.file,
        title: photo.title || `Foto ${index + 1}`,
        sequence_number: index,
      })
    })
    
    try {
      await Promise.all(uploadPromises)
    } catch (err) {
      console.error('Error uploading photos:', err)
      warning('Algumas fotos não foram enviadas')
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
    
    // Clear error for this field
    if (errors[name]) {
      setErrors(prev => {
        const newErrors = { ...prev }
        delete newErrors[name]
        return newErrors
      })
    }
  }
  
  // Handle photo selection
  const handlePhotoSelect = (e) => {
    const files = Array.from(e.target.files)
    
    if (files.length + photos.length > 10) {
      warning('Máximo de 10 fotos permitido')
      return
    }
    
    const newPhotos = files.map(file => ({
      file,
      preview: URL.createObjectURL(file),
      title: file.name,
    }))
    
    setPhotos(prev => [...prev, ...newPhotos])
  }
  
  // Remove photo
  const removePhoto = (index) => {
    setPhotos(prev => {
      const newPhotos = [...prev]
      URL.revokeObjectURL(newPhotos[index].preview)
      newPhotos.splice(index, 1)
      return newPhotos
    })
  }
  
  // Update photo title
  const updatePhotoTitle = (index, title) => {
    setPhotos(prev => {
      const newPhotos = [...prev]
      newPhotos[index].title = title
      return newPhotos
    })
  }

  return (
    <div>
      <div className="mb-6">
        <button
          onClick={() => navigate(-1)}
          className="inline-flex items-center text-sm font-medium text-gray-500 hover:text-gray-700 tap-target"
        >
          <ArrowLeft className="h-5 w-5 mr-2" />
          Voltar
        </button>
      </div>

      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h1 className="text-2xl font-bold text-gray-900 mb-6">
            Nova Inspeção
          </h1>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Basic Information */}
            <div className="border-b border-gray-200 pb-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Informações Básicas</h2>
              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                <div className="sm:col-span-2">
                  <label htmlFor="title" className="block text-sm font-medium text-gray-700">
                    Título *
                  </label>
                  <input
                    type="text"
                    name="title"
                    id="title"
                    required
                    placeholder="Ex: Inspeção Container ABCD1234"
                    className={`mt-1 block w-full rounded-md border px-3 py-2 shadow-sm focus:outline-none focus:ring-blue-500 sm:text-sm tap-target ${
                      errors.title ? 'border-red-300 focus:border-red-500' : 'border-gray-300 focus:border-blue-500'
                    }`}
                    value={formData.title}
                    onChange={handleChange}
                  />
                  {errors.title && (
                    <p className="mt-1 text-sm text-red-600">{errors.title}</p>
                  )}
                </div>

                <div>
                  <label htmlFor="inspection_type" className="block text-sm font-medium text-gray-700">
                    Tipo de Inspeção *
                  </label>
                  <select
                    id="inspection_type"
                    name="inspection_type"
                    required
                    disabled={loadingTypes}
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm tap-target disabled:opacity-50"
                    value={formData.inspection_type}
                    onChange={handleChange}
                  >
                    {loadingTypes ? (
                      <option value="">Carregando tipos...</option>
                    ) : inspectionTypes.length === 0 ? (
                      <option value="">Nenhum tipo disponível</option>
                    ) : (
                      inspectionTypes.map(type => (
                        <option key={type.id} value={type.id}>{type.name}</option>
                      ))
                    )}
                  </select>
                  {!loadingTypes && inspectionTypes.length === 0 && (
                    <p className="mt-1 text-sm text-yellow-600">
                      Nenhum tipo de inspeção encontrado. Verifique a conexão com a API.
                    </p>
                  )}
                </div>

                <div>
                  <label htmlFor="external_reference" className="block text-sm font-medium text-gray-700">
                    <Hash className="inline h-4 w-4 mr-1" />
                    Referência Externa
                  </label>
                  <input
                    type="text"
                    name="external_reference"
                    id="external_reference"
                    placeholder="Ex: BL123456, Pedido #789"
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm tap-target"
                    value={formData.external_reference}
                    onChange={handleChange}
                  />
                </div>

                <div>
                  <label htmlFor="scheduled_date" className="block text-sm font-medium text-gray-700">
                    <Calendar className="inline h-4 w-4 mr-1" />
                    Data Agendada
                  </label>
                  <input
                    type="datetime-local"
                    name="scheduled_date"
                    id="scheduled_date"
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm tap-target"
                    value={formData.scheduled_date}
                    onChange={handleChange}
                  />
                </div>

                <div>
                  <label htmlFor="status" className="block text-sm font-medium text-gray-700">
                    Status Inicial
                  </label>
                  <select
                    id="status"
                    name="status"
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm tap-target"
                    value={formData.status}
                    onChange={handleChange}
                  >
                    <option value="DRAFT">Rascunho</option>
                    <option value="IN_PROGRESS">Em Andamento</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Location Information */}
            <div className="border-b border-gray-200 pb-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
                <MapPin className="h-5 w-5 mr-2" />
                Localização
              </h2>
              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                <div className="sm:col-span-2">
                  <label htmlFor="location" className="block text-sm font-medium text-gray-700">
                    Local
                  </label>
                  <input
                    type="text"
                    name="location"
                    id="location"
                    placeholder="Ex: Armazém 5, Porto de Santos"
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm tap-target"
                    value={formData.location}
                    onChange={handleChange}
                  />
                </div>

                <div>
                  <label htmlFor="latitude" className="block text-sm font-medium text-gray-700">
                    Latitude
                  </label>
                  <input
                    type="number"
                    step="0.000001"
                    name="latitude"
                    id="latitude"
                    placeholder="-23.956789"
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm tap-target"
                    value={formData.latitude}
                    onChange={handleChange}
                  />
                </div>

                <div>
                  <label htmlFor="longitude" className="block text-sm font-medium text-gray-700">
                    Longitude
                  </label>
                  <input
                    type="number"
                    step="0.000001"
                    name="longitude"
                    id="longitude"
                    placeholder="-46.328888"
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm tap-target"
                    value={formData.longitude}
                    onChange={handleChange}
                  />
                </div>

                <div className="sm:col-span-2">
                  <button
                    type="button"
                    onClick={getCurrentLocation}
                    disabled={useGeolocation}
                    className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 tap-target"
                  >
                    <MapPin className="h-4 w-4 mr-2" />
                    {useGeolocation ? 'Obtendo localização...' : 'Usar Localização Atual'}
                  </button>
                </div>
              </div>
            </div>

            {/* Environment Conditions */}
            <div className="border-b border-gray-200 pb-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
                <Cloud className="h-5 w-5 mr-2" />
                Condições Ambientais
              </h2>
              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                <div>
                  <label htmlFor="weather_condition" className="block text-sm font-medium text-gray-700">
                    Condição Climática
                  </label>
                  <select
                    id="weather_condition"
                    name="weather_condition"
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm tap-target"
                    value={formData.weather_condition}
                    onChange={handleChange}
                  >
                    <option value="">Selecione...</option>
                    <option value="SUNNY">Ensolarado</option>
                    <option value="CLOUDY">Nublado</option>
                    <option value="RAINY">Chuvoso</option>
                    <option value="STORMY">Tempestade</option>
                    <option value="FOGGY">Neblina</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="temperature" className="block text-sm font-medium text-gray-700">
                    <Thermometer className="inline h-4 w-4 mr-1" />
                    Temperatura (°C)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    name="temperature"
                    id="temperature"
                    placeholder="25.5"
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm tap-target"
                    value={formData.temperature}
                    onChange={handleChange}
                  />
                </div>
              </div>
            </div>

            {/* Customer Information */}
            <div className="border-b border-gray-200 pb-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
                <User className="h-5 w-5 mr-2" />
                Informações do Cliente
              </h2>
              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                <div className="sm:col-span-2">
                  <label htmlFor="customer_name" className="block text-sm font-medium text-gray-700">
                    Nome do Cliente
                  </label>
                  <input
                    type="text"
                    name="customer_name"
                    id="customer_name"
                    placeholder="Ex: Empresa ABC Ltda"
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm tap-target"
                    value={formData.customer_name}
                    onChange={handleChange}
                  />
                </div>

                <div>
                  <label htmlFor="customer_email" className="block text-sm font-medium text-gray-700">
                    Email do Cliente
                  </label>
                  <input
                    type="email"
                    name="customer_email"
                    id="customer_email"
                    placeholder="cliente@empresa.com"
                    className={`mt-1 block w-full rounded-md border px-3 py-2 shadow-sm focus:outline-none focus:ring-blue-500 sm:text-sm tap-target ${
                      errors.customer_email ? 'border-red-300 focus:border-red-500' : 'border-gray-300 focus:border-blue-500'
                    }`}
                    value={formData.customer_email}
                    onChange={handleChange}
                  />
                  {errors.customer_email && (
                    <p className="mt-1 text-sm text-red-600">{errors.customer_email}</p>
                  )}
                </div>

                <div>
                  <label htmlFor="customer_phone" className="block text-sm font-medium text-gray-700">
                    Telefone do Cliente
                  </label>
                  <input
                    type="tel"
                    name="customer_phone"
                    id="customer_phone"
                    placeholder="(11) 98765-4321"
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm tap-target"
                    value={formData.customer_phone}
                    onChange={handleChange}
                  />
                </div>
              </div>
            </div>

            {/* Photo Upload */}
            <div className="border-b border-gray-200 pb-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
                <ImageIcon className="h-5 w-5 mr-2" />
                Fotos Iniciais (Opcional)
              </h2>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Adicionar Fotos ({photos.length}/10)
                  </label>
                  <div className="flex items-center justify-center w-full">
                    <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100">
                      <div className="flex flex-col items-center justify-center pt-5 pb-6">
                        <Upload className="h-10 w-10 text-gray-400 mb-2" />
                        <p className="text-sm text-gray-500">
                          <span className="font-semibold">Clique para adicionar</span> ou arraste fotos
                        </p>
                        <p className="text-xs text-gray-500 mt-1">PNG, JPG até 10MB</p>
                      </div>
                      <input
                        type="file"
                        className="hidden"
                        accept="image/*"
                        multiple
                        onChange={handlePhotoSelect}
                        disabled={photos.length >= 10}
                      />
                    </label>
                  </div>
                </div>

                {/* Photo Preview Grid */}
                {photos.length > 0 && (
                  <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                    {photos.map((photo, index) => (
                      <div key={index} className="relative group">
                        <img
                          src={photo.preview}
                          alt={photo.title}
                          className="w-full h-32 object-cover rounded-lg"
                        />
                        <button
                          type="button"
                          onClick={() => removePhoto(index)}
                          className="absolute top-2 right-2 p-1 bg-red-500 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
                        >
                          <X className="h-4 w-4" />
                        </button>
                        <input
                          type="text"
                          value={photo.title}
                          onChange={(e) => updatePhotoTitle(index, e.target.value)}
                          placeholder="Título da foto"
                          className="mt-2 block w-full text-xs rounded border-gray-300 px-2 py-1"
                        />
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Description */}
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                Descrição / Observações
              </label>
              <textarea
                id="description"
                name="description"
                rows={4}
                placeholder="Adicione observações, instruções especiais ou detalhes relevantes..."
                className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm"
                value={formData.description}
                onChange={handleChange}
              />
            </div>

            <div className="flex justify-end space-x-3">
              <button
                type="button"
                onClick={() => navigate(-1)}
                className="inline-flex items-center justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 tap-target"
              >
                Cancelar
              </button>
              <button
                type="submit"
                disabled={loading || uploadingPhotos || loadingTypes}
                className="inline-flex items-center justify-center rounded-md border border-transparent bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 tap-target disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading || uploadingPhotos ? (
                  <>
                    <Loader2 className="h-5 w-5 mr-2 animate-spin" />
                    {uploadingPhotos ? 'Enviando fotos...' : 'Salvando...'}
                  </>
                ) : (
                  <>
                    <Save className="h-5 w-5 mr-2" />
                    Salvar
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* Toast Notifications */}
      {toasts.map(toast => (
        <Toast
          key={toast.id}
          message={toast.message}
          type={toast.type}
          onClose={() => hideToast(toast.id)}
          duration={toast.duration}
        />
      ))}
    </div>
  )
}
