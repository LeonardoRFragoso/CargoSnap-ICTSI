/**
 * EmptyState Component
 * Componente padrão para estados vazios
 */
export default function EmptyState({ 
  icon: Icon, 
  title, 
  description, 
  action 
}) {
  return (
    <div className="px-6 py-16 text-center">
      <div className="max-w-sm mx-auto">
        {/* Icon with animation */}
        {Icon && (
          <div className="relative mb-6">
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-24 h-24 bg-blue-100 rounded-full animate-pulse"></div>
            </div>
            <div className="relative">
              <Icon className="mx-auto h-16 w-16 text-blue-400" strokeWidth={1.5} />
            </div>
          </div>
        )}
        
        {/* Title */}
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          {title}
        </h3>
        
        {/* Description */}
        {description && (
          <p className="text-sm text-gray-500 mb-6">
            {description}
          </p>
        )}
        
        {/* Action Button */}
        {action}
      </div>
    </div>
  )
}
