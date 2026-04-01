// useChat Hook for Chat functionality
import { useEffect, useState, useCallback } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { RootState, AppDispatch } from '../store'
import { 
  addMessage, 
  setMessages, 
  setCurrentConversation, 
  clearMessages 
} from '../store/slices/chatSlice'
import { wsService } from '../services/websocket'
import { apiService } from '../services/api'
import { Message, Conversation } from '../types'

export function useChat() {
  const dispatch = useDispatch<AppDispatch>()
  const { currentConversation, messages } = useSelector((state: RootState) => state.chat)
  const { token } = useSelector((state: RootState) => state.auth)
  
  const [isLoading, setIsLoading] = useState(false)
  const [isStreaming, setIsStreaming] = useState(false)
  const [currentResponse, setCurrentResponse] = useState('')

  // Initialize WebSocket connection
  useEffect(() => {
    if (token && !wsService.isConnected()) {
      wsService
        .connect(token)
        .then(() => {
          console.log('WebSocket connected')
          // Register streaming handler
          wsService.on('chat.response_chunk', handleResponseChunk)
          wsService.on('chat.response_complete', handleResponseComplete)
        })
        .catch((error) => {
          console.error('Failed to connect WebSocket:', error)
        })
    }

    return () => {
      wsService.off('chat.response_chunk')
      wsService.off('chat.response_complete')
    }
  }, [token])

  // Handle response chunks
  const handleResponseChunk = useCallback((data: any) => {
    setCurrentResponse((prev) => prev + (data.chunk || ''))
  }, [])

  // Handle response complete
  const handleResponseComplete = useCallback((data: any) => {
    setIsStreaming(false)
    // Add complete message to store
    dispatch(
      addMessage({
        role: 'assistant',
        content: currentResponse,
        timestamp: new Date().toISOString(),
        message_id: data.message_id,
      })
    )
    setCurrentResponse('')
  }, [currentResponse, dispatch])

  // Create new conversation
  const createConversation = useCallback(
    async (title?: string, slideId?: number) => {
      try {
        const conversation = await apiService.createConversation(title, slideId)
        dispatch(setCurrentConversation(conversation))
        dispatch(clearMessages())
        return conversation
      } catch (error) {
        console.error('Error creating conversation:', error)
        throw error
      }
    },
    [dispatch]
  )

  // Load conversation
  const loadConversation = useCallback(
    async (conversationId: number) => {
      try {
        setIsLoading(true)
        const conversation = await apiService.getConversation(conversationId)
        dispatch(setCurrentConversation(conversation))
        dispatch(setMessages(conversation.messages || []))
      } catch (error) {
        console.error('Error loading conversation:', error)
        throw error
      } finally {
        setIsLoading(false)
      }
    },
    [dispatch]
  )

  // Send message
  const sendMessage = useCallback(
    async (content: string, slideId?: number) => {
      if (!currentConversation) {
        throw new Error('No active conversation')
      }

      try {
        setIsLoading(true)
        setIsStreaming(true)
        setCurrentResponse('')

        // Add user message
        dispatch(
          addMessage({
            role: 'user',
            content,
            timestamp: new Date().toISOString(),
          })
        )

        // Send via WebSocket if available
        if (wsService.isConnected()) {
          wsService.sendMessage(currentConversation.id, content, slideId)
        } else {
          // Fallback to REST API
          const response = await apiService.sendMessage(
            currentConversation.id,
            content,
            slideId
          )
          dispatch(
            addMessage({
              role: 'assistant',
              content: response.assistant_message,
              timestamp: new Date().toISOString(),
              message_id: response.message_id,
            })
          )
          setIsStreaming(false)
        }
      } catch (error) {
        console.error('Error sending message:', error)
        setIsStreaming(false)
        throw error
      } finally {
        setIsLoading(false)
      }
    },
    [currentConversation, dispatch]
  )

  return {
    currentConversation,
    messages,
    isLoading,
    isStreaming,
    currentResponse,
    createConversation,
    loadConversation,
    sendMessage,
  }
}
