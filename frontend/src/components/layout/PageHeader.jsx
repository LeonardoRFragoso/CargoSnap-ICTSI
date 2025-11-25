import { ArrowLeft } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

/**
 * PageHeader Component
 * Componente padrão para cabeçalhos de página com título, descrição e ações
 */
export default function PageHeader({ 
  title, 
  description, 
  showBackButton = false, 
  backTo,
  actions,
  icon: Icon 
}) {
  const navigate = useNavigate()

  const handleBack = () => {
    if (backTo) {
      navigate(backTo)
    } else {
      navigate(-1)
    }
  }

  return (
    <div className="mb-6">
      {/* Back Button */}
      {showBackButton && (
        <button
          onClick={handleBack}
          className="inline-flex items-center text-sm font-medium text-gray-500 hover:text-gray-700 mb-4 transition-colors"
        >
          <ArrowLeft className="h-5 w-5 mr-2" />
          Voltar
        </button>
      )}

      {/* Header Content */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div className="flex items-start gap-3">
          {Icon && (
            <div className="p-2 bg-blue-100 rounded-lg flex-shrink-0">
              <Icon className="h-6 w-6 text-blue-600" />
            </div>
          )}
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{title}</h1>
            {description && (
              <p className="mt-1 text-sm text-gray-600">{description}</p>
            )}
          </div>
        </div>

        {/* Actions */}
        {actions && (
          <div className="flex items-center gap-3">
            {actions}
          </div>
        )}
      </div>
    </div>
  )
}
