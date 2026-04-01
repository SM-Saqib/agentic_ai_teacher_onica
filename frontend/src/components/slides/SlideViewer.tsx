// Slide Viewer Component
import React, { useEffect } from 'react'
import { useSelector } from 'react-redux'
import { RootState } from '../../store'

export const SlideViewer: React.FC = () => {
  const { currentSlide } = useSelector((state: RootState) => state.slide)

  return (
    <div className="flex-1 flex flex-col bg-white p-6">
      {currentSlide ? (
        <>
          <h2 className="text-2xl font-bold mb-4 text-gray-800">{currentSlide.title}</h2>
          <div className="flex-1 bg-gray-100 rounded-lg p-6 overflow-y-auto">
            <div className="prose max-w-none text-gray-800">
              {currentSlide.description && (
                <p className="text-lg mb-4">{currentSlide.description}</p>
              )}
              <div className="whitespace-pre-wrap">{currentSlide.content}</div>
            </div>
          </div>
          <div className="mt-4 text-sm text-gray-600">
            Version: {currentSlide.version} | Created: {new Date(currentSlide.created_at).toLocaleDateString()}
          </div>
        </>
      ) : (
        <div className="flex items-center justify-center h-full">
          <div className="text-center text-gray-500">
            <p className="text-lg mb-2">No Slide Selected</p>
            <p className="text-sm">Select a slide from the list to view its content</p>
          </div>
        </div>
      )}
    </div>
  )
}
