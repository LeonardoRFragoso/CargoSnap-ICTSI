import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'

export default function InspectionDetail() {
  const { id } = useParams()
  const navigate = useNavigate()

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
          <h1 className="text-2xl font-bold text-gray-900 mb-4">
            Inspeção #{id}
          </h1>
          <p className="text-sm text-gray-500">
            Detalhes da inspeção serão exibidos aqui.
          </p>
        </div>
      </div>
    </div>
  )
}
