// API Response types
export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  message?: string
}

// User types
export interface User {
  id: number
  email: string
  username: string
  full_name?: string
  tier: 'free' | 'premium' | 'enterprise'
  is_active: boolean
  created_at: string
}

export interface AuthToken {
  access_token: string
  refresh_token?: string
  expires_in: number
  token_type: string
}

// Slide types
export interface Slide {
  id: number
  title: string
  content: string
  description?: string
  is_prebuilt: boolean
  version: number
  created_at: string
  updated_at: string
}

// Chat types
export interface Message {
  id: number
  role: 'user' | 'assistant'
  content: string
  timestamp: string
  tokens_used?: number
}

export interface Conversation {
  id: number
  title?: string
  messages: Message[]
  created_at: string
  updated_at: string
}

// Voice types
export interface VoiceConfig {
  enabled: boolean
  language: string
  voice_quality: 'low' | 'medium' | 'high'
}

// Avatar types
export interface AvatarConfig {
  id?: number
  avatar_type: 'basic' | 'premium' | 'enterprise'
  model_id?: string
  enabled: boolean
}
