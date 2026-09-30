'use client'

import React, { useState, useRef, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { useVoiceStore } from '@/store/voiceStore'
import { useSchemeStore } from '@/store/schemeStore'
import { useAuthStore } from '@/store/authStore'
import { useToast } from '@/components/ui/Toast'
import { API_URL, SUPPORTED_LANGUAGES } from '@/lib/constants'

export default function VoiceAssistant() {
  const {
    isRecording,
    isProcessing,
    isSpeaking,
    sessionId,
    messages,
    citizenProfile,
    currentTranscript,
    currentResponse,
    currentAudioUrl,
    selectedLanguage,
    profileGaps,
    error,
    setRecording,
    setProcessing,
    setSpeaking,
    setSessionId,
    addMessage,
    updateCitizenProfile,
    setCurrentTranscript,
    setCurrentResponse,
    setCurrentAudioUrl,
    setSelectedLanguage,
    setError,
    resetVoiceState
  } = useVoiceStore()
  
  const { clearSchemeData } = useSchemeStore()
  const { user, token } = useAuthStore()
  const { addToast } = useToast()
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const audioChunksRef = useRef<Blob[]>([])
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const [recordingDuration, setRecordingDuration] = useState(0)
  const recordingTimerRef = useRef<NodeJS.Timeout | null>(null)

  // Auto-stop recording after 10 seconds
  useEffect(() => {
    if (isRecording) {
      recordingTimerRef.current = setInterval(() => {
        setRecordingDuration((prev) => {
          if (prev >= 9) {
            handleStopRecording()
            return 0
          }
          return prev + 1
        })
      }, 1000)
    } else {
      if (recordingTimerRef.current) {
        clearInterval(recordingTimerRef.current)
      }
      setRecordingDuration(0)
    }
    
    return () => {
      if (recordingTimerRef.current) {
        clearInterval(recordingTimerRef.current)
      }
    }
  }, [isRecording])

  const handleStartRecording = async () => {
    try {
      setError(null)
      resetVoiceState()
      
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
      setRecording(true)
      addToast('info', 'Recording started. Speak now!')
      
    } catch (err) {
      console.error('Error accessing microphone:', err)
      const errorMsg = 'Could not access microphone. Please allow microphone access.'
      setError(errorMsg)
      addToast('error', errorMsg)
      setRecording(false)
    }
  }
  
  const handleStopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop()
      setRecording(false)
      addToast('success', 'Recording stopped. Processing...')
    }
  }
  
  const processVoiceQuery = async (audioBlob: Blob) => {
    setProcessing(true)
    
    try {
      // Create FormData
      const formData = new FormData()
      formData.append('audio', audioBlob, 'recording.wav')
      formData.append('session_id', sessionId || '')
      formData.append('language', selectedLanguage)
      formData.append('user_id', user?.userId || 'demo-user')
      
      // Send to backend
      const response = await fetch(`${API_URL}/voice/query`, {
        method: 'POST',
        headers: token ? {
          'Authorization': `Bearer ${token}`
        } : {},
        body: formData,
      })
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`)
      }
      
      const data = await response.json()
      
      // Update state with response
      setSessionId(data.session_id)
      setCurrentTranscript(data.user_text || 'Could not transcribe audio')
      setCurrentResponse(data.response_text || 'No response generated')
      
      // Update citizen profile
      if (data.citizen_profile) {
        updateCitizenProfile(data.citizen_profile)
      }
      
      // Add messages to history
      if (data.user_text) {
        addMessage({
          message_id: `user-${Date.now()}`,
          role: 'USER',
          content: data.user_text,
          timestamp: new Date().toISOString()
        })
      }
      
      if (data.response_text) {
        addMessage({
          message_id: `assistant-${Date.now()}`,
          role: 'ASSISTANT',
          content: data.response_text,
          audio_url: data.audio_url,
          timestamp: new Date().toISOString(),
          intent: data.current_intent
        })
      }
      
      // Play audio response if available
      if (data.audio_url) {
        setCurrentAudioUrl(data.audio_url)
        playAudioResponse(data.audio_url)
      } else {
        setProcessing(false)
      }
      
      addToast('success', 'Voice query processed successfully!')
      
    } catch (err) {
      console.error('Error processing voice query:', err)
      const errorMsg = 'Failed to process voice query. Please try again.'
      setError(errorMsg)
      addToast('error', errorMsg)
      setProcessing(false)
    }
  }
  
  const playAudioResponse = (audioUrl: string) => {
    setSpeaking(true)
    const audio = new Audio(audioUrl)
    audioRef.current = audio
    
    audio.onended = () => {
      setSpeaking(false)
      setProcessing(false)
    }
    
    audio.onerror = () => {
      console.error('Error playing audio')
      setSpeaking(false)
      setProcessing(false)
      addToast('error', 'Could not play audio response')
    }
    
    audio.play().catch(err => {
      console.error('Error playing audio:', err)
      setSpeaking(false)
      setProcessing(false)
    })
  }

  const handleLanguageChange = (langCode: string) => {
    setSelectedLanguage(langCode)
    clearSchemeData()
    addToast('info', `Language changed to ${SUPPORTED_LANGUAGES.find(l => l.code === langCode)?.name}`)
  }

  const getStatusMessage = () => {
    if (isSpeaking) return 'Speaking...'
    if (isProcessing) return 'Processing with AI...'
    if (isRecording) return `Recording... (${recordingDuration}s)`
    return 'Ready to Help'
  }

  const getButtonColor = () => {
    if (isRecording) return 'bg-red-500 hover:bg-red-600 animate-pulse'
    if (isProcessing) return 'bg-yellow-500 hover:bg-yellow-600'
    if (isSpeaking) return 'bg-green-500 hover:bg-green-600 animate-pulse'
    return 'bg-blue-500 hover:bg-blue-600'
  }

  const getButtonIcon = () => {
    if (isSpeaking) return '🔊'
    if (isProcessing) return '⏳'
    if (isRecording) return '⏹️'
    return '🎤'
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Voice Interface */}
      <Card>
        <CardContent className="pt-6">
          <div className="text-center space-y-6">
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-2">
                Voice Assistant
              </h2>
              <p className="text-sm text-gray-600">
                {getStatusMessage()}
              </p>
            </div>
            
            {/* Language Selector */}
            <div className="flex justify-center">
              <select
                value={selectedLanguage}
                onChange={(e) => handleLanguageChange(e.target.value)}
                disabled={isRecording || isProcessing || isSpeaking}
                className="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {SUPPORTED_LANGUAGES.map((lang) => (
                  <option key={lang.code} value={lang.code}>
                    {lang.name}
                  </option>
                ))}
              </select>
            </div>
            
            {/* Microphone Button */}
            <div className="flex justify-center">
              <button
                onClick={isRecording ? handleStopRecording : handleStartRecording}
                disabled={isProcessing || isSpeaking}
                className={`w-24 h-24 rounded-full text-white text-5xl transition-all duration-300 shadow-lg ${getButtonColor()} disabled:opacity-50 disabled:cursor-not-allowed`}
              >
                {getButtonIcon()}
              </button>
            </div>
            
            <p className="text-xs text-gray-500">
              {!isRecording && !isProcessing && !isSpeaking && 'Tap to start speaking'}
              {isRecording && 'Tap to stop or wait 10 seconds'}
              {isProcessing && 'AI is processing your query...'}
              {isSpeaking && 'Playing AI response...'}
            </p>
            
            {error && (
              <div className="p-3 bg-red-100 text-red-700 rounded-lg text-sm">
                {error}
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Citizen Profile Status */}
      {(citizenProfile.state || citizenProfile.occupation) && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Your Profile</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3 text-sm">
              {citizenProfile.state && (
                <div>
                  <span className="text-gray-600">State: </span>
                  <span className="font-medium">{citizenProfile.state}</span>
                </div>
              )}
              {citizenProfile.occupation && (
                <div>
                  <span className="text-gray-600">Occupation: </span>
                  <span className="font-medium">{citizenProfile.occupation}</span>
                </div>
              )}
              {citizenProfile.age && (
                <div>
                  <span className="text-gray-600">Age: </span>
                  <span className="font-medium">{citizenProfile.age}</span>
                </div>
              )}
              {citizenProfile.is_farmer !== undefined && (
                <div>
                  <span className="text-gray-600">Farmer: </span>
                  <span className="font-medium">{citizenProfile.is_farmer ? 'Yes' : 'No'}</span>
                </div>
              )}
            </div>
            
            {profileGaps.length > 0 && (
              <div className="mt-3 pt-3 border-t">
                <p className="text-xs text-gray-500">
                  Missing info: {profileGaps.join(', ')}
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Conversation History */}
      {messages.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Conversation</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 max-h-96 overflow-y-auto">
            {messages.map((msg) => (
              <div
                key={msg.message_id}
                className={`p-3 rounded-lg ${
                  msg.role === 'USER'
                    ? 'bg-blue-50 ml-8'
                    : 'bg-green-50 mr-8'
                }`}
              >
                <p className="text-xs font-semibold text-gray-700 mb-1">
                  {msg.role === 'USER' ? 'You' : 'AI Assistant'}
                  {msg.intent && (
                    <span className="ml-2 text-gray-500">({msg.intent})</span>
                  )}
                </p>
                <p className="text-sm text-gray-900">{msg.content}</p>
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      {/* Current Interaction */}
      {(currentTranscript || currentResponse) && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Latest Exchange</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {currentTranscript && (
              <div>
                <p className="text-xs font-semibold text-gray-700 mb-1">You said:</p>
                <p className="text-sm text-gray-900 bg-blue-50 p-3 rounded">
                  {currentTranscript}
                </p>
              </div>
            )}
            {currentResponse && (
              <div>
                <p className="text-xs font-semibold text-gray-700 mb-1">AI Response:</p>
                <p className="text-sm text-gray-900 bg-green-50 p-3 rounded">
                  {currentResponse}
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Suggested Questions */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Try These Questions</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm text-gray-600">
          {selectedLanguage === 'te' && (
            <>
              <p>• &quot;నాకు రైతులకు సంబంధించిన ప్రభుత్వ పథకాలు కావాలి&quot;</p>
              <p>• &quot;ఇప్పుడు నేను ఏమి చేయాలి?&quot;</p>
            </>
          )}
          {selectedLanguage === 'hi' && (
            <>
              <p>• &quot;मुझे राशन कार्ड चाहिए&quot;</p>
              <p>• &quot;मुझे किसान योजनाओं के बारे में बताएं&quot;</p>
            </>
          )}
          {selectedLanguage === 'en' && (
            <>
              <p>• &quot;I need farmer schemes&quot;</p>
              <p>• &quot;What schemes are available for students?&quot;</p>
            </>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const audioChunksRef = useRef<Blob[]>([])
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const [recordingDuration, setRecordingDuration] = useState(0)
  const recordingTimerRef = useRef<NodeJS.Timeout | null>(null)

  // Auto-stop recording after 10 seconds
  useEffect(() => {
    if (isRecording) {
      recordingTimerRef.current = setInterval(() => {
        setRecordingDuration((prev) => {
          if (prev >= 9) {
            handleStopRecording()
            return 0
          }
          return prev + 1
        })
      }, 1000)
    } else {
      if (recordingTimerRef.current) {
        clearInterval(recordingTimerRef.current)
      }
      setRecordingDuration(0)
    }
    
    return () => {
      if (recordingTimerRef.current) {
        clearInterval(recordingTimerRef.current)
      }
    }
  }, [isRecording])

  const handleStartRecording = async () => {
    try {
      setError(null)
      resetVoiceState()
      
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
      setRecording(true)
      
    } catch (err) {
      console.error('Error accessing microphone:', err)
      setError('Could not access microphone. Please allow microphone access.')
      setRecording(false)
    }
  }
  
  const handleStopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop()
      setRecording(false)
    }
  }
  
  const processVoiceQuery = async (audioBlob: Blob) => {
    setProcessing(true)
    
    try {
      // Create FormData
      const formData = new FormData()
      formData.append('audio', audioBlob, 'recording.wav')
      formData.append('session_id', sessionId || '')
      formData.append('language', selectedLanguage)
      formData.append('user_id', 'demo-user') // TODO: Get from auth
      
      // Send to backend
      const response = await fetch(`${API_URL}/voice/query`, {
        method: 'POST',
        body: formData,
      })
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`)
      }
      
      const data = await response.json()
      
      // Update state with response
      setSessionId(data.session_id)
      setCurrentTranscript(data.user_text || 'Could not transcribe audio')
      setCurrentResponse(data.response_text || 'No response generated')
      
      // Update citizen profile
      if (data.citizen_profile) {
        updateCitizenProfile(data.citizen_profile)
      }
      
      // Add messages to history
      if (data.user_text) {
        addMessage({
          message_id: `user-${Date.now()}`,
          role: 'USER',
          content: data.user_text,
          timestamp: new Date().toISOString()
        })
      }
      
      if (data.response_text) {
        addMessage({
          message_id: `assistant-${Date.now()}`,
          role: 'ASSISTANT',
          content: data.response_text,
          audio_url: data.audio_url,
          timestamp: new Date().toISOString(),
          intent: data.current_intent
        })
      }
      
      // Play audio response if available
      if (data.audio_url) {
        setCurrentAudioUrl(data.audio_url)
        playAudioResponse(data.audio_url)
      } else {
        setProcessing(false)
      }
      
    } catch (err) {
      console.error('Error processing voice query:', err)
      setError('Failed to process voice query. Please try again.')
      setProcessing(false)
    }
  }
  
  const playAudioResponse = (audioUrl: string) => {
    setSpeaking(true)
    const audio = new Audio(audioUrl)
    audioRef.current = audio
    
    audio.onended = () => {
      setSpeaking(false)
      setProcessing(false)
    }
    
    audio.onerror = () => {
      console.error('Error playing audio')
      setSpeaking(false)
      setProcessing(false)
    }
    
    audio.play().catch(err => {
      console.error('Error playing audio:', err)
      setSpeaking(false)
      setProcessing(false)
    })
  }

  const handleLanguageChange = (langCode: string) => {
    setSelectedLanguage(langCode)
    clearSchemeData()
  }

  const getStatusMessage = () => {
    if (isSpeaking) return 'Speaking...'
    if (isProcessing) return 'Processing with AI...'
    if (isRecording) return `Recording... (${recordingDuration}s)`
    return 'Ready to Help'
  }

  const getButtonColor = () => {
    if (isRecording) return 'bg-red-500 hover:bg-red-600 animate-pulse'
    if (isProcessing) return 'bg-yellow-500 hover:bg-yellow-600'
    if (isSpeaking) return 'bg-green-500 hover:bg-green-600 animate-pulse'
    return 'bg-blue-500 hover:bg-blue-600'
  }

  const getButtonIcon = () => {
    if (isSpeaking) return '🔊'
    if (isProcessing) return '⏳'
    if (isRecording) return '⏹️'
    return '🎤'
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Voice Interface */}
      <Card>
        <CardContent className="pt-6">
          <div className="text-center space-y-6">
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-2">
                Voice Assistant
              </h2>
              <p className="text-sm text-gray-600">
                {getStatusMessage()}
              </p>
            </div>
            
            {/* Language Selector */}
            <div className="flex justify-center">
              <select
                value={selectedLanguage}
                onChange={(e) => handleLanguageChange(e.target.value)}
                disabled={isRecording || isProcessing || isSpeaking}
                className="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {LANGUAGES.map((lang) => (
                  <option key={lang.code} value={lang.code}>
                    {lang.nativeName}
                  </option>
                ))}
              </select>
            </div>
            
            {/* Microphone Button */}
            <div className="flex justify-center">
              <button
                onClick={isRecording ? handleStopRecording : handleStartRecording}
                disabled={isProcessing || isSpeaking}
                className={`w-24 h-24 rounded-full text-white text-5xl transition-all duration-300 shadow-lg ${getButtonColor()} disabled:opacity-50 disabled:cursor-not-allowed`}
              >
                {getButtonIcon()}
              </button>
            </div>
            
            <p className="text-xs text-gray-500">
              {!isRecording && !isProcessing && !isSpeaking && 'Tap to start speaking'}
              {isRecording && 'Tap to stop or wait 10 seconds'}
              {isProcessing && 'AI is processing your query...'}
              {isSpeaking && 'Playing AI response...'}
            </p>
            
            {error && (
              <div className="p-3 bg-red-100 text-red-700 rounded-lg text-sm">
                {error}
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Citizen Profile Status */}
      {(citizenProfile.state || citizenProfile.occupation) && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Your Profile</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3 text-sm">
              {citizenProfile.state && (
                <div>
                  <span className="text-gray-600">State: </span>
                  <span className="font-medium">{citizenProfile.state}</span>
                </div>
              )}
              {citizenProfile.occupation && (
                <div>
                  <span className="text-gray-600">Occupation: </span>
                  <span className="font-medium">{citizenProfile.occupation}</span>
                </div>
              )}
              {citizenProfile.age && (
                <div>
                  <span className="text-gray-600">Age: </span>
                  <span className="font-medium">{citizenProfile.age}</span>
                </div>
              )}
              {citizenProfile.is_farmer !== undefined && (
                <div>
                  <span className="text-gray-600">Farmer: </span>
                  <span className="font-medium">{citizenProfile.is_farmer ? 'Yes' : 'No'}</span>
                </div>
              )}
            </div>
            
            {profileGaps.length > 0 && (
              <div className="mt-3 pt-3 border-t">
                <p className="text-xs text-gray-500">
                  Missing info: {profileGaps.join(', ')}
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Conversation History */}
      {messages.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Conversation</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 max-h-96 overflow-y-auto">
            {messages.map((msg) => (
              <div
                key={msg.message_id}
                className={`p-3 rounded-lg ${
                  msg.role === 'USER'
                    ? 'bg-blue-50 ml-8'
                    : 'bg-green-50 mr-8'
                }`}
              >
                <p className="text-xs font-semibold text-gray-700 mb-1">
                  {msg.role === 'USER' ? 'You' : 'AI Assistant'}
                  {msg.intent && (
                    <span className="ml-2 text-gray-500">({msg.intent})</span>
                  )}
                </p>
                <p className="text-sm text-gray-900">{msg.content}</p>
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      {/* Current Interaction */}
      {(currentTranscript || currentResponse) && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Latest Exchange</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {currentTranscript && (
              <div>
                <p className="text-xs font-semibold text-gray-700 mb-1">You said:</p>
                <p className="text-sm text-gray-900 bg-blue-50 p-3 rounded">
                  {currentTranscript}
                </p>
              </div>
            )}
            {currentResponse && (
              <div>
                <p className="text-xs font-semibold text-gray-700 mb-1">AI Response:</p>
                <p className="text-sm text-gray-900 bg-green-50 p-3 rounded">
                  {currentResponse}
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Suggested Questions */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Try These Questions</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm text-gray-600">
          {selectedLanguage === 'te' && (
            <>
              <p>• &quot;నాకు రైతులకు సంబంధించిన ప్రభుత్వ పథకాలు కావాలి&quot;</p>
              <p>• &quot;ఇప్పుడు నేను ఏమి చేయాలి?&quot;</p>
            </>
          )}
          {selectedLanguage === 'hi' && (
            <>
              <p>• &quot;मुझे राशన कार्ड चाहिए&quot;</p>
              <p>• &quot;मुझे किसान योजनाओं के बारे में बताएं&quot;</p>
            </>
          )}
          {selectedLanguage === 'en' && (
            <>
              <p>• &quot;I need farmer schemes&quot;</p>
              <p>• &quot;What schemes are available for students?&quot;</p>
            </>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
