import { useState, useEffect } from 'react'
import { ChevronLeft, ChevronRight, Check, Camera, Edit, FileText, PenTool, AlertCircle, X } from 'lucide-react'
import DynamicFormField from './DynamicFormField'
import CameraCapture from './CameraCapture'
import { useToast } from '../../hooks/useToast'
import Toast from '../ui/Toast'

/**
 * WorkflowExecution Component
 * Handles step-by-step workflow execution
 */
export default function WorkflowExecution({ workflow, onComplete, onCancel }) {
  const [currentStepIndex, setCurrentStepIndex] = useState(0)
  const [stepData, setStepData] = useState({})
  const [stepErrors, setStepErrors] = useState({})
  const [photos, setPhotos] = useState({}) // { stepId: [photos] }
  const [showCamera, setShowCamera] = useState(false)
  const [completedSteps, setCompletedSteps] = useState(new Set())
  
  const { success, error: showError, warning } = useToast()
  
  const currentStep = workflow.steps[currentStepIndex]
  const totalSteps = workflow.steps.length
  const progress = ((currentStepIndex + 1) / totalSteps) * 100

  // Initialize step data
  useEffect(() => {
    const initialData = {}
    workflow.steps.forEach(step => {
      if (step.step_type === 'FORM' && step.forms) {
        step.forms.forEach(form => {
          form.fields.forEach(field => {
            if (field.default_value) {
              initialData[field.id] = field.default_value
            }
          })
        })
      }
    })
    setStepData(initialData)
  }, [workflow])

  // Handle field change
  const handleFieldChange = (fieldId, value) => {
    setStepData(prev => ({
      ...prev,
      [fieldId]: value
    }))
    
    // Clear error for this field
    if (stepErrors[fieldId]) {
      setStepErrors(prev => {
        const newErrors = { ...prev }
        delete newErrors[fieldId]
        return newErrors
      })
    }
  }

  // Handle photo capture
  const handlePhotoCapture = (file, url) => {
    const stepId = currentStep.id
    setPhotos(prev => ({
      ...prev,
      [stepId]: [...(prev[stepId] || []), { file, url, title: `Foto ${(prev[stepId]?.length || 0) + 1}` }]
    }))
    success('Foto capturada com sucesso!')
  }

  // Remove photo
  const removePhoto = (stepId, index) => {
    setPhotos(prev => {
      const newPhotos = { ...prev }
      URL.revokeObjectURL(newPhotos[stepId][index].url)
      newPhotos[stepId] = newPhotos[stepId].filter((_, i) => i !== index)
      return newPhotos
    })
  }

  // Validate current step
  const validateStep = () => {
    const errors = {}
    
    if (currentStep.step_type === 'FORM' && currentStep.forms) {
      currentStep.forms.forEach(form => {
        form.fields.forEach(field => {
          if (field.is_required && !stepData[field.id]) {
            errors[field.id] = 'Campo obrigatório'
          }
          
          // Validate email
          if (field.field_type === 'EMAIL' && stepData[field.id]) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
            if (!emailRegex.test(stepData[field.id])) {
              errors[field.id] = 'Email inválido'
            }
          }
          
          // Validate number range
          if (field.field_type === 'NUMBER' && stepData[field.id]) {
            const value = parseFloat(stepData[field.id])
            if (field.min_value && value < field.min_value) {
              errors[field.id] = `Valor mínimo: ${field.min_value}`
            }
            if (field.max_value && value > field.max_value) {
              errors[field.id] = `Valor máximo: ${field.max_value}`
            }
          }
          
          // Validate string length
          if (['TEXT', 'TEXTAREA'].includes(field.field_type) && stepData[field.id]) {
            const length = stepData[field.id].length
            if (field.min_length && length < field.min_length) {
              errors[field.id] = `Mínimo ${field.min_length} caracteres`
            }
            if (field.max_length && length > field.max_length) {
              errors[field.id] = `Máximo ${field.max_length} caracteres`
            }
          }
        })
      })
    }
    
    // Validate photos for PHOTO step
    if (currentStep.step_type === 'PHOTO') {
      const stepPhotos = photos[currentStep.id] || []
      if (currentStep.min_photos && stepPhotos.length < currentStep.min_photos) {
        errors.photos = `Mínimo de ${currentStep.min_photos} fotos necessário`
      }
      if (currentStep.max_photos && stepPhotos.length > currentStep.max_photos) {
        errors.photos = `Máximo de ${currentStep.max_photos} fotos permitido`
      }
    }
    
    setStepErrors(errors)
    return Object.keys(errors).length === 0
  }

  // Go to next step
  const nextStep = () => {
    if (!validateStep()) {
      warning('Por favor, preencha todos os campos obrigatórios')
      return
    }
    
    setCompletedSteps(prev => new Set([...prev, currentStepIndex]))
    
    if (currentStepIndex < totalSteps - 1) {
      setCurrentStepIndex(prev => prev + 1)
      setStepErrors({})
    } else {
      completeWorkflow()
    }
  }

  // Go to previous step
  const previousStep = () => {
    if (currentStepIndex > 0) {
      setCurrentStepIndex(prev => prev - 1)
      setStepErrors({})
    }
  }

  // Skip step (if allowed)
  const skipStep = () => {
    if (currentStep.is_skippable || workflow.allow_skip_steps) {
      if (currentStepIndex < totalSteps - 1) {
        setCurrentStepIndex(prev => prev + 1)
        setStepErrors({})
      }
    }
  }

  // Complete workflow
  const completeWorkflow = () => {
    const workflowData = {
      workflow_id: workflow.id,
      step_data: stepData,
      photos: photos,
      completed_steps: Array.from(completedSteps)
    }
    
    onComplete(workflowData)
  }

  // Render step icon
  const getStepIcon = (stepType) => {
    const icons = {
      'FORM': <FileText className="h-5 w-5" />,
      'PHOTO': <Camera className="h-5 w-5" />,
      'VIDEO': <Camera className="h-5 w-5" />,
      'SCAN': <Edit className="h-5 w-5" />,
      'SIGNATURE': <PenTool className="h-5 w-5" />,
      'APPROVAL': <Check className="h-5 w-5" />,
    }
    return icons[stepType] || <FileText className="h-5 w-5" />
  }

  // Render step content
  const renderStepContent = () => {
    switch (currentStep.step_type) {
      case 'FORM':
        return (
          <div className="space-y-6">
            {currentStep.forms?.map(form => (
              <div key={form.id} className="space-y-4">
                <h3 className="text-lg font-medium text-gray-900">{form.name}</h3>
                {form.description && (
                  <p className="text-sm text-gray-600">{form.description}</p>
                )}
                
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {form.fields?.map(field => (
                    <DynamicFormField
                      key={field.id}
                      field={field}
                      value={stepData[field.id]}
                      onChange={handleFieldChange}
                      error={stepErrors[field.id]}
                    />
                  ))}
                </div>
              </div>
            ))}
          </div>
        )

      case 'PHOTO':
        const stepPhotos = photos[currentStep.id] || []
        return (
          <div className="space-y-4">
            <div className="text-center">
              <Camera className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900">{currentStep.name}</h3>
              {currentStep.description && (
                <p className="text-sm text-gray-600 mt-2">{currentStep.description}</p>
              )}
              
              <div className="mt-4 text-sm text-gray-600">
                {stepPhotos.length}/{currentStep.max_photos || '∞'} fotos
                {currentStep.min_photos && (
                  <span className="ml-2 text-gray-500">
                    (mínimo: {currentStep.min_photos})
                  </span>
                )}
              </div>
            </div>

            {stepErrors.photos && (
              <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                <AlertCircle className="h-5 w-5 flex-shrink-0" />
                {stepErrors.photos}
              </div>
            )}

            {stepPhotos.length > 0 && (
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
                {stepPhotos.map((photo, index) => (
                  <div key={index} className="relative group">
                    <img
                      src={photo.url}
                      alt={photo.title}
                      className="w-full h-32 object-cover rounded-lg"
                    />
                    <button
                      onClick={() => removePhoto(currentStep.id, index)}
                      className="absolute top-2 right-2 p-1 bg-red-500 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </div>
                ))}
              </div>
            )}

            <button
              onClick={() => setShowCamera(true)}
              disabled={currentStep.max_photos && stepPhotos.length >= currentStep.max_photos}
              className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Camera className="h-5 w-5" />
              Capturar Foto
            </button>
          </div>
        )

      case 'SIGNATURE':
        return (
          <div className="text-center space-y-4">
            <PenTool className="h-16 w-16 text-gray-400 mx-auto" />
            <h3 className="text-lg font-medium text-gray-900">{currentStep.name}</h3>
            <p className="text-sm text-gray-600">Funcionalidade de assinatura em desenvolvimento</p>
          </div>
        )

      default:
        return (
          <div className="text-center space-y-4">
            {getStepIcon(currentStep.step_type)}
            <h3 className="text-lg font-medium text-gray-900">{currentStep.name}</h3>
            {currentStep.description && (
              <p className="text-sm text-gray-600">{currentStep.description}</p>
            )}
          </div>
        )
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      {/* Header */}
      <div className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between mb-2">
            <h2 className="text-lg font-semibold text-gray-900">{workflow.name}</h2>
            <span className="text-sm text-gray-600">
              Step {currentStepIndex + 1} de {totalSteps}
            </span>
          </div>
          
          {/* Progress Bar */}
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-4 py-6">
        <div className="bg-white rounded-lg shadow-sm p-6">
          {renderStepContent()}
        </div>
      </div>

      {/* Navigation */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-4 safe-bottom">
        <div className="max-w-4xl mx-auto flex items-center justify-between gap-3">
          <button
            onClick={previousStep}
            disabled={currentStepIndex === 0}
            className="flex items-center gap-2 px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ChevronLeft className="h-5 w-5" />
            Anterior
          </button>

          {(currentStep.is_skippable || workflow.allow_skip_steps) && currentStepIndex < totalSteps - 1 && (
            <button
              onClick={skipStep}
              className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
            >
              Pular
            </button>
          )}

          <button
            onClick={currentStepIndex === totalSteps - 1 ? completeWorkflow : nextStep}
            className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors ml-auto"
          >
            {currentStepIndex === totalSteps - 1 ? (
              <>
                <Check className="h-5 w-5" />
                Concluir
              </>
            ) : (
              <>
                Próximo
                <ChevronRight className="h-5 w-5" />
              </>
            )}
          </button>
        </div>
      </div>

      {/* Camera Modal */}
      {showCamera && (
        <CameraCapture
          onCapture={handlePhotoCapture}
          onClose={() => setShowCamera(false)}
          maxPhotos={currentStep.max_photos || 10}
          currentCount={photos[currentStep.id]?.length || 0}
        />
      )}
    </div>
  )
}

// Note: Toasts are managed by parent component (CreateInspectionWithWorkflow)
