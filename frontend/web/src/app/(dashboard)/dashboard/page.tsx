'use client'

import React, { useState, useEffect } from 'react'
import { MetricCard } from '@/components/dashboard/MetricCard'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'

const INDIAN_STATES = [
  'All India', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
  'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka',
  'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
  'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
  'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'
]

interface DashboardData {
  activeSchemes: number
  helplines: number
  applications: number
  savedSchemes: number
}

export default function DashboardPage() {
  const [selectedState, setSelectedState] = useState('All India')
  const [locationDetected, setLocationDetected] = useState(false)
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
    detectLocation()
  }, [])

  const detectLocation = () => {
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          // Simple state detection based on coordinates
          // In production, use reverse geocoding API
          const { latitude, longitude } = position.coords
          const detectedState = getStateFromCoordinates(latitude, longitude)
          if (detectedState) {
            setSelectedState(detectedState)
            setLocationDetected(true)
          }
        },
        () => {
          console.log('Location access denied or unavailable')
        }
      )
    }
  }

  const getStateFromCoordinates = (lat: number, lng: number): string | null => {
    // Approximate state detection (simplified)
    // Maharashtra: 18-21°N, 72-80°E
    if (lat >= 18 && lat <= 21 && lng >= 72 && lng <= 80) return 'Maharashtra'
    // Karnataka: 12-18°N, 74-78°E
    if (lat >= 12 && lat <= 18 && lng >= 74 && lng <= 78) return 'Karnataka'
    // Tamil Nadu: 8-13°N, 76-80°E
    if (lat >= 8 && lat <= 13 && lng >= 76 && lng <= 80) return 'Tamil Nadu'
    // Telangana: 16-19°N, 77-81°E
    if (lat >= 16 && lat <= 19 && lng >= 77 && lng <= 81) return 'Telangana'
    // Gujarat: 20-24°N, 68-74°E
    if (lat >= 20 && lat <= 24 && lng >= 68 && lng <= 74) return 'Gujarat'
    // Rajasthan: 24-30°N, 69-78°E
    if (lat >= 24 && lat <= 30 && lng >= 69 && lng <= 78) return 'Rajasthan'
    // West Bengal: 22-27°N, 85-89°E
    if (lat >= 22 && lat <= 27 && lng >= 85 && lng <= 89) return 'West Bengal'
    // Kerala: 8-13°N, 74-77°E
    if (lat >= 8 && lat <= 13 && lng >= 74 && lng <= 77) return 'Kerala'
    return null
  }

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
      {/* State Selector */}
      <div className="flex justify-between items-center flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          {locationDetected && (
            <p className="text-sm text-green-600 mt-1">📍 Location detected: {selectedState}</p>
          )}
        </div>
        <select
          value={selectedState}
          onChange={(e) => setSelectedState(e.target.value)}
          className="px-4 py-2 border rounded-lg bg-white"
        >
          {INDIAN_STATES.map(state => (
            <option key={state} value={state}>{state}</option>
          ))}
        </select>
      </div>

      {/* Portal Status Section */}
      <Card>
        <CardHeader>
          <CardTitle>Government Portal Status</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
              <span className="text-sm font-medium">National Portal</span>
              <Badge variant="success">Online</Badge>
            </div>
            <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
              <span className="text-sm font-medium">{selectedState} Portal</span>
              <Badge variant="success">Online</Badge>
            </div>
            <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
              <span className="text-sm font-medium">Application System</span>
              <Badge variant="success">Active</Badge>
            </div>
          </div>
        </CardContent>
      </Card>
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