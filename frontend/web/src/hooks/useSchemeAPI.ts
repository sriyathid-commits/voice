import { useSchemeStore } from '@/store/schemeStore'
import { useVoiceStore } from '@/store/voiceStore'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev'

export function useSchemeAPI() {
  const {
    setEligibilityExplanation,
    setIsCheckingEligibility,
    setActionPlan,
    setIsGeneratingActionPlan,
    setError
  } = useSchemeStore()
  
  const { citizenProfile } = useVoiceStore()

  /**
   * Check eligibility and get detailed explanation
   */
  const checkEligibilityWithExplanation = async (
    schemeId: string,
    language: string = 'en'
  ) => {
    setIsCheckingEligibility(true)
    setError(null)
    
    try {
      const response = await fetch(
        `${API_URL}/schemes/${schemeId}/eligibility-explanation?language=${language}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            user_profile: citizenProfile
          })
        }
      )
      
      if (!response.ok) {
        throw new Error(`Failed to check eligibility: ${response.status}`)
      }
      
      const data = await response.json()
      
      if (data.success && data.explanation) {
        setEligibilityExplanation(data.explanation)
        return data.explanation
      } else {
        throw new Error('Invalid response format')
      }
    } catch (err) {
      console.error('Error checking eligibility:', err)
      setError('Failed to check eligibility. Please try again.')
      return null
    } finally {
      setIsCheckingEligibility(false)
    }
  }

  /**
   * Generate action plan for scheme application
   */
  const generateActionPlan = async (
    schemeId: string,
    availableDocuments: string[] = [],
    language: string = 'en'
  ) => {
    setIsGeneratingActionPlan(true)
    setError(null)
    
    try {
      const queryParams = new URLSearchParams({
        language,
        ...availableDocuments.reduce((acc, doc, idx) => ({
          ...acc,
          [`available_documents[${idx}]`]: doc
        }), {})
      })
      
      const response = await fetch(
        `${API_URL}/schemes/${schemeId}/action-plan?${queryParams}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(citizenProfile)
        }
      )
      
      if (!response.ok) {
        throw new Error(`Failed to generate action plan: ${response.status}`)
      }
      
      const data = await response.json()
      
      if (data.success && data.action_plan) {
        setActionPlan(data.action_plan)
        return data.action_plan
      } else {
        throw new Error('Invalid response format')
      }
    } catch (err) {
      console.error('Error generating action plan:', err)
      setError('Failed to generate action plan. Please try again.')
      return null
    } finally {
      setIsGeneratingActionPlan(false)
    }
  }

  /**
   * Get eligibility and action plan together
   */
  const getCompleteAnalysis = async (
    schemeId: string,
    availableDocuments: string[] = [],
    language: string = 'en'
  ) => {
    // First check eligibility
    const eligibility = await checkEligibilityWithExplanation(schemeId, language)
    
    if (!eligibility) {
      return { eligibility: null, actionPlan: null }
    }
    
    // Then generate action plan
    const actionPlan = await generateActionPlan(schemeId, availableDocuments, language)
    
    return { eligibility, actionPlan }
  }

  return {
    checkEligibilityWithExplanation,
    generateActionPlan,
    getCompleteAnalysis
  }
}
