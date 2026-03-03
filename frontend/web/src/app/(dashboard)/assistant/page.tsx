'use client'

import React, { useState, useRef } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'

const API_URL = 'https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev'

export default function AssistantPage() {
  const [status, setStatus] = useState<'ready' | 'listening' | 'processing' | 'speaking'>('ready')
  const [transcript, setTranscript] = useState<string>('')
  const [response, setResponse] = useState<string>('')
  const [language, setLanguage] = useState<string>('hi')
  const [error, setError] = useState<string>('')
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const audioChunksRef = useRef<Blob[]>([])
  const audioRef = useRef<HTMLAudioElement | null>(null)

  const handleVoiceToggle = async () => {
    if (status === 'ready') {
      try {
        setError('')
        setTranscript('')
        setResponse('')
        
        // Request microphone access
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        
        // Create MediaRecorder
        const mediaRecorder = new MediaRecorder(stream)
        mediaRecorderRef.current = mediaRecorder
        audioChunksRef.current = []
        
        mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            audioChunksRef.current.push(event.data)
          }
        }
        
        mediaRecorder.onstop = async () => {
          // Stop all tracks
          stream.getTracks().forEach(track => track.stop())
          
          // Create audio blob
          const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' })
          
          // Send to backend
          await processVoiceQuery(audioBlob)
        }
        
        // Start recording
        mediaRecorder.start()
        setStatus('listening')
        
        // Auto-stop after 5 seconds
        setTimeout(() => {
          if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
            mediaRecorderRef.current.stop()
          }
        }, 5000)
        
      } catch (err) {
        console.error('Error accessing microphone:', err)
        setError('Could not access microphone. Please allow microphone access.')
        setStatus('ready')
      }
    } else if (status === 'listening') {
      // Stop recording manually
      if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
        mediaRecorderRef.current.stop()
      }
    }
  }
  
  const processVoiceQuery = async (audioBlob: Blob) => {
    setStatus('processing')
    
    try {
      // Create FormData
      const formData = new FormData()
      formData.append('audio', audioBlob, 'recording.wav')
      formData.append('session_id', `session-${Date.now()}`)
      formData.append('language', language)
      formData.append('user_id', 'demo-user')
      
      // Send to backend
      const response = await fetch(`${API_URL}/voice/query`, {
        method: 'POST',
        body: formData,
      })
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`)
      }
      
      const data = await response.json()
      
      // Update UI with response
      setTranscript(data.user_text || 'Could not transcribe audio')
      setResponse(data.response_text || 'No response generated')
      
      // Play audio response if available
      if (data.audio_url) {
        setStatus('speaking')
        playAudioResponse(data.audio_url)
      } else {
        setStatus('ready')
      }
      
    } catch (err) {
      console.error('Error processing voice query:', err)
      setError('Failed to process voice query. Please try again.')
      setStatus('ready')
    }
  }
  
  const playAudioResponse = (audioUrl: string) => {
    const audio = new Audio(audioUrl)
    audioRef.current = audio
    
    audio.onended = () => {
      setStatus('ready')
    }
    
    audio.onerror = () => {
      console.error('Error playing audio')
      setStatus('ready')
    }
    
    audio.play().catch(err => {
      console.error('Error playing audio:', err)
      setStatus('ready')
    })
  }

  const getStatusMessage = () => {
    switch (status) {
      case 'ready': return 'Ready to Help'
      case 'listening': return 'Listening... (speak now)'
      case 'processing': return 'Processing with AI...'
      case 'speaking': return 'Playing response...'
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
        <p className="text-gray-600 mb-4">
          {getStatusMessage()}
        </p>
        
        {/* Language Selector */}
        <div className="mb-6">
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            disabled={status !== 'ready'}
            className="px-4 py-2 border rounded-lg"
          >
            <option value="en">English</option>
            <option value="hi">Hindi (हिंदी)</option>
            <option value="ta">Tamil (தமிழ்)</option>
            <option value="te">Telugu (తెలుగు)</option>
            <option value="mr">Marathi (मराठी)</option>
            <option value="kn">Kannada (ಕನ್ನಡ)</option>
          </select>
        </div>
        
        <button
          onClick={handleVoiceToggle}
          disabled={status === 'processing' || status === 'speaking'}
          className={`w-32 h-32 rounded-full text-white text-4xl transition-all duration-300 ${getButtonColor()} disabled:opacity-50`}
        >
          {status === 'listening' ? '⏹️' : '🎤'}
        </button>
        
        <p className="text-sm text-gray-500 mt-4">
          {status === 'ready' && 'Tap to start speaking'}
          {status === 'listening' && 'Recording... (tap to stop or wait 5 sec)'}
          {status === 'processing' && 'AI is processing your query...'}
          {status === 'speaking' && 'Playing AI response...'}
        </p>
        
        {error && (
          <div className="mt-4 p-3 bg-red-100 text-red-700 rounded-lg">
            {error}
          </div>
        )}
      </div>

      {/* Transcript and Response */}
      {(transcript || response) && (
        <Card>
          <CardHeader>
            <CardTitle>Conversation</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {transcript && (
              <div>
                <p className="text-sm font-semibold text-gray-700 mb-1">You said:</p>
                <p className="text-gray-900 bg-blue-50 p-3 rounded">{transcript}</p>
              </div>
            )}
            {response && (
              <div>
                <p className="text-sm font-semibold text-gray-700 mb-1">AI Response:</p>
                <p className="text-gray-900 bg-green-50 p-3 rounded">{response}</p>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Suggested Questions */}
      <Card>
        <CardHeader>
          <CardTitle>Try These Questions</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="text-sm text-gray-600 space-y-2">
            <p>• &quot;मुझे राशन कार्ड चाहिए&quot; (I need a ration card)</p>
            <p>• &quot;How to apply for Ayushman Bharat?&quot;</p>
            <p>• &quot;What schemes are available for farmers?&quot;</p>
            <p>• &quot;Tell me about education scholarships&quot;</p>
          </div>
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
