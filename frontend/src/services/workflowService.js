import api from './api'

/**
 * Workflow Service
 * Handles all API calls related to workflows
 */

// Workflows
export const workflowService = {
  getAll: async (params = {}) => {
    const response = await api.get('/workflows/workflows/', { params })
    return response.data
  },
  
  getById: async (id) => {
    const response = await api.get(`/workflows/workflows/${id}/`)
    return response.data
  },
  
  getByInspectionType: async (typeId) => {
    const response = await api.get('/workflows/workflows/', {
      params: { inspection_type: typeId }
    })
    return response.data
  },
  
  create: async (data) => {
    const response = await api.post('/workflows/workflows/', data)
    return response.data
  },
  
  duplicate: async (id) => {
    const response = await api.post(`/workflows/workflows/${id}/duplicate/`)
    return response.data
  },
}

// Workflow Executions
export const executionService = {
  getAll: async (params = {}) => {
    const response = await api.get('/workflows/executions/', { params })
    return response.data
  },
  
  getById: async (id) => {
    const response = await api.get(`/workflows/executions/${id}/`)
    return response.data
  },
  
  create: async (data) => {
    const response = await api.post('/workflows/executions/', data)
    return response.data
  },
  
  start: async (id) => {
    const response = await api.post(`/workflows/executions/${id}/start/`)
    return response.data
  },
  
  complete: async (id) => {
    const response = await api.post(`/workflows/executions/${id}/complete/`)
    return response.data
  },
  
  updateStepData: async (executionId, stepId, data) => {
    const response = await api.patch(`/workflows/executions/${executionId}/steps/${stepId}/`, data)
    return response.data
  },
}

// Forms
export const formService = {
  getAll: async () => {
    const response = await api.get('/workflows/forms/')
    return response.data
  },
  
  getById: async (id) => {
    const response = await api.get(`/workflows/forms/${id}/`)
    return response.data
  },
}

export default {
  workflow: workflowService,
  execution: executionService,
  form: formService,
}
