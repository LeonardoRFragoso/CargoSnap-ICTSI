/**
 * PageContainer Component
 * Container padrão para todas as páginas do sistema
 */
export default function PageContainer({ children, className = '' }) {
  return (
    <div className={`min-h-screen bg-gray-50 ${className}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {children}
      </div>
    </div>
  )
}
