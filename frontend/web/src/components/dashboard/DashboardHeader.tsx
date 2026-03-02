import React from 'react'
import { INDIAN_STATES, SUPPORTED_LANGUAGES } from '@/lib/constants'

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

            {/* Help Button */}
            <div className="flex flex-col justify-end">
              <button className="bg-white/10 border border-white/20 rounded-lg px-4 py-2 text-white hover:bg-white/20 transition-colors">
                <span className="text-lg">?</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}