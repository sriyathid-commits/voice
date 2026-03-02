'use client'

import React, { useState } from 'react'
import { Button } from '@/components/ui/Button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'

export default function AssistantPage() {
  const [status, setStatus] = useState<'ready' | 'listening' | 'processing' | 'speaking'>('ready')

  const handleVoiceToggle = () => {
    if (status === 'ready') {
      setStatus('listening')
      // Simulate voice processing
      setTimeout(() => {
        setStatus('processing')
        setTimeout(() => {
          setStatus('speaking')
          setTimeout(() => {
            setStatus('ready')
          }, 2000)
        }, 1500)
      }, 3000)
    }
  }

  const getStatusMessage = () => {
    switch (status) {
      case 'ready': return 'Ready to Help'
      case 'listening': return 'Listening...'
      case 'processing': return 'Processing your query...'
      case 'speaking': return 'Speaking response...'
      default: return 'Ready to Help'
    }
  }

  const getButtonColor = () => {
    switch (status) {
      case 'listening': return 'bg-red-500 hover:bg-red-600 animate-pulse'
      case 'processing': return 'bg-yellow-500 hover:bg-yellow-600'
      case 'speaking': return 'bg-green-500 hover:bg-green-600'
      default: return 'bg-blue-500 hover:bg-blue-600'
    }
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Voice Interface */}
      <div className="text-center py-12">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">
          Voice Assistant
        </h1>
        <p className="text-gray-600 mb-8">
          {getStatusMessage()}
        </p>
        
        <button
          onClick={handleVoiceToggle}
          disabled={status !== 'ready'}
          className={`w-32 h-32 rounded-full text-white text-4xl transition-all duration-300 ${getButtonColor()} disabled:opacity-50`}
        >
          🎤
        </button>
        
        <p className="text-sm text-gray-500 mt-4">
          {status === 'ready' ? 'Tap to start speaking' : 'Processing...'}
        </p>
      </div>

      {/* Suggested Questions */}
      <Card>
        <CardHeader>
          <CardTitle>Suggested Questions</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <Button 
            variant="outline" 
            className="w-full text-left justify-start"
            onClick={() => alert('Voice query: How to apply for Ration card?')}
          >
            How to apply for Ration card?
          </Button>
          <Button 
            variant="outline" 
            className="w-full text-left justify-start"
            onClick={() => alert('Voice query: Where is the nearest PDS shop?')}
          >
            Where is the nearest PDS shop?
          </Button>
          <Button 
            variant="outline" 
            className="w-full text-left justify-start"
            onClick={() => alert('Voice query: What is Ayushman Bharat?')}
          >
            What is Ayushman Bharat?
          </Button>
        </CardContent>
      </Card>

      {/* Instructions */}
      <Card>
        <CardHeader>
          <CardTitle>How to Use</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm text-gray-600">
          <p>1. Tap the microphone button to start recording</p>
          <p>2. Speak your question clearly in any supported language</p>
          <p>3. Wait for the AI to process and respond</p>
          <p>4. Listen to the audio response or read the text</p>
        </CardContent>
      </Card>

      {/* Supported Languages */}
      <Card>
        <CardHeader>
          <CardTitle>Supported Languages</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-2 text-sm">
            <span className="bg-gray-100 px-3 py-1 rounded">English</span>
            <span className="bg-gray-100 px-3 py-1 rounded">Hindi</span>
            <span className="bg-gray-100 px-3 py-1 rounded">Marathi</span>
            <span className="bg-gray-100 px-3 py-1 rounded">Kannada</span>
            <span className="bg-gray-100 px-3 py-1 rounded">Tamil</span>
            <span className="bg-gray-100 px-3 py-1 rounded">Telugu</span>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
