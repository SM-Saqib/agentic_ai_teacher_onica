// WebSocket Service for Chat
import { store } from '../store'
import { addMessage, setCurrentConversation } from '../store/slices/chatSlice'
import { addNotification } from '../store/slices/uiSlice'

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  timestamp: string
  message_id?: number
}

export interface WebSocketEvent {
  event: string
  data: any
}

class WebSocketService {
  private ws: WebSocket | null = null
  private url: string
  private token: string | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectDelay = 3000
  private messageHandlers: Map<string, Function> = new Map()
  private isManualClose = false

  constructor(url?: string) {
    this.url = url || import.meta.env.VITE_WS_URL || 'ws://localhost:8000'
  }

  /**
   * Connect to WebSocket server
   */
  connect(token: string): Promise<void> {
    return new Promise((resolve, reject) => {
      this.token = token
      this.isManualClose = false
      const wsUrl = `${this.url}/ws/v1/chat/${token}`

      try {
        this.ws = new WebSocket(wsUrl)

        this.ws.onopen = () => {
          console.log('WebSocket connected')
          this.reconnectAttempts = 0
          resolve()
        }

        this.ws.onmessage = (event) => {
          try {
            const wsEvent: WebSocketEvent = JSON.parse(event.data)
            this.handleMessage(wsEvent)
          } catch (error) {
            console.error('Error parsing WebSocket message:', error)
          }
        }

        this.ws.onerror = (error) => {
          console.error('WebSocket error:', error)
          reject(error)
        }

        this.ws.onclose = () => {
          console.log('WebSocket disconnected')
          if (!this.isManualClose) {
            this.attemptReconnect()
          }
        }
      } catch (error) {
        reject(error)
      }
    })
  }

  /**
   * Disconnect from WebSocket
   */
  disconnect(): void {
    this.isManualClose = true
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
  }

  /**
   * Send a chat message
   */
  sendMessage(
    conversationId: number,
    content: string,
    slideId?: number
  ): void {
    if (!this.isConnected()) {
      console.error('WebSocket is not connected')
      return
    }

    const event: WebSocketEvent = {
      event: 'chat.message',
      data: {
        conversation_id: conversationId,
        content,
        slide_id: slideId,
      },
    }

    this.ws?.send(JSON.stringify(event))
  }

  /**
   * Create a new conversation
   */
  createConversation(title?: string, slideId?: number): void {
    if (!this.isConnected()) {
      console.error('WebSocket is not connected')
      return
    }

    const event: WebSocketEvent = {
      event: 'conversation.create',
      data: {
        title,
        slide_id: slideId,
      },
    }

    this.ws?.send(JSON.stringify(event))
  }

  /**
   * Register event handler
   */
  on(eventType: string, handler: Function): void {
    this.messageHandlers.set(eventType, handler)
  }

  /**
   * Remove event handler
   */
  off(eventType: string): void {
    this.messageHandlers.delete(eventType)
  }

  /**
   * Check if connected
   */
  isConnected(): boolean {
    return this.ws !== null && this.ws.readyState === WebSocket.OPEN
  }

  /**
   * Handle incoming WebSocket messages
   */
  private handleMessage(event: WebSocketEvent): void {
    const { event: eventType, data } = event

    console.log(`Received event: ${eventType}`, data)

    switch (eventType) {
      case 'connection.ready':
        this.handleConnectionReady(data)
        break

      case 'chat.user_message':
        this.handleUserMessage(data)
        break

      case 'chat.response_chunk':
        this.handleResponseChunk(data)
        break

      case 'chat.response_complete':
        this.handleResponseComplete(data)
        break

      case 'conversation.created':
        this.handleConversationCreated(data)
        break

      case 'error':
        this.handleError(data)
        break

      default:
        // Call custom handler if registered
        const handler = this.messageHandlers.get(eventType)
        if (handler) {
          handler(data)
        }
        break
    }
  }

  /**
   * Handle connection ready event
   */
  private handleConnectionReady(data: any): void {
    console.log('Connection ready:', data)
    store.dispatch(
      addNotification({
        message: 'Connected to AI Teacher',
        type: 'success',
      })
    )
  }

  /**
   * Handle user message confirmation
   */
  private handleUserMessage(data: any): void {
    const message: ChatMessage = {
      role: 'user',
      content: data.content,
      timestamp: new Date().toISOString(),
      message_id: data.message_id,
    }

    store.dispatch(addMessage(message))
  }

  /**
   * Handle response chunk
   */
  private handleResponseChunk(data: any): void {
    const { conversation_id, chunk } = data
    // Emit custom event for UI to handle streaming
    const handler = this.messageHandlers.get('chat.response_chunk')
    if (handler) {
      handler(data)
    }
  }

  /**
   * Handle response complete
   */
  private handleResponseComplete(data: any): void {
    console.log('Response complete:', data)
    // Emit custom event
    const handler = this.messageHandlers.get('chat.response_complete')
    if (handler) {
      handler(data)
    }
  }

  /**
   * Handle conversation created event
   */
  private handleConversationCreated(data: any): void {
    const conversation = {
      id: data.conversation_id,
      title: data.title || 'New Conversation',
      slide_id: data.slide_id,
      messages: [],
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    }

    store.dispatch(setCurrentConversation(conversation))
  }

  /**
   * Handle error event
   */
  private handleError(data: any): void {
    const message = data.message || 'An error occurred'
    store.dispatch(
      addNotification({
        message,
        type: 'error',
      })
    )
  }

  /**
   * Attempt to reconnect
   */
  private attemptReconnect(): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      console.log(
        `Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`
      )

      setTimeout(() => {
        if (this.token) {
          this.connect(this.token).catch((error) => {
            console.error('Reconnection failed:', error)
          })
        }
      }, this.reconnectDelay)
    } else {
      store.dispatch(
        addNotification({
          message: 'Connection lost. Please refresh the page.',
          type: 'error',
        })
      )
    }
  }
}

// Export singleton instance
export const wsService = new WebSocketService()
