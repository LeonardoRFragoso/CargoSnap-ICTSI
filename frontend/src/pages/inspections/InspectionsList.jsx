import { Link } from 'react-router-dom'
import { Plus, Search, Package } from 'lucide-react'
import { useAuthStore } from '../../store/authStore'
import PageContainer from '../../components/layout/PageContainer'
import PageHeader from '../../components/layout/PageHeader'
import Card from '../../components/layout/Card'
import EmptyState from '../../components/layout/EmptyState'
import Button from '../../components/ui/Button'

export default function InspectionsList() {
  const { canCreate } = useAuthStore()

  return (
    <PageContainer>
      <PageHeader
        title="Inspeções"
        description="Gerencie todas as suas inspeções de containers"
        icon={Package}
        actions={
          canCreate() && (
            <Link to="/inspections/new">
              <Button icon={Plus}>
                Nova Inspeção
              </Button>
            </Link>
          )
        }
      />

      {/* Search Bar */}
      <Card className="mb-6" padding="sm">
        <div className="relative">
          <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-4">
            <Search className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            placeholder="Buscar inspeções..."
            className="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-12 pr-4 text-sm placeholder-gray-500 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
          />
        </div>
      </Card>

      {/* Inspections List - Empty State */}
      <Card padding="none">
        <EmptyState
          icon={Package}
          title="Nenhuma inspeção encontrada"
          description="Comece criando sua primeira inspeção de container"
          action={
            canCreate() && (
              <Link to="/inspections/new">
                <Button icon={Plus}>
                  Nova Inspeção
                </Button>
              </Link>
            )
          }
        />
      </Card>
    </PageContainer>
  )
}
