// Chat Window Component
import React, { useEffect, useRef } from 'react'
import { useChat } from '../../hooks/useChat'
import { ChatMessage } from './ChatMessage'
import { MessageInput } from './MessageInput'

export const ChatWindow: React.FC = () => {
  const {
    currentConversation,
    messages,
    isStreaming,
    currentResponse,
  } = useChat()
  
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, currentResponse])

  if (!currentConversation) {
    return (
      <div className="flex-1 flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <p className="text-gray-500 mb-4">No conversation selected</p>
          <p className="text-sm text-gray-400">Create or select a conversation to start chatting</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex-1 flex flex-col h-full bg-white">
      {/* Header */}
      <div className="border-b border-gray-200 p-4">
        <h2 className="text-lg font-semibold text-gray-800">
          {currentConversation.title || 'Conversation'}
        </h2>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 py-8">
            <p>Start a conversation by asking a question</p>
          </div>
        )}

        {messages.map((message, index) => (
          <ChatMessage key={index} message={message} />
        ))}

        {isStreaming && currentResponse && (
          <ChatMessage
            message={{
              role: 'assistant',
              content: currentResponse,
              timestamp: new Date().toISOString(),
            }}
            isStreaming={true}
          />
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <MessageInput />
    </div>
  )
}
