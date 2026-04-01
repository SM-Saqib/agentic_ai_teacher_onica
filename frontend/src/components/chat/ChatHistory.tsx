// Chat History Component
import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { RootState } from '../../store'
import { setCurrentConversation } from '../../store/slices/chatSlice'
import { apiService } from '../../services/api'

export const ChatHistory: React.FC = () => {
  const dispatch = useDispatch()
  const { currentConversation } = useSelector((state: RootState) => state.chat)
  const [conversations, setConversations] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    loadConversations()
  }, [])

  const loadConversations = async () => {
    try {
      setIsLoading(true)
      const data = await apiService.getConversations(20)
      setConversations(data.conversations)
    } catch (error) {
      console.error('Error loading conversations:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleSelectConversation = (conversationId: number) => {
    const conversation = conversations.find((c) => c.id === conversationId)
    if (conversation) {
      dispatch(setCurrentConversation(conversation))
    }
  }

  return (
    <div className="border-r border-gray-200 p-4 overflow-y-auto bg-gray-50">
      <h3 className="font-semibold mb-4 text-gray-800">Conversations</h3>

      {isLoading ? (
        <div className="text-center text-gray-500 py-4">Loading...</div>
      ) : conversations.length === 0 ? (
        <div className="text-center text-gray-500 text-sm py-8">No conversations yet</div>
      ) : (
        <div className="space-y-2">
          {conversations.map((conversation) => (
            <button
              key={conversation.id}
              onClick={() => handleSelectConversation(conversation.id)}
              className={`w-full text-left px-3 py-2 rounded-lg transition ${
                currentConversation?.id === conversation.id
                  ? 'bg-blue-600 text-white'
                  : 'hover:bg-gray-200 text-gray-800'
              }`}
            >
              <p className="text-sm font-medium truncate">{conversation.title}</p>
              <p className="text-xs mt-1 opacity-75">
                {new Date(conversation.created_at).toLocaleDateString()}
              </p>
            </button>
          ))}
        </div>
      )}

      <button
        onClick={loadConversations}
        className="w-full mt-4 px-3 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition"
      >
        New Conversation
      </button>
    </div>
  )
}
