// User Types
export interface User {
  userId: string
  phoneNumber: string
  language: string
  profile?: UserProfile
  preferences: UserPreferences
  createdAt: string
  updatedAt: string
  lastLoginAt?: string
}

export interface UserProfile {
  name?: string
  dateOfBirth?: string
  gender?: 'MALE' | 'FEMALE' | 'OTHER'
  state?: string
  district?: string
  income?: number
  category?: 'GENERAL' | 'OBC' | 'SC' | 'ST' | 'EWS'
  aadhaarNumber?: string
  panNumber?: string
  bankAccount?: BankDetails
  documents: string[]
}

export interface UserPreferences {
  notificationChannels: ('sms' | 'email' | 'push' | 'whatsapp')[]
  preferredLanguage: 'en' | 'hi' | 'mr' | 'kn' | 'ta' | 'te'
  voiceSpeed: number
  autoPlayAudio: boolean
}

export interface BankDetails {
  accountNumber: string
  ifscCode: string
  bankName: string
  verified: boolean
}

// Scheme Types
export interface Scheme {
  schemeId: string
  name: Record<string, string>
  description: Record<string, string>
  state: string
  category: 'education' | 'health' | 'agriculture' | 'housing' | 'employment' | 'pension' | 'women' | 'children' | 'disability' | 'financial' | 'other'
  eligibilityCriteria: EligibilityCriteria
  benefits: Record<string, string>
  applicationProcess: Record<string, string[]>
  requiredDocuments: string[]
  portalUrl?: string
  portalStatus: 'ACTIVE' | 'MAINTENANCE' | 'OFFLINE'
  lastSyncedAt: string
  isActive: boolean
}

export interface EligibilityCriteria {
  minAge?: number
  maxAge?: number
  gender: ('MALE' | 'FEMALE' | 'OTHER' | 'ALL')[]
  incomeLimit?: number
  categories: ('GENERAL' | 'OBC' | 'SC' | 'ST' | 'EWS' | 'ALL')[]
  states: string[]
  customRules: Rule[]
}

export interface Rule {
  field: string
  operator: 'eq' | 'ne' | 'gt' | 'lt' | 'gte' | 'lte' | 'in' | 'not_in' | 'contains' | 'not_contains'
  value: any
  logicalOperator?: 'AND' | 'OR'
}

// Application Types
export interface Application {
  applicationId: string
  userId: string
  schemeId: string
  status: ApplicationStatus
  formData: Record<string, any>
  documents: DocumentReference[]
  submittedAt?: string
  lastUpdatedAt: string
  externalReferenceId?: string
  statusHistory: StatusChange[]
  notes?: string
}

export type ApplicationStatus = 
  | 'DRAFT' 
  | 'SUBMITTED' 
  | 'UNDER_REVIEW'
  | 'DOCUMENTS_PENDING'
  | 'APPROVED' 
  | 'REJECTED' 
  | 'WITHDRAWN'
  | 'COMPLETED'

export interface DocumentReference {
  documentId: string
  documentType: 'aadhaar' | 'pan' | 'income_certificate' | 'caste_certificate' | 'bank_passbook' | 'photo' | 'address_proof' | 'age_proof' | 'disability_certificate' | 'ration_card' | 'other'
  s3Key: string
  uploadedAt: string
  verified: boolean
}

export interface StatusChange {
  status: ApplicationStatus
  timestamp: string
  reason?: string
  updatedBy: string
}

// Voice Types
export interface ConversationSession {
  sessionId: string
  userId: string
  language: 'en' | 'hi' | 'mr' | 'kn' | 'ta' | 'te'
  messages: Message[]
  context: ConversationContext
  startedAt: string
  lastActivityAt: string
  isActive: boolean
}

export interface Message {
  messageId: string
  role: 'USER' | 'ASSISTANT' | 'SYSTEM'
  content: string
  audioUrl?: string
  timestamp: string
  metadata?: Record<string, any>
}

export interface ConversationContext {
  currentIntent?: string
  entities: Record<string, any>
  selectedScheme?: string
  conversationState: 'READY' | 'LISTENING' | 'PROCESSING' | 'SPEAKING' | 'SHOWING_SCHEMES' | 'ELIGIBILITY_CHECKED' | 'APPLICATION_STARTED' | 'STATUS_SHOWN'
  userPreferences: Record<string, any>
}

// Other Types
export interface Helpline {
  helplineId: string
  name: Record<string, string>
  phoneNumber: string
  category: 'welfare' | 'health' | 'emergency' | 'agriculture' | 'education' | 'other'
  state: string
  availability: string
  languages: ('en' | 'hi' | 'mr' | 'kn' | 'ta' | 'te')[]
  description: Record<string, string>
  isActive: boolean
  createdAt: string
  updatedAt: string
}

export interface GuideContent {
  contentId: string
  category: 'quick-guide' | 'faq' | 'tutorial' | 'troubleshooting'
  state: string
  question: Record<string, string>
  answer: Record<string, string>
  priority: number
  tags: string[]
  relatedSchemes: string[]
  viewCount: number
  lastUpdatedAt: string
  isActive: boolean
}

export interface SuggestedQuery {
  queryId: string
  text: Record<string, string>
  category: 'ration-card' | 'health' | 'agriculture' | 'education' | 'pension' | 'other'
  state: string
  intent: 'SEARCH_SCHEMES' | 'CHECK_ELIGIBILITY' | 'START_APPLICATION' | 'GET_STATUS' | 'FIND_HELPLINE' | 'GET_GUIDE' | 'OTHER'
  entities: Record<string, any>
  popularity: number
  displayOrder: number
  isActive: boolean
  lastUpdatedAt: string
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  message?: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
  hasMore: boolean
}
