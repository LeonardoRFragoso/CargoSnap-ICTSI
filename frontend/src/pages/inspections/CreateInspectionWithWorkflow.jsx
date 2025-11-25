import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { Loader2, Workflow as WorkflowIcon, Info, Package, FileText, MapPin, User, Ship, Container, Truck } from 'lucide-react'
import { inspectionTypeService, inspectionService, photoService } from '../../services/inspectionService'
import { workflowService } from '../../services/workflowService'
import { useToast } from '../../hooks/useToast'
import Toast from '../../components/ui/Toast'
import WorkflowExecution from '../../components/workflow/WorkflowExecution'
import PageContainer from '../../components/layout/PageContainer'
import PageHeader from '../../components/layout/PageHeader'
import Card from '../../components/layout/Card'
import Button from '../../components/ui/Button'

/**
 * CreateInspectionWithWorkflow Component
 * Creates inspection and executes associated workflow
 */
export default function CreateInspectionWithWorkflow() {
  const navigate = useNavigate()
  const [step, setStep] = useState('basic') // 'basic' or 'workflow'
  const [formData, setFormData] = useState({
    title: '',
    inspection_type: null,
    external_reference: '',
    location: '',
    customer_name: '',
    // Container fields
    container_number: '',
    seal_number: '',
    booking_number: '',
    vessel_name: '',
    voyage_number: '',
    container_type: '',
    container_size: '',
    cargo_description: '',
    cargo_weight: '',
    // Vehicle fields
    vehicle_plate: '',
    vehicle_model: '',
    vehicle_year: '',
    vehicle_vin: '',
  })
  
  const [inspectionTypes, setInspectionTypes] = useState([])
  const [selectedWorkflow, setSelectedWorkflow] = useState(null)
  const [createdInspection, setCreatedInspection] = useState(null)
  const [loading, setLoading] = useState(false)
  const [loadingTypes, setLoadingTypes] = useState(true)
  const [loadingWorkflow, setLoadingWorkflow] = useState(false)
  
  const { toasts, hideToast, success, error: showError } = useToast()

  // Load workflow when type changes
  const loadWorkflowForType = useCallback(async (typeId) => {
    try {
      setLoadingWorkflow(true)
      const data = await workflowService.getByInspectionType(typeId)
      
      let workflows = []
      if (Array.isArray(data)) {
        workflows = data
      } else if (data.results && Array.isArray(data.results)) {
        workflows = data.results
      }
      
      // Find default workflow or use first one
      const selectedWorkflowSummary = workflows.find(w => w.is_default) || workflows[0]
      
      if (selectedWorkflowSummary) {
        // Fetch complete workflow details including steps
        const completeWorkflow = await workflowService.getById(selectedWorkflowSummary.id)
        setSelectedWorkflow(completeWorkflow)
      } else {
        setSelectedWorkflow(null)
      }
    } catch {
      // Silently handle error - workflow is optional
      // User will see "Nenhum workflow configurado" message
      setSelectedWorkflow(null)
    } finally {
      setLoadingWorkflow(false)
    }
  }, [])

  // Load inspection types
  useEffect(() => {
    const fetchInspectionTypes = async () => {
      try {
        setLoadingTypes(true)
        const data = await inspectionTypeService.getAll()
        
        let types = []
        if (Array.isArray(data)) {
          types = data
        } else if (data.results && Array.isArray(data.results)) {
          types = data.results
        } else if (data.data && Array.isArray(data.data)) {
          types = data.data
        }
        
        if (types.length > 0) {
          setInspectionTypes(types)
          setFormData(prev => ({ ...prev, inspection_type: types[0].id }))
          loadWorkflowForType(types[0].id)
        } else {
          const fallbackTypes = [
            { id: 1, name: 'Inspeção de Carga' },
            { id: 2, name: 'Inspeção de Container' },
            { id: 3, name: 'Inspeção de Veículo' },
          ]
          setInspectionTypes(fallbackTypes)
          setFormData(prev => ({ ...prev, inspection_type: fallbackTypes[0].id }))
        }
      } catch {
        showError('Erro ao carregar tipos de inspeção')
      } finally {
        setLoadingTypes(false)
      }
    }
    
    fetchInspectionTypes()
  }, [loadWorkflowForType, showError])

  // Handle type change
  const handleTypeChange = (e) => {
    const typeId = parseInt(e.target.value)
    setFormData(prev => ({ ...prev, inspection_type: typeId }))
    loadWorkflowForType(typeId)
  }

  // Handle basic form change
  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }))
  }

  // Create inspection
  const createInspection = async () => {
    if (!formData.title.trim()) {
      showError('Título é obrigatório')
      return
    }

    if (!formData.inspection_type) {
      showError('Tipo de inspeção é obrigatório')
      return
    }

    try {
      setLoading(true)
      
      // Clean empty string fields to avoid validation errors
      const inspectionData = Object.entries(formData).reduce((acc, [key, value]) => {
        // Only include non-empty values
        if (value !== '' && value !== null && value !== undefined) {
          acc[key] = value
        }
        return acc
      }, {})
      
      inspectionData.status = 'IN_PROGRESS'
      
      const inspection = await inspectionService.create(inspectionData)
      setCreatedInspection(inspection)
      
      success('Inspeção criada! Iniciando workflow...')
      
      // Move to workflow step
      setTimeout(() => {
        setStep('workflow')
      }, 1000)
      
    } catch (err) {
      // eslint-disable-next-line no-console
      console.error('Error creating inspection:', err)
      
      // Show specific validation errors if available
      if (err.response?.data) {
        const errors = err.response.data
        // eslint-disable-next-line no-console
        console.error('Validation errors:', errors)
        
        // Show first error message
        const firstError = Object.values(errors)[0]
        if (Array.isArray(firstError)) {
          showError(firstError[0])
        } else if (typeof firstError === 'string') {
          showError(firstError)
        } else {
          showError('Erro ao criar inspeção')
        }
      } else {
        showError('Erro ao criar inspeção')
      }
    } finally {
      setLoading(false)
    }
  }

  // Complete workflow
  const handleWorkflowComplete = async (workflowData) => {
    try {
      setLoading(true)
      
      // Upload photos from workflow
      if (workflowData.photos && Object.keys(workflowData.photos).length > 0) {
        for (const [stepId, stepPhotos] of Object.entries(workflowData.photos)) {
          for (const photo of stepPhotos) {
            await photoService.upload({
              inspection: createdInspection.id,
              photo: photo.file,
              title: photo.title,
            })
          }
        }
      }
      
      // Complete inspection
      await inspectionService.complete(createdInspection.id)
      
      success('Inspeção concluída com sucesso!')
      
      setTimeout(() => {
        navigate(`/inspections/${createdInspection.id}`)
      }, 1500)
      
    } catch (err) {
      // eslint-disable-next-line no-console
      console.error('Error completing workflow:', err)
      showError('Erro ao finalizar inspeção')
    } finally {
      setLoading(false)
    }
  }

  // Cancel workflow
  const handleWorkflowCancel = () => {
    if (window.confirm('Deseja cancelar esta inspeção?')) {
      navigate('/inspections')
    }
  }

  // Render workflow step
  if (step === 'workflow' && selectedWorkflow && createdInspection) {
    return (
      <WorkflowExecution
        workflow={selectedWorkflow}
        onComplete={handleWorkflowComplete}
        onCancel={handleWorkflowCancel}
      />
    )
  }

  // Render basic info step
  return (
    <PageContainer>
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Modern Header with Gradient */}
        <div className="relative bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 rounded-2xl shadow-2xl p-8 text-white overflow-hidden">
          <div className="absolute inset-0 opacity-10">
            <div className="absolute top-0 right-0 w-64 h-64 bg-white rounded-full blur-3xl transform translate-x-32 -translate-y-32"></div>
            <div className="absolute bottom-0 left-0 w-96 h-96 bg-blue-400 rounded-full blur-3xl transform -translate-x-48 translate-y-48"></div>
          </div>
          
          <div className="relative z-10">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-3 bg-white/20 rounded-xl backdrop-blur-sm">
                <Package className="h-8 w-8" />
              </div>
              <h1 className="text-3xl font-bold tracking-tight">Nova Inspeção</h1>
            </div>
            <p className="text-blue-100 text-base">Preencha as informações básicas e siga o workflow de inspeção</p>
          </div>
        </div>

        <Card className="shadow-lg border border-gray-100">
        <div className="space-y-8">
          {/* Tipo de Inspeção Section */}
          <div>
            <label htmlFor="inspection_type" className="block text-sm font-semibold text-gray-900 mb-2">
              Tipo de Inspeção *
            </label>
            <div className="relative">
              <select
                id="inspection_type"
                name="inspection_type"
                value={formData.inspection_type || ''}
                onChange={handleTypeChange}
                disabled={loadingTypes}
                className="mt-1 block w-full rounded-lg border-2 border-gray-200 px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none disabled:opacity-50 disabled:bg-gray-100 transition-all"
              >
                {loadingTypes ? (
                  <option>Carregando...</option>
                ) : (
                  inspectionTypes.map(type => (
                    <option key={type.id} value={type.id}>{type.name}</option>
                  ))
                )}
              </select>
            </div>
          </div>

          {/* Workflow Info - Modern Design */}
          {loadingWorkflow ? (
            <div className="flex items-center gap-3 p-5 bg-gradient-to-r from-gray-50 to-gray-100 rounded-xl border border-gray-200">
              <Loader2 className="h-6 w-6 animate-spin text-blue-600" />
              <span className="text-sm font-medium text-gray-700">Carregando workflow...</span>
            </div>
          ) : selectedWorkflow ? (
            <div className="p-6 bg-gradient-to-br from-blue-50 to-indigo-50 border-2 border-blue-200 rounded-xl shadow-sm">
              <div className="flex items-start gap-4">
                <div className="p-3 bg-blue-600 rounded-xl shadow-lg">
                  <WorkflowIcon className="h-6 w-6 text-white" />
                </div>
                <div className="flex-1">
                  <h3 className="text-base font-bold text-blue-900 mb-1">
                    Workflow: {selectedWorkflow.name}
                  </h3>
                  {selectedWorkflow.description && (
                    <p className="text-sm text-blue-700 mb-3">{selectedWorkflow.description}</p>
                  )}
                  <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-white/80 rounded-lg border border-blue-200">
                    <span className="text-sm font-semibold text-blue-900">{selectedWorkflow.steps?.length || 0} passos</span>
                    <span className="text-sm text-blue-600">a serem executados</span>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="p-6 bg-gradient-to-br from-yellow-50 to-orange-50 border-2 border-yellow-300 rounded-xl shadow-sm">
              <div className="flex items-start gap-4">
                <div className="p-3 bg-yellow-500 rounded-xl shadow-lg">
                  <Info className="h-6 w-6 text-white" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-yellow-900 mb-1">
                    Nenhum workflow configurado
                  </h3>
                  <p className="text-sm text-yellow-700">
                    Este tipo de inspeção não possui um workflow associado. A inspeção será criada sem passos guiados.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Basic Information Section */}
          <div className="space-y-6 p-6 bg-gray-50 rounded-xl border border-gray-200">
            <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
              <FileText className="h-5 w-5 text-blue-600" />
              Informações Básicas
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="md:col-span-2">
                <label htmlFor="title" className="block text-sm font-semibold text-gray-900 mb-2">
                  Título *
                </label>
                <input
                  type="text"
                  id="title"
                  name="title"
                  value={formData.title}
                  onChange={handleChange}
                  placeholder="Ex: Inspeção Container ABCD1234"
                  required
                  className="block w-full rounded-lg border-2 border-gray-200 px-4 py-3 text-gray-900 placeholder-gray-400 shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all"
                />
              </div>

              <div>
                <label htmlFor="external_reference" className="block text-sm font-semibold text-gray-900 mb-2">
                  Referência Externa
                </label>
                <input
                  type="text"
                  id="external_reference"
                  name="external_reference"
                  value={formData.external_reference}
                  onChange={handleChange}
                  placeholder="Ex: BL123456, Pedido #789"
                  className="block w-full rounded-lg border-2 border-gray-200 px-4 py-3 text-gray-900 placeholder-gray-400 shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all"
                />
              </div>

              <div>
                <label htmlFor="location" className="block text-sm font-semibold text-gray-900 mb-2 flex items-center gap-1">
                  <MapPin className="h-4 w-4 text-gray-600" />
                  Local
                </label>
                <input
                  type="text"
                  id="location"
                  name="location"
                  value={formData.location}
                  onChange={handleChange}
                  placeholder="Ex: Armazém 5, Porto de Santos"
                  className="block w-full rounded-lg border-2 border-gray-200 px-4 py-3 text-gray-900 placeholder-gray-400 shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all"
                />
              </div>

              <div>
                <label htmlFor="customer_name" className="block text-sm font-semibold text-gray-900 mb-2 flex items-center gap-1">
                  <User className="h-4 w-4 text-gray-600" />
                  Nome do Cliente
                </label>
                <input
                  type="text"
                  id="customer_name"
                  name="customer_name"
                  value={formData.customer_name}
                  onChange={handleChange}
                  placeholder="Ex: Empresa ABC Ltda"
                  className="block w-full rounded-lg border-2 border-gray-200 px-4 py-3 text-gray-900 placeholder-gray-400 shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all"
                />
              </div>
            </div>
          </div>

          {/* Container-specific fields */}
          {(inspectionTypes.find(t => t.id === formData.inspection_type)?.name?.toLowerCase().includes('container') ||
            inspectionTypes.find(t => t.id === formData.inspection_type)?.name?.toLowerCase().includes('carga')) && (
            <>
              <div className="p-6 bg-gradient-to-br from-cyan-50 to-blue-50 rounded-xl border-2 border-cyan-200">
                <h3 className="text-lg font-bold text-gray-900 mb-6 flex items-center gap-2">
                  <div className="p-2 bg-cyan-600 rounded-lg">
                    <Container className="h-5 w-5 text-white" />
                  </div>
                  Informações do Container/Carga
                </h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label htmlFor="container_number" className="block text-sm font-semibold text-gray-900 mb-2">
                      Número do Container
                    </label>
                    <input
                      type="text"
                      id="container_number"
                      name="container_number"
                      value={formData.container_number}
                      onChange={handleChange}
                      placeholder="Ex: ABCD1234567"
                      className="block w-full rounded-lg border-2 border-gray-200 px-4 py-3 text-gray-900 placeholder-gray-400 shadow-sm focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500 focus:outline-none transition-all"
                    />
                  </div>

                  <div>
                    <label htmlFor="seal_number" className="block text-sm font-semibold text-gray-900 mb-2">
                      Número do Lacre
                    </label>
                    <input
                      type="text"
                      id="seal_number"
                      name="seal_number"
                      value={formData.seal_number}
                      onChange={handleChange}
                      placeholder="Ex: SEAL123456"
                      className="block w-full rounded-lg border-2 border-gray-200 px-4 py-3 text-gray-900 placeholder-gray-400 shadow-sm focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500 focus:outline-none transition-all"
                    />
                  </div>

                  <div>
                    <label htmlFor="booking_number" className="block text-sm font-semibold text-gray-900 mb-2 flex items-center gap-1">
                      <FileText className="h-4 w-4 text-gray-600" />
                      Booking / BL Number
                    </label>
                    <input
                      type="text"
                      id="booking_number"
                      name="booking_number"
                      value={formData.booking_number}
                      onChange={handleChange}
                      placeholder="Ex: BL123456789"
                      className="block w-full rounded-lg border-2 border-gray-200 px-4 py-3 text-gray-900 placeholder-gray-400 shadow-sm focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500 focus:outline-none transition-all"
                    />
                  </div>

                  <div>
                    <label htmlFor="container_type" className="block text-sm font-semibold text-gray-900 mb-2">
                      Tipo de Container
                    </label>
                    <select
                      id="container_type"
                      name="container_type"
                      value={formData.container_type}
                      onChange={handleChange}
                      className="block w-full rounded-lg border-2 border-gray-200 px-4 py-3 text-gray-900 shadow-sm focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500 focus:outline-none transition-all"
                    >
                      <option value="">Selecione...</option>
                      <option value="20ft Standard">20ft Standard</option>
                      <option value="40ft Standard">40ft Standard</option>
                      <option value="40ft High Cube">40ft High Cube</option>
                      <option value="20ft Refrigerated">20ft Refrigerated</option>
                      <option value="40ft Refrigerated">40ft Refrigerated</option>
                      <option value="20ft Open Top">20ft Open Top</option>
                      <option value="40ft Open Top">40ft Open Top</option>
                      <option value="20ft Flat Rack">20ft Flat Rack</option>
                      <option value="40ft Flat Rack">40ft Flat Rack</option>
                    </select>
                  </div>

                  <div>
                    <label htmlFor="vessel_name" className="block text-sm font-semibold text-gray-900 mb-2 flex items-center gap-1">
                      <Ship className="h-4 w-4 text-gray-600" />
                      Nome do Navio
                    </label>
                    <input
                      type="text"
                      id="vessel_name"
                      name="vessel_name"
                      value={formData.vessel_name}
                      onChange={handleChange}
                      placeholder="Ex: MSC Mediterranean"
                      className="block w-full rounded-lg border-2 border-gray-200 px-4 py-3 text-gray-900 placeholder-gray-400 shadow-sm focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500 focus:outline-none transition-all"
                    />
                  </div>

                  <div>
                    <label htmlFor="voyage_number" className="block text-sm font-semibold text-gray-900 mb-2">
                      Número da Viagem
                    </label>
                    <input
                      type="text"
                      id="voyage_number"
                      name="voyage_number"
                      value={formData.voyage_number}
                      onChange={handleChange}
                      placeholder="Ex: V123"
                      className="block w-full rounded-lg border-2 border-gray-200 px-4 py-3 text-gray-900 placeholder-gray-400 shadow-sm focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500 focus:outline-none transition-all"
                    />
                </div>
                </div>
                
                <div className="mt-6 space-y-6">
                  <div>
                    <label htmlFor="cargo_description" className="block text-sm font-semibold text-gray-900 mb-2">
                      Descrição da Carga
                    </label>
                    <textarea
                      id="cargo_description"
                      name="cargo_description"
                      value={formData.cargo_description}
                      onChange={handleChange}
                      rows={4}
                      placeholder="Descreva o tipo de carga, quantidade, embalagem, etc."
                      className="block w-full rounded-lg border-2 border-gray-200 px-4 py-3 text-gray-900 placeholder-gray-400 shadow-sm focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500 focus:outline-none transition-all resize-none"
                    />
                  </div>

                  <div>
                    <label htmlFor="cargo_weight" className="block text-sm font-semibold text-gray-900 mb-2">
                      Peso da Carga (kg)
                    </label>
                    <input
                      type="number"
                      id="cargo_weight"
                      name="cargo_weight"
                      value={formData.cargo_weight}
                      onChange={handleChange}
                      placeholder="Ex: 25000"
                      step="0.01"
                      className="block w-full rounded-lg border-2 border-gray-200 px-4 py-3 text-gray-900 placeholder-gray-400 shadow-sm focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500 focus:outline-none transition-all"
                    />
                  </div>
                </div>
              </div>
            </>
          )}

          {/* Vehicle-specific fields */}
          {inspectionTypes.find(t => t.id === formData.inspection_type)?.name?.toLowerCase().includes('veículo') && (
            <>
              <div className="p-6 bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl border-2 border-purple-200">
                <h3 className="text-lg font-bold text-gray-900 mb-6 flex items-center gap-2">
                  <div className="p-2 bg-purple-600 rounded-lg">
                    <Truck className="h-5 w-5 text-white" />
                  </div>
                  Informações do Veículo
                </h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label htmlFor="vehicle_plate" className="block text-sm font-semibold text-gray-900 mb-2">
                      Placa do Veículo *
                    </label>
                    <input
                      type="text"
                      id="vehicle_plate"
                      name="vehicle_plate"
                      value={formData.vehicle_plate}
                      onChange={handleChange}
                      placeholder="Ex: ABC-1234"
                      className="block w-full rounded-lg border-2 border-gray-200 px-4 py-3 text-gray-900 placeholder-gray-400 shadow-sm focus:border-purple-500 focus:ring-2 focus:ring-purple-500 focus:outline-none transition-all"
                    />
                  </div>

                  <div>
                    <label htmlFor="vehicle_model" className="block text-sm font-semibold text-gray-900 mb-2">
                      Modelo do Veículo
                    </label>
                    <input
                      type="text"
                      id="vehicle_model"
                      name="vehicle_model"
                      value={formData.vehicle_model}
                      onChange={handleChange}
                      placeholder="Ex: Scania R450"
                      className="block w-full rounded-lg border-2 border-gray-200 px-4 py-3 text-gray-900 placeholder-gray-400 shadow-sm focus:border-purple-500 focus:ring-2 focus:ring-purple-500 focus:outline-none transition-all"
                    />
                  </div>

                  <div>
                    <label htmlFor="vehicle_year" className="block text-sm font-semibold text-gray-900 mb-2">
                      Ano do Veículo
                    </label>
                    <input
                      type="number"
                      id="vehicle_year"
                      name="vehicle_year"
                      value={formData.vehicle_year}
                      onChange={handleChange}
                      placeholder="Ex: 2023"
                      min="1900"
                      max="2099"
                      className="block w-full rounded-lg border-2 border-gray-200 px-4 py-3 text-gray-900 placeholder-gray-400 shadow-sm focus:border-purple-500 focus:ring-2 focus:ring-purple-500 focus:outline-none transition-all"
                    />
                  </div>

                  <div>
                    <label htmlFor="vehicle_vin" className="block text-sm font-semibold text-gray-900 mb-2">
                      Chassi (VIN)
                    </label>
                    <input
                      type="text"
                      id="vehicle_vin"
                      name="vehicle_vin"
                      value={formData.vehicle_vin}
                      onChange={handleChange}
                      placeholder="Ex: 9BWZZZ377VT004251"
                      className="block w-full rounded-lg border-2 border-gray-200 px-4 py-3 text-gray-900 placeholder-gray-400 shadow-sm focus:border-purple-500 focus:ring-2 focus:ring-purple-500 focus:outline-none transition-all"
                    />
                  </div>
                </div>
              </div>
            </>
          )}
        </div>

        {/* Actions - Modern Design */}
        <div className="mt-8 pt-6 border-t-2 border-gray-200 flex justify-end gap-4">
          <Button
            variant="secondary"
            onClick={() => navigate(-1)}
            className="px-6 py-3 text-base font-semibold"
          >
            Cancelar
          </Button>
          <Button
            onClick={createInspection}
            disabled={!formData.title.trim()}
            loading={loading}
            className="px-8 py-3 text-base font-semibold shadow-lg hover:shadow-xl transition-all"
          >
            {selectedWorkflow ? '🚀 Criar e Iniciar Workflow' : '✓ Criar Inspeção'}
          </Button>
        </div>
      </Card>

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
    </PageContainer>
  )
}
