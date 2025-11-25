/**
 * PageContainer Component
 * Container padrão para todas as páginas do sistema
 * MainLayout já fornece padding horizontal e max-width, este componente apenas adiciona padding vertical
 */
export default function PageContainer({ children, className = '' }) {
  return (
    <div className={`space-y-6 ${className}`}>
      {children}
    </div>
  )
}
