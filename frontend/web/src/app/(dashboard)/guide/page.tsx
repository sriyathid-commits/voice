'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'

export default function GuidePage() {
  const guides = [
    {
      title: "How to Apply for Ration Card",
      category: "Food Security",
      steps: [
        "Visit your nearest PDS shop or Tehsildar office",
        "Carry required documents: Aadhaar card, address proof, income certificate",
        "Fill the application form completely",
        "Submit the form with documents and get acknowledgment receipt",
        "Track your application status online or visit office after 15 days"
      ]
    },
    {
      title: "Ayushman Bharat Registration",
      category: "Healthcare",
      steps: [
        "Check eligibility on the official Ayushman Bharat website",
        "Visit nearest Common Service Center (CSC) or hospital",
        "Carry Aadhaar card and family details",
        "Get your eligibility verified by the operator",
        "Receive your Ayushman Bharat card if eligible"
      ]
    },
    {
      title: "PM Kisan Samman Nidhi",
      category: "Agriculture",
      steps: [
        "Visit PM Kisan portal or nearest CSC",
        "Register with Aadhaar number and bank account details",
        "Upload land ownership documents",
        "Verify mobile number with OTP",
        "Check payment status regularly on the portal"
      ]
    }
  ]

  const faqs = [
    {
      question: "What documents do I need for most government schemes?",
      answer: "Common documents include Aadhaar card, PAN card, bank account details, income certificate, caste certificate (if applicable), and address proof."
    },
    {
      question: "How long does it take to process applications?",
      answer: "Processing time varies by scheme. Most applications are processed within 15-30 days. You can track status online or through the voice assistant."
    },
    {
      question: "Can I apply for multiple schemes at once?",
      answer: "Yes, you can apply for multiple schemes simultaneously if you meet the eligibility criteria for each scheme."
    }
  ]

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Complete Guide
        </h1>
        <p className="text-gray-600">
          Step-by-step instructions for government welfare schemes
        </p>
      </div>

      {/* Application Guides */}
      <div className="space-y-6">
        <h2 className="text-xl font-semibold text-gray-900">Application Guides</h2>
        
        {guides.map((guide, index) => (
          <Card key={index}>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>{guide.title}</CardTitle>
                <Badge variant="info">{guide.category}</Badge>
              </div>
            </CardHeader>
            <CardContent>
              <ol className="space-y-2">
                {guide.steps.map((step, stepIndex) => (
                  <li key={stepIndex} className="flex items-start">
                    <span className="flex-shrink-0 w-6 h-6 bg-orange-500 text-white text-sm rounded-full flex items-center justify-center mr-3 mt-0.5">
                      {stepIndex + 1}
                    </span>
                    <span className="text-gray-700">{step}</span>
                  </li>
                ))}
              </ol>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* FAQs */}
      <div className="space-y-6">
        <h2 className="text-xl font-semibold text-gray-900">Frequently Asked Questions</h2>
        
        {faqs.map((faq, index) => (
          <Card key={index}>
            <CardHeader>
              <CardTitle className="text-lg">{faq.question}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700">{faq.answer}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Contact Information */}
      <Card>
        <CardHeader>
          <CardTitle>Need More Help?</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-center space-x-3">
              <span className="text-2xl">🎤</span>
              <div>
                <h4 className="font-medium">Voice Assistant</h4>
                <p className="text-sm text-gray-600">Ask questions in your preferred language</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <span className="text-2xl">📞</span>
              <div>
                <h4 className="font-medium">Helpline</h4>
                <p className="text-sm text-gray-600">Call 1800-XXX-XXXX for support</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <span className="text-2xl">💬</span>
              <div>
                <h4 className="font-medium">WhatsApp</h4>
                <p className="text-sm text-gray-600">Get help via WhatsApp chat</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <span className="text-2xl">🏢</span>
              <div>
                <h4 className="font-medium">Visit Office</h4>
                <p className="text-sm text-gray-600">Find nearest government office</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}