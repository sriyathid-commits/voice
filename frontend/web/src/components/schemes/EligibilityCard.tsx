'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { EligibilityExplanation } from '@/store/schemeStore'

interface EligibilityCardProps {
  explanation: EligibilityExplanation
  language?: string
}

const STATUS_COLORS = {
  ELIGIBLE: 'bg-green-100 text-green-800 border-green-300',
  LIKELY_ELIGIBLE: 'bg-blue-100 text-blue-800 border-blue-300',
  NEEDS_VERIFICATION: 'bg-yellow-100 text-yellow-800 border-yellow-300',
  NOT_ELIGIBLE: 'bg-red-100 text-red-800 border-red-300'
}

const STATUS_LABELS = {
  ELIGIBLE: '✓ Eligible',
  LIKELY_ELIGIBLE: '~ Likely Eligible',
  NEEDS_VERIFICATION: '⚠ Needs Verification',
  NOT_ELIGIBLE: '✗ Not Eligible'
}

const STATUS_DESCRIPTIONS = {
  ELIGIBLE: 'You meet all known eligibility criteria for this scheme.',
  LIKELY_ELIGIBLE: 'You likely meet the criteria, but some verification is needed.',
  NEEDS_VERIFICATION: 'Please provide missing information to verify your eligibility.',
  NOT_ELIGIBLE: 'Based on current information, you may not be eligible for this scheme.'
}

export default function EligibilityCard({ explanation, language = 'en' }: EligibilityCardProps) {
  const schemeName = explanation.scheme_name[language] || explanation.scheme_name['en']
  const statusColor = STATUS_COLORS[explanation.status]
  const statusLabel = STATUS_LABELS[explanation.status]
  const statusDescription = STATUS_DESCRIPTIONS[explanation.status]

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-xl">Eligibility Analysis</CardTitle>
        <p className="text-sm text-gray-600 mt-1">{schemeName}</p>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Status Badge */}
        <div className="flex items-center justify-between">
          <div>
            <div className={`inline-flex items-center px-4 py-2 rounded-lg border-2 font-semibold ${statusColor}`}>
              {statusLabel}
            </div>
            <p className="text-sm text-gray-600 mt-2">
              {statusDescription}
            </p>
          </div>
          <div className="text-right">
            <div className="text-4xl font-bold text-gray-900">
              {explanation.score}
            </div>
            <div className="text-sm text-gray-500">/ 100</div>
          </div>
        </div>

        {/* Score Bar */}
        <div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div
              className={`h-3 rounded-full transition-all duration-500 ${
                explanation.score >= 80
                  ? 'bg-green-500'
                  : explanation.score >= 60
                  ? 'bg-blue-500'
                  : explanation.score >= 40
                  ? 'bg-yellow-500'
                  : 'bg-red-500'
              }`}
              style={{ width: `${explanation.score}%` }}
            />
          </div>
        </div>

        {/* Matched Conditions */}
        {explanation.match_reasons && explanation.match_reasons.length > 0 && (
          <div>
            <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
              <span className="text-green-500 mr-2">✓</span>
              Matching Criteria ({explanation.match_reasons.length})
            </h4>
            <ul className="space-y-2">
              {explanation.match_reasons.map((reason, index) => (
                <li
                  key={index}
                  className="text-sm text-gray-700 bg-green-50 p-2 rounded flex items-start"
                >
                  <span className="text-green-500 mr-2 mt-0.5">•</span>
                  <span>{reason}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Missing Information */}
        {explanation.missing_information && explanation.missing_information.length > 0 && (
          <div>
            <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
              <span className="text-yellow-500 mr-2">⚠</span>
              Missing Information ({explanation.missing_information.length})
            </h4>
            <ul className="space-y-2">
              {explanation.missing_information.map((info, index) => (
                <li
                  key={index}
                  className="text-sm text-gray-700 bg-yellow-50 p-2 rounded flex items-start"
                >
                  <span className="text-yellow-500 mr-2 mt-0.5">•</span>
                  <span>{info}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Verification Required */}
        {explanation.verification_required && explanation.verification_required.length > 0 && (
          <div>
            <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
              <span className="text-orange-500 mr-2">📋</span>
              Verification Required
            </h4>
            <ul className="space-y-2">
              {explanation.verification_required.map((item, index) => (
                <li
                  key={index}
                  className="text-sm text-gray-700 bg-orange-50 p-2 rounded flex items-start"
                >
                  <span className="text-orange-500 mr-2 mt-0.5">•</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Eligibility Criteria Summary */}
        <div className="border-t pt-4">
          <h4 className="font-semibold text-gray-900 mb-3">
            Scheme Requirements
          </h4>
          <div className="grid grid-cols-2 gap-3 text-sm">
            {explanation.eligibility_criteria_summary.age_range && (
              <div className="bg-gray-50 p-2 rounded">
                <span className="text-gray-600">Age Range: </span>
                <span className="font-medium">
                  {explanation.eligibility_criteria_summary.age_range}
                </span>
              </div>
            )}
            {explanation.eligibility_criteria_summary.income_limit && (
              <div className="bg-gray-50 p-2 rounded">
                <span className="text-gray-600">Income Limit: </span>
                <span className="font-medium">
                  ₹{explanation.eligibility_criteria_summary.income_limit.toLocaleString()}
                </span>
              </div>
            )}
            {explanation.eligibility_criteria_summary.eligible_states && (
              <div className="bg-gray-50 p-2 rounded col-span-2">
                <span className="text-gray-600">States: </span>
                <span className="font-medium">
                  {explanation.eligibility_criteria_summary.eligible_states.join(', ')}
                </span>
              </div>
            )}
            {explanation.eligibility_criteria_summary.eligible_categories && (
              <div className="bg-gray-50 p-2 rounded col-span-2">
                <span className="text-gray-600">Categories: </span>
                <span className="font-medium">
                  {explanation.eligibility_criteria_summary.eligible_categories.join(', ')}
                </span>
              </div>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
