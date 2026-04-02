'use client'
import { useState, useEffect, useRef } from 'react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'

export default function ChatBox() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [emotion, setEmotion] = useState(null)
  const [crisis, setCrisis] = useState(false)
  const [moodHistory, setMoodHistory] = useState([])
  const chatEndRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  useEffect(() => {
    inputRef.current?.focus()
  }, [])

  const sendMessage = async () => {
    const trimmedInput = input.trim()
    if (!trimmedInput || loading) return

    const userMessage = { role: 'user', content: trimmedInput }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: trimmedInput })
      })

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`)
      }

      const data = await response.json()
      
      const aiMessage = { role: 'assistant', content: data.response }
      setMessages(prev => [...prev, aiMessage])
      setEmotion(data.emotion)
      setCrisis(data.crisis)
      if (data.mood_history) {
        setMoodHistory(data.mood_history)
      }
    } catch (err) {
      console.error('Chat error:', err)
      setError('Failed to get response. Please try again.')
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: "I'm having trouble connecting right now. Please try again in a moment." 
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleReset = async () => {
    try {
      await fetch(`${API_URL}/reset`, { method: 'POST' })
      setMessages([])
      setEmotion(null)
      setCrisis(false)
      setMoodHistory([])
      setError(null)
    } catch (err) {
      console.error('Reset error:', err)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const getEmotionColor = (emotion) => {
    const colors = {
      joy: '#10b981',
      love: '#ec4899',
      sadness: '#3b82f6',
      anger: '#ef4444',
      fear: '#8b5cf6',
      anxiety: '#f59e0b',
      surprise: '#06b6d4',
      neutral: '#6b7280'
    }
    return colors[emotion?.toLowerCase()] || '#6b7280'
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold text-gray-900">AI Counselling System</h1>
            <p className="text-sm text-gray-500">Your safe space for emotional support</p>
          </div>
          <button
            onClick={handleReset}
            className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          >
            Reset Chat
          </button>
        </div>
      </div>

      {/* Status Bar */}
      {(emotion || crisis) && (
        <div className="bg-white border-b border-gray-200 px-6 py-2">
          <div className="max-w-4xl mx-auto flex items-center gap-4 text-sm">
            {emotion && (
              <div className="flex items-center gap-2">
                <span className="text-gray-500">Emotion:</span>
                <span 
                  className="px-2 py-0.5 rounded-full text-white text-xs font-medium"
                  style={{ backgroundColor: getEmotionColor(emotion) }}
                >
                  {emotion}
                </span>
              </div>
            )}
            {crisis && (
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
                <span className="text-red-600 font-medium">Crisis detected</span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-6">
        <div className="max-w-4xl mx-auto space-y-4">
          {messages.length === 0 && (
            <div className="text-center py-12">
              <div className="text-4xl mb-4">💙</div>
              <h2 className="text-lg font-medium text-gray-900 mb-2">Welcome to your safe space</h2>
              <p className="text-gray-500 max-w-md mx-auto">
                I'm here to listen and support you. Share what's on your mind, and we'll work through it together.
              </p>
            </div>
          )}

          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                  msg.role === 'user'
                    ? 'bg-blue-600 text-white rounded-br-sm'
                    : 'bg-white border border-gray-200 text-gray-900 rounded-bl-sm'
                }`}
              >
                <p className="whitespace-pre-wrap text-sm leading-relaxed">{msg.content}</p>
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-white border border-gray-200 rounded-2xl rounded-bl-sm px-4 py-3">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              </div>
            </div>
          )}

          {error && (
            <div className="text-center text-red-500 text-sm py-2">
              {error}
            </div>
          )}

          <div ref={chatEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 px-6 py-4">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-end gap-3">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Type your message here..."
              rows={1}
              className="flex-1 resize-none border border-gray-300 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={loading}
            />
            <button
              onClick={sendMessage}
              disabled={loading || !input.trim()}
              className="px-6 py-3 bg-blue-600 text-white rounded-xl text-sm font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Send
            </button>
          </div>
          <p className="text-xs text-gray-400 mt-2 text-center">
            This AI provides emotional support but is not a replacement for professional help.
          </p>
        </div>
      </div>
    </div>
  )
}