'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { ActionPlan as ActionPlanType, ActionPlanStep } from '@/store/schemeStore'

interface ActionPlanProps {
  plan: ActionPlanType
  language?: string
}

const STEP_STATUS_COLORS = {
  COMPLETED: 'bg-green-100 text-green-800 border-green-300',
  REQUIRED: 'bg-blue-100 text-blue-800 border-blue-300',
  OPTIONAL: 'bg-gray-100 text-gray-600 border-gray-300'
}

const STEP_STATUS_ICONS = {
  COMPLETED: '✓',
  REQUIRED: '→',
  OPTIONAL: '○'
}

const DOCUMENT_ICONS: { [key: string]: string } = {
  aadhaar: '🪪',
  pan: '💳',
  income_certificate: '📄',
  caste_certificate: '📋',
  bank_passbook: '🏦',
  land_records: '🏞️',
  photo: '📷',
  domicile_certificate: '🏠',
  age_proof: '📅',
  disability_certificate: '♿',
  ration_card: '🎫'
}

export default function ActionPlan({ plan, language = 'en' }: ActionPlanProps) {
  const schemeName = plan.scheme_name[language] || plan.scheme_name['en']

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-xl">Your Action Plan</CardTitle>
        <p className="text-sm text-gray-600 mt-1">{schemeName}</p>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Eligibility Status */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-semibold text-gray-900">Eligibility Status</h4>
              <p className="text-sm text-gray-600 mt-1">{plan.eligibility_status}</p>
            </div>
            {plan.estimated_time && (
              <div className="text-right">
                <p className="text-xs text-gray-500">Estimated Time</p>
                <p className="font-semibold text-gray-900">{plan.estimated_time}</p>
              </div>
            )}
          </div>
        </div>

        {/* Document Checklist */}
        <div>
          <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
            <span className="mr-2">📁</span>
            Document Checklist
          </h4>
          
          {/* Available Documents */}
          {plan.available_documents.length > 0 && (
            <div className="mb-3">
              <p className="text-xs font-semibold text-green-600 mb-2">
                ✓ Available ({plan.available_documents.length})
              </p>
              <div className="flex flex-wrap gap-2">
                {plan.available_documents.map((doc) => (
                  <div
                    key={doc}
                    className="flex items-center px-3 py-1 bg-green-50 text-green-800 rounded-full text-sm border border-green-200"
                  >
                    <span className="mr-1">{DOCUMENT_ICONS[doc] || '📄'}</span>
                    <span>{doc.replace(/_/g, ' ')}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Missing Documents */}
          {plan.missing_documents.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-orange-600 mb-2">
                ⚠ Required ({plan.missing_documents.length})
              </p>
              <div className="flex flex-wrap gap-2">
                {plan.missing_documents.map((doc) => (
                  <div
                    key={doc}
                    className="flex items-center px-3 py-1 bg-orange-50 text-orange-800 rounded-full text-sm border border-orange-200"
                  >
                    <span className="mr-1">{DOCUMENT_ICONS[doc] || '📄'}</span>
                    <span>{doc.replace(/_/g, ' ')}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* All Documents Available */}
          {plan.missing_documents.length === 0 && plan.available_documents.length > 0 && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-3 text-center">
              <p className="text-green-800 font-semibold">
                ✓ All required documents are available!
              </p>
            </div>
          )}
        </div>

        {/* Next Steps */}
        {plan.next_steps && plan.next_steps.length > 0 && (
          <div>
            <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
              <span className="mr-2">🎯</span>
              Next Steps
            </h4>
            <div className="space-y-3">
              {plan.next_steps.map((step: ActionPlanStep) => (
                <div
                  key={step.step_number}
                  className={`border-2 rounded-lg p-4 ${STEP_STATUS_COLORS[step.status]}`}
                >
                  <div className="flex items-start">
                    <div className="flex-shrink-0 mr-3">
                      <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center font-bold">
                        {step.step_number}
                      </div>
                    </div>
                    <div className="flex-1">
                      <div className="flex items-start justify-between">
                        <h5 className="font-semibold text-gray-900">
                          {step.action}
                        </h5>
                        <span className="text-xs font-semibold ml-2">
                          {STEP_STATUS_ICONS[step.status]} {step.status}
                        </span>
                      </div>
                      <p className="text-sm text-gray-700 mt-1">
                        {step.description}
                      </p>
                      {step.documents_needed && step.documents_needed.length > 0 && (
                        <div className="mt-2 flex flex-wrap gap-1">
                          {step.documents_needed.map((doc) => (
                            <span
                              key={doc}
                              className="inline-flex items-center px-2 py-0.5 bg-white rounded text-xs"
                            >
                              {DOCUMENT_ICONS[doc] || '📄'} {doc.replace(/_/g, ' ')}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Application Method */}
        {plan.application_method && (
          <div className="border-t pt-4">
            <h4 className="font-semibold text-gray-900 mb-2">
              Application Method
            </h4>
            <p className="text-sm text-gray-700 bg-gray-50 p-3 rounded">
              {plan.application_method}
            </p>
            {plan.portal_url && (
              <a
                href={plan.portal_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center mt-2 text-sm text-blue-600 hover:text-blue-800"
              >
                Visit Portal →
              </a>
            )}
          </div>
        )}

        {/* Helpful Notes */}
        {plan.notes && plan.notes.length > 0 && (
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
            <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
              <span className="mr-2">💡</span>
              Helpful Notes
            </h4>
            <ul className="space-y-1">
              {plan.notes.map((note, index) => (
                <li key={index} className="text-sm text-gray-700">
                  • {note}
                </li>
              ))}
            </ul>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
