import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Loader2, Workflow as WorkflowIcon, Info, Package } from 'lucide-react'
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
  }, [showError])

  // Load workflow when type changes
  const loadWorkflowForType = async (typeId) => {
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
      const defaultWorkflow = workflows.find(w => w.is_default) || workflows[0]
      setSelectedWorkflow(defaultWorkflow || null)
    } catch {
      // Silently handle error - workflow is optional
      // User will see "Nenhum workflow configurado" message
      setSelectedWorkflow(null)
    } finally {
      setLoadingWorkflow(false)
    }
  }

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

    try {
      setLoading(true)
      
      const inspectionData = {
        ...formData,
        status: 'IN_PROGRESS',
      }
      
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
      showError('Erro ao criar inspeção')
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
    <PageContainer className="max-w-4xl">
      <PageHeader
        title="Nova Inspeção"
        description="Preencha as informações básicas e siga o workflow de inspeção"
        icon={Package}
        showBackButton
      />

      <Card>
        <div className="space-y-6">
          <div>
            <label htmlFor="inspection_type" className="block text-sm font-medium text-gray-700">
              Tipo de Inspeção *
            </label>
            <select
              id="inspection_type"
              name="inspection_type"
              value={formData.inspection_type || ''}
              onChange={handleTypeChange}
              disabled={loadingTypes}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 disabled:opacity-50"
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

          {/* Workflow Info */}
          {loadingWorkflow ? (
            <div className="flex items-center gap-2 p-4 bg-gray-50 rounded-lg">
              <Loader2 className="h-5 w-5 animate-spin text-gray-400" />
              <span className="text-sm text-gray-600">Carregando workflow...</span>
            </div>
          ) : selectedWorkflow ? (
            <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <div className="flex items-start gap-3">
                <WorkflowIcon className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                  <h3 className="text-sm font-medium text-blue-900">
                    Workflow: {selectedWorkflow.name}
                  </h3>
                  {selectedWorkflow.description && (
                    <p className="mt-1 text-sm text-blue-700">{selectedWorkflow.description}</p>
                  )}
                  <div className="mt-2 text-sm text-blue-700">
                    <strong>{selectedWorkflow.steps?.length || 0} passos</strong> a serem executados
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <div className="flex items-start gap-3">
                <Info className="h-5 w-5 text-yellow-600 flex-shrink-0 mt-0.5" />
                <div>
                  <h3 className="text-sm font-medium text-yellow-900">
                    Nenhum workflow configurado
                  </h3>
                  <p className="mt-1 text-sm text-yellow-700">
                    Este tipo de inspeção não possui um workflow associado. A inspeção será criada sem passos guiados.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Title */}
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-gray-700">
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
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
            />
          </div>

          {/* External Reference */}
          <div>
            <label htmlFor="external_reference" className="block text-sm font-medium text-gray-700">
              Referência Externa
            </label>
            <input
              type="text"
              id="external_reference"
              name="external_reference"
              value={formData.external_reference}
              onChange={handleChange}
              placeholder="Ex: BL123456, Pedido #789"
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
            />
          </div>

          {/* Location */}
          <div>
            <label htmlFor="location" className="block text-sm font-medium text-gray-700">
              Local
            </label>
            <input
              type="text"
              id="location"
              name="location"
              value={formData.location}
              onChange={handleChange}
              placeholder="Ex: Armazém 5, Porto de Santos"
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
            />
          </div>

          {/* Customer Name */}
          <div>
            <label htmlFor="customer_name" className="block text-sm font-medium text-gray-700">
              Nome do Cliente
            </label>
            <input
              type="text"
              id="customer_name"
              name="customer_name"
              value={formData.customer_name}
              onChange={handleChange}
              placeholder="Ex: Empresa ABC Ltda"
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
            />
          </div>

          {/* Container-specific fields */}
          {(inspectionTypes.find(t => t.id === formData.inspection_type)?.name?.toLowerCase().includes('container') ||
            inspectionTypes.find(t => t.id === formData.inspection_type)?.name?.toLowerCase().includes('carga')) && (
            <>
              <div className="border-t border-gray-200 pt-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Informações do Container/Carga</h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label htmlFor="container_number" className="block text-sm font-medium text-gray-700">
                      Número do Container
                    </label>
                    <input
                      type="text"
                      id="container_number"
                      name="container_number"
                      value={formData.container_number}
                      onChange={handleChange}
                      placeholder="Ex: ABCD1234567"
                      className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
                    />
                  </div>

                  <div>
                    <label htmlFor="seal_number" className="block text-sm font-medium text-gray-700">
                      Número do Lacre
                    </label>
                    <input
                      type="text"
                      id="seal_number"
                      name="seal_number"
                      value={formData.seal_number}
                      onChange={handleChange}
                      placeholder="Ex: SEAL123456"
                      className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
                    />
                  </div>

                  <div>
                    <label htmlFor="booking_number" className="block text-sm font-medium text-gray-700">
                      Booking / BL Number
                    </label>
                    <input
                      type="text"
                      id="booking_number"
                      name="booking_number"
                      value={formData.booking_number}
                      onChange={handleChange}
                      placeholder="Ex: BL123456789"
                      className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
                    />
                  </div>

                  <div>
                    <label htmlFor="container_type" className="block text-sm font-medium text-gray-700">
                      Tipo de Container
                    </label>
                    <select
                      id="container_type"
                      name="container_type"
                      value={formData.container_type}
                      onChange={handleChange}
                      className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
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
                    <label htmlFor="vessel_name" className="block text-sm font-medium text-gray-700">
                      Nome do Navio
                    </label>
                    <input
                      type="text"
                      id="vessel_name"
                      name="vessel_name"
                      value={formData.vessel_name}
                      onChange={handleChange}
                      placeholder="Ex: MSC Mediterranean"
                      className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
                    />
                  </div>

                  <div>
                    <label htmlFor="voyage_number" className="block text-sm font-medium text-gray-700">
                      Número da Viagem
                    </label>
                    <input
                      type="text"
                      id="voyage_number"
                      name="voyage_number"
                      value={formData.voyage_number}
                      onChange={handleChange}
                      placeholder="Ex: V123"
                      className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
                    />
                </div>
                
                <div className="mt-6 space-y-6">
                  <div>
                    <label htmlFor="cargo_description" className="block text-sm font-medium text-gray-700">
                      Descrição da Carga
                    </label>
                    <textarea
                      id="cargo_description"
                      name="cargo_description"
                      value={formData.cargo_description}
                      onChange={handleChange}
                      rows={3}
                      placeholder="Descreva o tipo de carga, quantidade, embalagem, etc."
                      className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
                    />
                  </div>

                  <div>
                    <label htmlFor="cargo_weight" className="block text-sm font-medium text-gray-700">
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
                      className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
                    />
                  </div>
                </div>
              </div>
            </>
          )}

          {/* Vehicle-specific fields */}
          {inspectionTypes.find(t => t.id === formData.inspection_type)?.name?.toLowerCase().includes('veículo') && (
            <>
              <div className="border-t border-gray-200 pt-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Informações do Veículo</h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label htmlFor="vehicle_plate" className="block text-sm font-medium text-gray-700">
                      Placa do Veículo *
                    </label>
                    <input
                      type="text"
                      id="vehicle_plate"
                      name="vehicle_plate"
                      value={formData.vehicle_plate}
                      onChange={handleChange}
                      placeholder="Ex: ABC-1234"
                      className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
                    />
                  </div>

                  <div>
                    <label htmlFor="vehicle_model" className="block text-sm font-medium text-gray-700">
                      Modelo do Veículo
                    </label>
                    <input
                      type="text"
                      id="vehicle_model"
                      name="vehicle_model"
                      value={formData.vehicle_model}
                      onChange={handleChange}
                      placeholder="Ex: Scania R450"
                      className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
                    />
                  </div>

                  <div>
                    <label htmlFor="vehicle_year" className="block text-sm font-medium text-gray-700">
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
                      className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
                    />
                  </div>

                  <div>
                    <label htmlFor="vehicle_vin" className="block text-sm font-medium text-gray-700">
                      Chassi (VIN)
                    </label>
                    <input
                      type="text"
                      id="vehicle_vin"
                      name="vehicle_vin"
                      value={formData.vehicle_vin}
                      onChange={handleChange}
                      placeholder="Ex: 9BWZZZ377VT004251"
                      className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
                    />
                  </div>
                </div>
              </div>
            </>
          )}
        </div>

        {/* Actions */}
        <div className="mt-6 pt-6 border-t border-gray-200 flex justify-end gap-3">
          <Button
            variant="secondary"
            onClick={() => navigate(-1)}
          >
            Cancelar
          </Button>
          <Button
            onClick={createInspection}
            disabled={!formData.title.trim()}
            loading={loading}
          >
            {selectedWorkflow ? 'Criar e Iniciar Workflow' : 'Criar Inspeção'}
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
    </PageContainer>
  )
}
