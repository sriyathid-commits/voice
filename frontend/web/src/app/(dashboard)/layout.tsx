'use client'

import React, { useState } from 'react'
import { DashboardHeader } from '@/components/dashboard/DashboardHeader'
import { TabNavigation } from '@/components/dashboard/TabNavigation'

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const [selectedState, setSelectedState] = useState('Karnataka')
  const [selectedLanguage, setSelectedLanguage] = useState('en')

  return (
    <div className="min-h-screen bg-gray-50">
      <DashboardHeader
        selectedState={selectedState}
        selectedLanguage={selectedLanguage}
        onStateChange={setSelectedState}
        onLanguageChange={setSelectedLanguage}
      />
      <TabNavigation />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  )
}
