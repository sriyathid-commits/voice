import { create } from 'zustand'
import { Scheme } from '@/types'

export interface EligibilityExplanation {
  scheme_id: string
  scheme_name: Record<string, string>
  status: 'ELIGIBLE' | 'LIKELY_ELIGIBLE' | 'NEEDS_VERIFICATION' | 'NOT_ELIGIBLE'
  score: number
  matched_conditions: string[]
  match_reasons: string[]
  missing_information: string[]
  verification_required: string[]
  eligibility_criteria_summary: {
    age_range?: string
    eligible_genders?: string[]
    income_limit?: number
    eligible_categories?: string[]
    eligible_states?: string[]
  }
}

export interface ActionPlanStep {
  step_number: number
  action: string
  description: string
  status: 'COMPLETED' | 'REQUIRED' | 'OPTIONAL'
  documents_needed: string[]
}

export interface ActionPlan {
  scheme_id: string
  scheme_name: Record<string, string>
  eligibility_status: string
  required_documents: string[]
  available_documents: string[]
  missing_documents: string[]
  next_steps: ActionPlanStep[]
  application_method?: string
  portal_url?: string
  estimated_time?: string
  notes: string[]
}

interface SchemeState {
  // Schemes
  schemes: Scheme[]
  selectedScheme: Scheme | null
  isLoadingSchemes: boolean
  
  // Eligibility
  eligibilityExplanation: EligibilityExplanation | null
  isCheckingEligibility: boolean
  
  // Action Plan
  actionPlan: ActionPlan | null
  isGeneratingActionPlan: boolean
  
  // Filters
  selectedState: string | null
  selectedCategory: string | null
  
  // Error
  error: string | null
  
  // Actions
  setSchemes: (schemes: Scheme[]) => void
  setSelectedScheme: (scheme: Scheme | null) => void
  setIsLoadingSchemes: (isLoading: boolean) => void
  setEligibilityExplanation: (explanation: EligibilityExplanation | null) => void
  setIsCheckingEligibility: (isChecking: boolean) => void
  setActionPlan: (plan: ActionPlan | null) => void
  setIsGeneratingActionPlan: (isGenerating: boolean) => void
  setSelectedState: (state: string | null) => void
  setSelectedCategory: (category: string | null) => void
  setError: (error: string | null) => void
  clearSchemeData: () => void
}

export const useSchemeStore = create<SchemeState>((set) => ({
  // Initial state
  schemes: [],
  selectedScheme: null,
  isLoadingSchemes: false,
  
  eligibilityExplanation: null,
  isCheckingEligibility: false,
  
  actionPlan: null,
  isGeneratingActionPlan: false,
  
  selectedState: null,
  selectedCategory: null,
  
  error: null,
  
  // Actions
  setSchemes: (schemes) => set({ schemes }),
  
  setSelectedScheme: (scheme) => set({ selectedScheme: scheme }),
  
  setIsLoadingSchemes: (isLoading) => set({ isLoadingSchemes: isLoading }),
  
  setEligibilityExplanation: (explanation) => 
    set({ eligibilityExplanation: explanation }),
  
  setIsCheckingEligibility: (isChecking) => 
    set({ isCheckingEligibility: isChecking }),
  
  setActionPlan: (plan) => set({ actionPlan: plan }),
  
  setIsGeneratingActionPlan: (isGenerating) => 
    set({ isGeneratingActionPlan: isGenerating }),
  
  setSelectedState: (state) => set({ selectedState: state }),
  
  setSelectedCategory: (category) => set({ selectedCategory: category }),
  
  setError: (error) => set({ error }),
  
  clearSchemeData: () =>
    set({
      selectedScheme: null,
      eligibilityExplanation: null,
      actionPlan: null,
      error: null
    })
}))
