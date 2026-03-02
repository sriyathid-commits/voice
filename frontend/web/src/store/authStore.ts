import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { User } from '@/types'

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  
  // Actions
  setUser: (user: User) => void
  setToken: (token: string) => void
  logout: () => void
  updateProfile: (profile: Partial<User['profile']>) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,

      setUser: (user) => set({ user, isAuthenticated: true }),
      
      setToken: (token) => set({ token }),
      
      logout: () => set({ 
        user: null, 
        token: null, 
        isAuthenticated: false 
      }),
      
      updateProfile: (profile) => set((state) => {
        if (!state.user) return { user: null }
        return {
          user: {
            ...state.user,
            profile: { 
              ...state.user.profile, 
              ...profile,
              documents: profile?.documents || state.user.profile?.documents || []
            }
          }
        }
      }),
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)
