/**
 * Card Component
 * Componente de card padrão para conteúdo
 */
export default function Card({ 
  children, 
  className = '', 
  padding = 'default',
  hover = false 
}) {
  const paddingClasses = {
    none: '',
    sm: 'p-4',
    default: 'p-6',
    lg: 'p-8'
  }

  const hoverClass = hover ? 'hover:shadow-xl transition-shadow duration-200' : ''

  return (
    <div className={`bg-white rounded-xl shadow-md border border-gray-100 ${paddingClasses[padding]} ${hoverClass} ${className}`}>
      {children}
    </div>
  )
}
