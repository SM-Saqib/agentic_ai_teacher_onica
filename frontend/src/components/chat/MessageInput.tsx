// Message Input Component
import React, { useState } from 'react'
import { useChat } from '../../hooks/useChat'
import { useSelector } from 'react-redux'
import { RootState } from '../../store'

export const MessageInput: React.FC = () => {
  const [input, setInput] = useState('')
  const { sendMessage, isLoading } = useChat()
  const { currentSlide } = useSelector((state: RootState) => state.slide)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!input.trim()) return

    try {
      await sendMessage(input, currentSlide?.id)
      setInput('')
    } catch (error) {
      console.error('Failed to send message:', error)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="border-t border-gray-200 p-4 bg-gray-50">
      <div className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question..."
          disabled={isLoading}
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
        >
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </form>
  )
}
