import React, { useEffect } from 'react'
import { useDispatch } from 'react-redux'
import { ChatWindow } from '../components/chat/ChatWindow'
import { ChatHistory } from '../components/chat/ChatHistory'
import { SlideViewer } from '../components/slides/SlideViewer'
import { useChat } from '../hooks/useChat'
import { AppDispatch } from '../store'

export default function TeachingPage() {
  const dispatch = useDispatch<AppDispatch>()
  const { currentConversation, createConversation } = useChat()

  useEffect(() => {
    // Create initial conversation if none exists
    if (!currentConversation) {
      createConversation('Teaching Session').catch((error) => {
        console.error('Failed to create conversation:', error)
      })
    }
  }, [])

  return (
    <div className="h-screen w-screen bg-gray-50 flex">
      {/* Sidebar - Conversation History */}
      <div className="w-64 bg-white border-r border-gray-200 overflow-hidden">
        <ChatHistory />
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex gap-4 p-4">
        {/* Slide Panel */}
        <div className="flex-1 bg-white rounded-lg shadow">
          <SlideViewer />
        </div>

        {/* Chat Panel */}
        <div className="w-96 bg-white rounded-lg shadow flex flex-col overflow-hidden">
          <ChatWindow />
        </div>
      </div>
    </div>
  )
}
