'use client'

import React, { useState, useEffect } from 'react'
import { MetricCard } from '@/components/dashboard/MetricCard'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'

interface DashboardData {
  activeSchemes: number
  helplines: number
  applications: number
  savedSchemes: number
}

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData>({
    activeSchemes: 0,
    helplines: 0,
    applications: 0,
    savedSchemes: 0
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      setLoading(true)
      setError(null)
      
      // For now, use mock data since we need to implement the backend endpoints
      // In production, these would be real API calls:
      // const schemes = await api.get('/schemes?isActive=true')
      // const helplines = await api.get('/helplines')
      // const applications = await api.get('/applications')
      
      // Mock data for demonstration
      setTimeout(() => {
        setData({
          activeSchemes: 156,
          helplines: 24,
          applications: 3,
          savedSchemes: 8
        })
        setLoading(false)
      }, 1000)
      
    } catch (err) {
      console.error('Failed to load dashboard data:', err)
      setError('Failed to load dashboard data')
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="bg-gray-200 animate-pulse rounded-xl h-24"></div>
          ))}
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600 mb-4">{error}</p>
        <Button onClick={loadDashboardData}>Try Again</Button>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <MetricCard
          title="Active Schemes"
          count={data.activeSchemes}
          icon={<div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white text-sm">📋</div>}
          backgroundColor="bg-blue-50"
          onClick={() => window.location.href = '/schemes'}
        />
        
        <MetricCard
          title="Helplines"
          count={data.helplines}
          icon={<div className="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center text-white text-sm">📞</div>}
          backgroundColor="bg-orange-50"
          onClick={() => window.location.href = '/helplines'}
        />
      </div>

      {/* Status Items */}
      <div className="space-y-4">
        <h2 className="text-lg font-semibold text-gray-900">Status Updates</h2>
        
        <Card>
          <CardContent className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                <span className="text-green-600">🍚</span>
              </div>
              <div>
                <h3 className="font-medium text-gray-900">Ration Card Status</h3>
                <p className="text-sm text-gray-500">Your ration card application is approved</p>
              </div>
            </div>
            <Button variant="outline" size="sm">VIEW</Button>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                <span className="text-blue-600">🆔</span>
              </div>
              <div>
                <h3 className="font-medium text-gray-900">Aadhaar Seeding</h3>
                <p className="text-sm text-gray-500">Bank account linked successfully</p>
              </div>
            </div>
            <Badge variant="success">ACTIVE</Badge>
          </CardContent>
        </Card>
      </div>

      {/* Quick Guide */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Guide Summary</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-3">
            <div>
              <h4 className="font-medium text-gray-900">How to apply for Ration card?</h4>
              <p className="text-sm text-gray-600">Visit your nearest PDS shop with required documents including Aadhaar card, address proof, and income certificate.</p>
            </div>
            <div>
              <h4 className="font-medium text-gray-900">What is Ayushman Bharat?</h4>
              <p className="text-sm text-gray-600">A national health insurance scheme providing coverage up to ₹5 lakh per family per year for secondary and tertiary care hospitalization.</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Primary CTA */}
      <div className="text-center py-8">
        <Button 
          size="lg" 
          className="bg-navy-800 hover:bg-navy-900 text-white px-8 py-4 text-lg"
          onClick={() => window.location.href = '/assistant'}
        >
          <span className="mr-2">🎤</span>
          TALK TO THE ASSISTANT
        </Button>
      </div>

      {/* Footer Links */}
      <div className="flex justify-center space-x-6 text-sm text-gray-500 py-4">
        <a href="/data-access" className="hover:text-gray-700">OFFICIAL DATA ACCESS</a>
        <a href="/privacy" className="hover:text-gray-700">PRIVACY</a>
        <a href="/terms" className="hover:text-gray-700">TERMS</a>
      </div>
    </div>
  )
}