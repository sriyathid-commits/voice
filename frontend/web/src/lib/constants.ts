// API Configuration
export const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
export const WS_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000'
export const CLOUDFRONT_URL = process.env.NEXT_PUBLIC_CLOUDFRONT_URL || ''

// Cognito Configuration
export const COGNITO_USER_POOL_ID = process.env.NEXT_PUBLIC_COGNITO_USER_POOL_ID || ''
export const COGNITO_CLIENT_ID = process.env.NEXT_PUBLIC_COGNITO_CLIENT_ID || ''
export const COGNITO_REGION = process.env.NEXT_PUBLIC_COGNITO_REGION || 'ap-south-1'

// Application Configuration
export const APP_NAME = 'Voice for Bharat'
export const APP_VERSION = '1.0.0'
export const DEFAULT_LANGUAGE = 'en'

// Supported Languages
export const SUPPORTED_LANGUAGES = [
  { code: 'en', name: 'English' },
  { code: 'hi', name: 'Hindi' },
  { code: 'mr', name: 'Marathi' },
  { code: 'kn', name: 'Kannada' },
  { code: 'ta', name: 'Tamil' },
  { code: 'te', name: 'Telugu' },
] as const

// Indian States
export const INDIAN_STATES = [
  'Andhra Pradesh',
  'Telangana',
  'Karnataka',
  'Tamil Nadu',
  'Kerala',
  'Maharashtra',
  'Uttar Pradesh',
  'Bihar',
  'West Bengal',
  'Gujarat',
  'Other',
] as const

// Color Palette
export const COLORS = {
  primary: {
    orange: '#ff6b35',
    green: '#4caf50',
    navy: '#1a2332',
  },
  status: {
    success: '#4caf50',
    warning: '#ffc107',
    error: '#f44336',
    info: '#9c27b0',
  },
  card: {
    lightBlue: '#e3f2fd',
    lightOrange: '#fff3e0',
  },
} as const

// API Endpoints
export const API_ENDPOINTS = {
  // User endpoints
  register: '/register',
  verifyOtp: '/verify-otp',
  profile: '/profile',
  
  // Scheme endpoints
  schemes: '/schemes',
  schemeDetails: (id: string) => `/schemes/${id}`,
  checkEligibility: (id: string) => `/schemes/${id}/check-eligibility`,
  saveScheme: (id: string) => `/schemes/${id}/save`,
  
  // Application endpoints
  applications: '/applications',
  applicationDetails: (id: string) => `/applications/${id}`,
  submitApplication: (id: string) => `/applications/${id}/submit`,
  
  // Document endpoints
  uploadDocument: '/documents/upload',
  getDocument: (id: string) => `/documents/${id}`,
  deleteDocument: (id: string) => `/documents/${id}`,
  
  // Voice endpoints
  voiceQuery: '/voice/query',
  voiceSession: (id: string) => `/voice/session/${id}`,
  
  // Other endpoints
  activity: '/activity',
  helplines: '/helplines',
  guideContent: '/guide-content',
  suggestedQueries: '/suggested-queries',
} as const

// Feature Flags
export const FEATURES = {
  enablePWA: process.env.NEXT_PUBLIC_ENABLE_PWA === 'true',
  enableVoiceAssistant: process.env.NEXT_PUBLIC_ENABLE_VOICE_ASSISTANT === 'true',
  enableOfflineMode: process.env.NEXT_PUBLIC_ENABLE_OFFLINE_MODE === 'true',
} as const
