'use client'

import VoiceAssistant from '@/components/voice/VoiceAssistant'
import EligibilityCard from '@/components/schemes/EligibilityCard'
import ActionPlan from '@/components/schemes/ActionPlan'
import { useSchemeStore } from '@/store/schemeStore'

export default function AssistantPage() {
  const { eligibilityExplanation, actionPlan } = useSchemeStore()

  return (
    <div className="space-y-6">
      {/* Voice Assistant */}
      <VoiceAssistant />

      {/* Eligibility Explanation */}
      {eligibilityExplanation && (
        <EligibilityCard explanation={eligibilityExplanation} />
      )}

      {/* Action Plan */}
      {actionPlan && (
        <ActionPlan plan={actionPlan} />
      )}
    </div>
  )
}
