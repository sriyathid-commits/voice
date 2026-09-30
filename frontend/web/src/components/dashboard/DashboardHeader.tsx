'use client'

import React from 'react'
import { useRouter } from 'next/navigation'
import { INDIAN_STATES, SUPPORTED_LANGUAGES } from '@/lib/constants'
import { useAuthStore } from '@/store/authStore'
import { useToast } from '@/components/ui/Toast'

interface DashboardHeaderProps {
  selectedState: string
  selectedLanguage: string
  onStateChange: (state: string) => void
  onLanguageChange: (language: string) => void
}

export function DashboardHeader({
  selectedState,
  selectedLanguage,
  onStateChange,
  onLanguageChange
}: DashboardHeaderProps) {
  const router = useRouter()
  const { logout, user } = useAuthStore()
  const { addToast } = useToast()
  
  const handleLogout = () => {
    logout()
    addToast('success', 'Logged out successfully')
    router.push('/login')
  }
  
  return (
    <div className="bg-gradient-to-r from-orange-500 to-green-500 text-white p-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between">
          <div className="mb-4 md:mb-0">
            <h1 className="text-2xl md:text-3xl font-bold">
              VOICE FOR BHARAT
            </h1>
            <p className="text-orange-100 text-sm md:text-base">
              NATIONAL DIGITAL INCLUSION PROJECT
            </p>
            {user && (
              <p className="text-orange-100 text-xs mt-1">
                Welcome, {user.profile?.name || user.phoneNumber}
              </p>
            )}
          </div>
          
          <div className="flex flex-col sm:flex-row gap-4">
            {/* State Selector */}
            <div className="flex flex-col">
              <label className="text-xs font-medium text-orange-100 mb-1">
                STATE
              </label>
              <select
                value={selectedState}
                onChange={(e) => onStateChange(e.target.value)}
                className="bg-white/10 border border-white/20 rounded-lg px-3 py-2 text-white placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-white/50"
              >
                {INDIAN_STATES.map((state) => (
                  <option key={state} value={state} className="text-gray-900">
                    {state}
                  </option>
                ))}
              </select>
            </div>

            {/* Language Selector */}
            <div className="flex flex-col">
              <label className="text-xs font-medium text-orange-100 mb-1">
                LANGUAGE
              </label>
              <select
                value={selectedLanguage}
                onChange={(e) => onLanguageChange(e.target.value)}
                className="bg-white/10 border border-white/20 rounded-lg px-3 py-2 text-white placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-white/50"
              >
                {SUPPORTED_LANGUAGES.map((lang) => (
                  <option key={lang.code} value={lang.code} className="text-gray-900">
                    {lang.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Logout Button */}
            <div className="flex flex-col justify-end">
              <button 
                onClick={handleLogout}
                className="bg-white/10 border border-white/20 rounded-lg px-4 py-2 text-white hover:bg-white/20 transition-colors flex items-center gap-2"
                title="Logout"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                <span className="hidden sm:inline">Logout</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}