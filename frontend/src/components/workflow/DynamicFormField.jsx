import { useState } from 'react'
import { Calendar, Clock, Upload, X } from 'lucide-react'

/**
 * DynamicFormField Component
 * Renders different field types based on configuration
 */
export default function DynamicFormField({ field, value, onChange, error }) {
  const [fileName, setFileName] = useState('')

  const handleChange = (e) => {
    const newValue = e.target.type === 'checkbox' ? e.target.checked : e.target.value
    onChange(field.id, newValue)
  }

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      setFileName(file.name)
      onChange(field.id, file)
    }
  }

  const renderField = () => {
    const baseClasses = `mt-1 block w-full rounded-md border px-3 py-2 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 sm:text-sm ${
      error ? 'border-red-300 focus:border-red-500' : 'border-gray-300 focus:border-blue-500'
    }`

    switch (field.field_type) {
      case 'TEXT':
        return (
          <input
            type="text"
            value={value || ''}
            onChange={handleChange}
            placeholder={field.placeholder}
            required={field.is_required}
            minLength={field.min_length}
            maxLength={field.max_length}
            pattern={field.pattern}
            className={baseClasses}
          />
        )

      case 'NUMBER':
        return (
          <input
            type="number"
            value={value || ''}
            onChange={handleChange}
            placeholder={field.placeholder}
            required={field.is_required}
            min={field.min_value}
            max={field.max_value}
            step="any"
            className={baseClasses}
          />
        )

      case 'EMAIL':
        return (
          <input
            type="email"
            value={value || ''}
            onChange={handleChange}
            placeholder={field.placeholder}
            required={field.is_required}
            className={baseClasses}
          />
        )

      case 'PHONE':
        return (
          <input
            type="tel"
            value={value || ''}
            onChange={handleChange}
            placeholder={field.placeholder}
            required={field.is_required}
            className={baseClasses}
          />
        )

      case 'URL':
        return (
          <input
            type="url"
            value={value || ''}
            onChange={handleChange}
            placeholder={field.placeholder}
            required={field.is_required}
            className={baseClasses}
          />
        )

      case 'DATE':
        return (
          <div className="relative">
            <input
              type="date"
              value={value || ''}
              onChange={handleChange}
              required={field.is_required}
              className={baseClasses}
            />
            <Calendar className="absolute right-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400 pointer-events-none" />
          </div>
        )

      case 'TIME':
        return (
          <div className="relative">
            <input
              type="time"
              value={value || ''}
              onChange={handleChange}
              required={field.is_required}
              className={baseClasses}
            />
            <Clock className="absolute right-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400 pointer-events-none" />
          </div>
        )

      case 'DATETIME':
        return (
          <input
            type="datetime-local"
            value={value || ''}
            onChange={handleChange}
            required={field.is_required}
            className={baseClasses}
          />
        )

      case 'TEXTAREA':
        return (
          <textarea
            value={value || ''}
            onChange={handleChange}
            placeholder={field.placeholder}
            required={field.is_required}
            minLength={field.min_length}
            maxLength={field.max_length}
            rows={4}
            className={baseClasses}
          />
        )

      case 'SELECT':
        return (
          <select
            value={value || ''}
            onChange={handleChange}
            required={field.is_required}
            className={baseClasses}
          >
            <option value="">Selecione...</option>
            {field.options?.map((option, index) => (
              <option key={index} value={option.value || option}>
                {option.label || option}
              </option>
            ))}
          </select>
        )

      case 'MULTISELECT':
        return (
          <select
            multiple
            value={value || []}
            onChange={(e) => {
              const selected = Array.from(e.target.selectedOptions, option => option.value)
              onChange(field.id, selected)
            }}
            required={field.is_required}
            className={`${baseClasses} h-32`}
          >
            {field.options?.map((option, index) => (
              <option key={index} value={option.value || option}>
                {option.label || option}
              </option>
            ))}
          </select>
        )

      case 'CHECKBOX':
        return (
          <div className="flex items-center">
            <input
              type="checkbox"
              checked={value || false}
              onChange={handleChange}
              required={field.is_required}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label className="ml-2 text-sm text-gray-700">
              {field.placeholder || 'Sim'}
            </label>
          </div>
        )

      case 'RADIO':
        return (
          <div className="space-y-2">
            {field.options?.map((option, index) => (
              <div key={index} className="flex items-center">
                <input
                  type="radio"
                  name={`field_${field.id}`}
                  value={option.value || option}
                  checked={value === (option.value || option)}
                  onChange={handleChange}
                  required={field.is_required}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
                />
                <label className="ml-2 text-sm text-gray-700">
                  {option.label || option}
                </label>
              </div>
            ))}
          </div>
        )

      case 'FILE':
        return (
          <div>
            <label className="flex items-center justify-center w-full px-4 py-2 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer hover:bg-gray-50">
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <Upload className="h-5 w-5" />
                <span>{fileName || 'Escolher arquivo'}</span>
              </div>
              <input
                type="file"
                onChange={handleFileChange}
                required={field.is_required}
                className="hidden"
              />
            </label>
            {fileName && (
              <div className="mt-2 flex items-center justify-between text-sm text-gray-600">
                <span>{fileName}</span>
                <button
                  type="button"
                  onClick={() => {
                    setFileName('')
                    onChange(field.id, null)
                  }}
                  className="text-red-500 hover:text-red-700"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>
            )}
          </div>
        )

      default:
        return (
          <input
            type="text"
            value={value || ''}
            onChange={handleChange}
            placeholder={field.placeholder}
            className={baseClasses}
          />
        )
    }
  }

  // Check if field should be shown based on conditional logic
  const shouldShow = () => {
    // TODO: Implement conditional logic based on show_if_field and show_if_value
    return true
  }

  if (!shouldShow()) {
    return null
  }

  // Determine field width class
  const widthClass = {
    'full': 'col-span-2',
    'half': 'col-span-1',
    'third': 'col-span-1',
    'quarter': 'col-span-1',
  }[field.width] || 'col-span-2'

  return (
    <div className={widthClass}>
      <label className="block text-sm font-medium text-gray-700">
        {field.label}
        {field.is_required && <span className="text-red-500 ml-1">*</span>}
      </label>
      
      {renderField()}
      
      {field.help_text && (
        <p className="mt-1 text-sm text-gray-500">{field.help_text}</p>
      )}
      
      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}
    </div>
  )
}
