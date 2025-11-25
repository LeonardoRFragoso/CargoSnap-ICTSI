import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useAuthStore = create(
  persist(
    (set) => ({
      user: null,
      token: null,
      refreshToken: null,
      isAuthenticated: false,

      setAuth: (data) => set({
        user: data.user,
        token: data.access,
        refreshToken: data.refresh,
        isAuthenticated: true,
      }),

      updateUser: (userData) => set((state) => ({
        user: { ...state.user, ...userData },
      })),

      logout: () => set({
        user: null,
        token: null,
        refreshToken: null,
        isAuthenticated: false,
      }),

      // Helper to check if user has specific role
      hasRole: (role) => {
        const state = useAuthStore.getState()
        return state.user?.role === role
      },

      // Helper to check if user can perform action
      canCreate: () => {
        const state = useAuthStore.getState()
        return ['ADMIN', 'MANAGER', 'INSPECTOR'].includes(state.user?.role)
      },

      canEdit: () => {
        const state = useAuthStore.getState()
        return ['ADMIN', 'MANAGER'].includes(state.user?.role)
      },

      canDelete: () => {
        const state = useAuthStore.getState()
        return state.user?.role === 'ADMIN'
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        refreshToken: state.refreshToken,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)
