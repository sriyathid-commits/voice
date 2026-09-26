import { create } from 'zustand'

export interface CitizenProfile {
  language: string
  state?: string
  district?: string
  age?: number
  occupation?: string
  income_range?: string
  gender?: string
  is_farmer?: boolean
  is_student?: boolean
  has_land?: boolean
  has_disability?: boolean
  available_documents: string[]
  current_scheme_context?: string
}

export interface ConversationMessage {
  message_id: string
  role: 'USER' | 'ASSISTANT' | 'SYSTEM'
  content: string
  audio_url?: string
  timestamp: string
  intent?: string
}

interface VoiceState {
  // Voice recording state
  isRecording: boolean
  isProcessing: boolean
  isSpeaking: boolean
  
  // Session & conversation
  sessionId: string | null
  messages: ConversationMessage[]
  citizenProfile: CitizenProfile
  currentIntent: string | null
  profileGaps: string[]
  
  // Current voice interaction
  currentTranscript: string
  currentResponse: string
  currentAudioUrl: string | null
  confidence: number
  
  // Language
  selectedLanguage: string
  
  // Error handling
  error: string | null
  
  // Actions
  setRecording: (isRecording: boolean) => void
  setProcessing: (isProcessing: boolean) => void
  setSpeaking: (isSpeaking: boolean) => void
  setSessionId: (sessionId: string) => void
  addMessage: (message: ConversationMessage) => void
  setMessages: (messages: ConversationMessage[]) => void
  updateCitizenProfile: (updates: Partial<CitizenProfile>) => void
  setCurrentIntent: (intent: string | null) => void
  setProfileGaps: (gaps: string[]) => void
  setCurrentTranscript: (transcript: string) => void
  setCurrentResponse: (response: string) => void
  setCurrentAudioUrl: (url: string | null) => void
  setConfidence: (confidence: number) => void
  setSelectedLanguage: (language: string) => void
  setError: (error: string | null) => void
  resetVoiceState: () => void
  clearConversation: () => void
}

const initialCitizenProfile: CitizenProfile = {
  language: 'hi',
  available_documents: []
}

export const useVoiceStore = create<VoiceState>((set) => ({
  // Initial state
  isRecording: false,
  isProcessing: false,
  isSpeaking: false,
  
  sessionId: null,
  messages: [],
  citizenProfile: initialCitizenProfile,
  currentIntent: null,
  profileGaps: [],
  
  currentTranscript: '',
  currentResponse: '',
  currentAudioUrl: null,
  confidence: 0,
  
  selectedLanguage: 'hi',
  
  error: null,
  
  // Actions
  setRecording: (isRecording) => set({ isRecording }),
  
  setProcessing: (isProcessing) => set({ isProcessing }),
  
  setSpeaking: (isSpeaking) => set({ isSpeaking }),
  
  setSessionId: (sessionId) => set({ sessionId }),
  
  addMessage: (message) => 
    set((state) => ({ 
      messages: [...state.messages, message]
    })),
  
  setMessages: (messages) => set({ messages }),
  
  updateCitizenProfile: (updates) =>
    set((state) => ({
      citizenProfile: {
        ...state.citizenProfile,
        ...updates
      }
    })),
  
  setCurrentIntent: (intent) => set({ currentIntent: intent }),
  
  setProfileGaps: (gaps) => set({ profileGaps: gaps }),
  
  setCurrentTranscript: (transcript) => set({ currentTranscript: transcript }),
  
  setCurrentResponse: (response) => set({ currentResponse: response }),
  
  setCurrentAudioUrl: (url) => set({ currentAudioUrl: url }),
  
  setConfidence: (confidence) => set({ confidence }),
  
  setSelectedLanguage: (language) =>
    set((state) => ({
      selectedLanguage: language,
      citizenProfile: {
        ...state.citizenProfile,
        language
      }
    })),
  
  setError: (error) => set({ error }),
  
  resetVoiceState: () =>
    set({
      isRecording: false,
      isProcessing: false,
      isSpeaking: false,
      currentTranscript: '',
      currentResponse: '',
      currentAudioUrl: null,
      confidence: 0,
      error: null
    }),
  
  clearConversation: () =>
    set({
      sessionId: null,
      messages: [],
      citizenProfile: initialCitizenProfile,
      currentIntent: null,
      profileGaps: [],
      currentTranscript: '',
      currentResponse: '',
      currentAudioUrl: null,
      confidence: 0,
      error: null
    })
}))
