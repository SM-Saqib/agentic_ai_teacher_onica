export default function TeachingPage() {
  return (
    <div className="h-screen w-screen bg-gray-50 flex">
      {/* Sidebar */}
      <div className="w-64 bg-white border-r border-gray-200">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-xl font-bold">AI Teacher</h2>
        </div>
        <nav className="p-4">
          <p className="text-gray-500 text-sm">Navigation coming soon...</p>
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex">
        {/* Slide Panel */}
        <div className="flex-1 bg-white border-r border-gray-200 p-6">
          <h3 className="text-2xl font-bold mb-4">Slide Viewer</h3>
          <div className="bg-gray-100 rounded-lg h-96 flex items-center justify-center">
            <p className="text-gray-500">Slide content will appear here</p>
          </div>
        </div>

        {/* Chat Panel */}
        <div className="w-96 bg-white flex flex-col">
          <div className="p-4 border-b border-gray-200">
            <h3 className="font-bold">Chat with AI Teacher</h3>
          </div>
          <div className="flex-1 p-4 overflow-y-auto">
            <p className="text-gray-500 text-sm">Chat messages will appear here</p>
          </div>
          <div className="p-4 border-t border-gray-200">
            <input
              type="text"
              placeholder="Ask a question..."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      </div>
    </div>
  )
}
