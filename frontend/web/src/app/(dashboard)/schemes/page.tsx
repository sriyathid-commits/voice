'use client'

import { useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';

const INDIAN_STATES = [
  'All India', 'Maharashtra', 'Karnataka', 'Tamil Nadu', 'Telangana', 
  'Gujarat', 'Rajasthan', 'Uttar Pradesh', 'West Bengal', 'Kerala'
]

export default function SchemesPage() {
  const [selectedState, setSelectedState] = useState('All India')
  const [selectedCategory, setSelectedCategory] = useState('All')

  // Mock data for schemes with states
  const allSchemes = [
    {
      id: 1,
      name: "PM Kisan Samman Nidhi",
      description: "Financial support to farmers",
      eligibility: "Small and marginal farmers",
      amount: "₹6,000/year",
      state: "All India",
      category: "Agriculture",
      status: "Active"
    },
    {
      id: 2,
      name: "Pradhan Mantri Awas Yojana",
      description: "Housing for all scheme",
      eligibility: "EWS/LIG/MIG families",
      amount: "Up to ₹2.67 lakh subsidy",
      state: "All India",
      category: "Housing",
      status: "Active"
    },
    {
      id: 3,
      name: "Ayushman Bharat",
      description: "Health insurance scheme",
      eligibility: "Poor and vulnerable families",
      amount: "₹5 lakh coverage",
      state: "All India",
      category: "Healthcare",
      status: "Active"
    },
    {
      id: 4,
      name: "Maharashtra Farmer Support",
      description: "Additional support for Maharashtra farmers",
      eligibility: "Farmers in Maharashtra",
      amount: "₹10,000/year",
      state: "Maharashtra",
      category: "Agriculture",
      status: "Active"
    },
    {
      id: 5,
      name: "Karnataka Education Scholarship",
      description: "Scholarship for students",
      eligibility: "Students from Karnataka",
      amount: "₹25,000/year",
      state: "Karnataka",
      category: "Education",
      status: "Active"
    },
    {
      id: 6,
      name: "Tamil Nadu Health Scheme",
      description: "Free healthcare for all",
      eligibility: "Tamil Nadu residents",
      amount: "₹5 lakh coverage",
      state: "Tamil Nadu",
      category: "Healthcare",
      status: "Active"
    }
  ];

  const filteredSchemes = allSchemes.filter(scheme => {
    const stateMatch = selectedState === 'All India' || scheme.state === selectedState || scheme.state === 'All India'
    const categoryMatch = selectedCategory === 'All' || scheme.category === selectedCategory
    return stateMatch && categoryMatch
  })

  const categories = ['All', 'Agriculture', 'Healthcare', 'Housing', 'Education']

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center flex-wrap gap-4">
        <h1 className="text-2xl font-bold text-gray-900">Government Schemes</h1>
        <div className="flex gap-3">
          <select
            value={selectedState}
            onChange={(e) => setSelectedState(e.target.value)}
            className="px-4 py-2 border rounded-lg bg-white"
          >
            {INDIAN_STATES.map(state => (
              <option key={state} value={state}>{state}</option>
            ))}
          </select>
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="px-4 py-2 border rounded-lg bg-white"
          >
            {categories.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="text-sm text-gray-600">
        Showing {filteredSchemes.length} schemes for {selectedState}
      </div>

      <div className="grid gap-4">
        {filteredSchemes.map((scheme) => (
          <Card key={scheme.id} className="p-6">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {scheme.name}
                </h3>
                <p className="text-gray-600 mb-3">{scheme.description}</p>
              </div>
              <Badge variant="success">{scheme.status}</Badge>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
              <div>
                <p className="text-sm text-gray-500">Amount</p>
                <p className="font-medium">{scheme.amount}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Category</p>
                <p className="font-medium">{scheme.category}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">State</p>
                <p className="font-medium">{scheme.state}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Eligibility</p>
                <p className="font-medium text-sm">{scheme.eligibility}</p>
              </div>
            </div>

            <div className="flex gap-3">
              <Button variant="primary" size="sm">
                Check Eligibility
              </Button>
              <Button variant="secondary" size="sm">
                Save Scheme
              </Button>
              <Button variant="secondary" size="sm">
                View Details
              </Button>
            </div>
          </Card>
        ))}
      </div>

      <div className="text-center py-8">
        <p className="text-gray-500 mb-4">Looking for more schemes?</p>
        <Button variant="primary">
          Browse All Schemes
        </Button>
      </div>
    </div>
  );
}