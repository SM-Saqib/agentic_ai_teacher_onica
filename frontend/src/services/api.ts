// API Service for REST endpoints
import axios, { AxiosInstance } from 'axios'
import { User, AuthToken, Conversation, Message } from '../types'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

class ApiService {
  private api: AxiosInstance

  constructor() {
    this.api = axios.create({
      baseURL: `${API_URL}/api/v1`,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Add token to requests
    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('access_token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    })
  }

  // ===== Auth Endpoints =====

  async register(
    email: string,
    username: string,
    password: string,
    fullName?: string
  ): Promise<{ user: User; access_token: string; refresh_token?: string }> {
    const response = await this.api.post('/auth/register', {
      email,
      username,
      password,
      full_name: fullName,
    })
    return response.data
  }

  async login(
    email: string,
    password: string
  ): Promise<{ user: User; access_token: string; refresh_token?: string }> {
    const response = await this.api.post('/auth/login', {
      email,
      password,
    })
    return response.data
  }

  async getCurrentUser(): Promise<User> {
    const response = await this.api.get('/auth/me')
    return response.data
  }

  // ===== Chat Endpoints =====

  async createConversation(
    title?: string,
    slideId?: number
  ): Promise<Conversation> {
    const response = await this.api.post('/chat/conversations', {
      title,
      slide_id: slideId,
    })
    return response.data
  }

  async getConversations(limit = 20): Promise<{ conversations: Conversation[]; total: number }> {
    const response = await this.api.get('/chat/conversations', {
      params: { limit },
    })
    return response.data
  }

  async getConversation(conversationId: number): Promise<Conversation & { messages: Message[] }> {
    const response = await this.api.get(`/chat/conversations/${conversationId}`)
    return response.data
  }

  async sendMessage(
    conversationId: number,
    content: string,
    slideId?: number
  ): Promise<{ message_id: number; assistant_message: string; tokens_used: number }> {
    const response = await this.api.post('/chat/message', {
      conversation_id: conversationId,
      content,
      slide_id: slideId,
    })
    return response.data
  }

  async deleteConversation(conversationId: number): Promise<void> {
    await this.api.delete(`/chat/conversations/${conversationId}`)
  }

  // ===== Slides Endpoints (placeholder) =====

  async getSlides(): Promise<any> {
    try {
      const response = await this.api.get('/slides')
      return response.data
    } catch (error) {
      console.error('Error fetching slides:', error)
      return { slides: [] }
    }
  }

  async getSlide(slideId: number): Promise<any> {
    try {
      const response = await this.api.get(`/slides/${slideId}`)
      return response.data
    } catch (error) {
      console.error('Error fetching slide:', error)
      return null
    }
  }

  // ===== Health Check =====

  async healthCheck(): Promise<{ status: string }> {
    const response = await this.api.get('/health')
    return response.data
  }
}

export const apiService = new ApiService()
