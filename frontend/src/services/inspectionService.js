import api from './api'

/**
 * Inspection Service
 * Handles all API calls related to inspections
 */

// Inspection Types
export const inspectionTypeService = {
  getAll: async () => {
    const response = await api.get('/inspections/types/')
    return response.data
  },
  
  getById: async (id) => {
    const response = await api.get(`/inspections/types/${id}/`)
    return response.data
  },
}

// Inspections
export const inspectionService = {
  getAll: async (params = {}) => {
    const response = await api.get('/inspections/inspections/', { params })
    return response.data
  },
  
  getById: async (id) => {
    const response = await api.get(`/inspections/inspections/${id}/`)
    return response.data
  },
  
  create: async (data) => {
    const response = await api.post('/inspections/inspections/', data)
    return response.data
  },
  
  update: async (id, data) => {
    const response = await api.put(`/inspections/inspections/${id}/`, data)
    return response.data
  },
  
  delete: async (id) => {
    const response = await api.delete(`/inspections/inspections/${id}/`)
    return response.data
  },
  
  start: async (id) => {
    const response = await api.post(`/inspections/inspections/${id}/start/`)
    return response.data
  },
  
  complete: async (id) => {
    const response = await api.post(`/inspections/inspections/${id}/complete/`)
    return response.data
  },
  
  getSummary: async (id) => {
    const response = await api.get(`/inspections/inspections/${id}/summary/`)
    return response.data
  },
}

// Photos
export const photoService = {
  getAll: async (inspectionId) => {
    const response = await api.get('/inspections/photos/', {
      params: { inspection: inspectionId }
    })
    return response.data
  },
  
  upload: async (data) => {
    const formData = new FormData()
    Object.keys(data).forEach(key => {
      if (data[key] !== null && data[key] !== undefined) {
        formData.append(key, data[key])
      }
    })
    
    const response = await api.post('/inspections/photos/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },
  
  delete: async (id) => {
    const response = await api.delete(`/inspections/photos/${id}/`)
    return response.data
  },
}

// Videos
export const videoService = {
  upload: async (data) => {
    const formData = new FormData()
    Object.keys(data).forEach(key => {
      if (data[key] !== null && data[key] !== undefined) {
        formData.append(key, data[key])
      }
    })
    
    const response = await api.post('/inspections/videos/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },
}

// Documents
export const documentService = {
  upload: async (data) => {
    const formData = new FormData()
    Object.keys(data).forEach(key => {
      if (data[key] !== null && data[key] !== undefined) {
        formData.append(key, data[key])
      }
    })
    
    const response = await api.post('/inspections/documents/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },
}

export default {
  inspectionType: inspectionTypeService,
  inspection: inspectionService,
  photo: photoService,
  video: videoService,
  document: documentService,
}
