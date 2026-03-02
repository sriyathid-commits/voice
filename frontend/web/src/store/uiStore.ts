import { create } from 'zustand'

interface Toast {
  id: string
  message: string
  type: 'success' | 'error' | 'warning' | 'info'
  duration?: number
}

interface Modal {
  id: string
  isOpen: boolean
  content?: React.ReactNode
}

interface UIState {
  // State
  selectedState: string
  selectedLanguage: string
  activeTab: string
  toasts: Toast[]
  modals: Modal[]
  isLoading: boolean
  
  // Actions
  setSelectedState: (state: string) => void
  setSelectedLanguage: (language: string) => void
  setActiveTab: (tab: string) => void
  addToast: (toast: Omit<Toast, 'id'>) => void
  removeToast: (id: string) => void
  openModal: (id: string, content?: React.ReactNode) => void
  closeModal: (id: string) => void
  setLoading: (isLoading: boolean) => void
}

export const useUIStore = create<UIState>((set) => ({
  selectedState: 'Other',
  selectedLanguage: 'en',
  activeTab: 'DASHBOARD',
  toasts: [],
  modals: [],
  isLoading: false,

  setSelectedState: (state) => set({ selectedState: state }),
  
  setSelectedLanguage: (language) => set({ selectedLanguage: language }),
  
  setActiveTab: (tab) => set({ activeTab: tab }),
  
  addToast: (toast) => set((state) => ({
    toasts: [...state.toasts, { ...toast, id: Date.now().toString() }]
  })),
  
  removeToast: (id) => set((state) => ({
    toasts: state.toasts.filter((t) => t.id !== id)
  })),
  
  openModal: (id, content) => set((state) => ({
    modals: [...state.modals.filter((m) => m.id !== id), { id, isOpen: true, content }]
  })),
  
  closeModal: (id) => set((state) => ({
    modals: state.modals.map((m) => m.id === id ? { ...m, isOpen: false } : m)
  })),
  
  setLoading: (isLoading) => set({ isLoading }),
}))
