import api from './api'

export const authService = {
  /**
   * Login user
   * @param {string} username
   * @param {string} password
   * @returns {Promise} User data and tokens
   */
  login: async (username, password) => {
    const response = await api.post('/auth/token/', {
      username,
      password,
    })
    return response.data
  },

  /**
   * Refresh access token
   * @param {string} refreshToken
   * @returns {Promise} New access token
   */
  refreshToken: async (refreshToken) => {
    const response = await api.post('/auth/token/refresh/', {
      refresh: refreshToken,
    })
    return response.data
  },

  /**
   * Get current user profile
   * @returns {Promise} User data
   */
  getProfile: async () => {
    const response = await api.get('/auth/users/me/')
    return response.data
  },

  /**
   * Update user profile
   * @param {Object} data - User data to update
   * @returns {Promise} Updated user data
   */
  updateProfile: async (data) => {
    const response = await api.put('/auth/users/update_profile/', data)
    return response.data
  },

  /**
   * Change password
   * @param {string} oldPassword
   * @param {string} newPassword
   * @param {string} newPassword2
   * @returns {Promise}
   */
  changePassword: async (oldPassword, newPassword, newPassword2) => {
    const response = await api.post('/auth/users/change_password/', {
      old_password: oldPassword,
      new_password: newPassword,
      new_password2: newPassword2,
    })
    return response.data
  },
}
