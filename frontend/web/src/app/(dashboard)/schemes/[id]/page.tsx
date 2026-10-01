'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter, useSearchParams } from 'next/navigation';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { Card } from '@/components/ui/Card';
// import { EligibilityCard } from '@/components/schemes/EligibilityCard';
// import { ActionPlan } from '@/components/schemes/ActionPlan';
import { useToast } from '@/components/ui/Toast';
import { api } from '@/lib/api';
import type { Scheme } from '@/types';
import type { EligibilityExplanation, ActionPlanStep } from '@/store/schemeStore';

export const dynamic = 'force-dynamic';

export default function SchemeDetailPage() {
  const params = useParams();
  const router = useRouter();
  const searchParams = useSearchParams();
  const { addToast } = useToast();
  
  const schemeId = params.id as string;
  const actionParam = searchParams.get('action');
  
  const [scheme, setScheme] = useState<Scheme | null>(null);
  const [loading, setLoading] = useState(true);
  const [eligibility, setEligibility] = useState<EligibilityExplanation | null>(null);
  const [actionPlan, setActionPlan] = useState<ActionPlanStep[] | null>(null);
  const [checkingEligibility, setCheckingEligibility] = useState(false);
  const [generatingPlan, setGeneratingPlan] = useState(false);
  const [isSaved, setIsSaved] = useState(false);
  
  useEffect(() => {
    if (schemeId) {
      fetchSchemeDetail();
    }
  }, [schemeId]);
  
  // Auto-check eligibility if action=apply in URL
  useEffect(() => {
    if (actionParam === 'apply' && scheme && !eligibility) {
      handleCheckEligibility();
    }
  }, [actionParam, scheme]);
  
  const fetchSchemeDetail = async () => {
    setLoading(true);
    try {
      const response = await api.get<{ scheme: Scheme }>(`/schemes/${schemeId}`);
      setScheme(response.scheme);
    } catch (error) {
      console.error('Error fetching scheme:', error);
      addToast('error', 'Failed to load scheme details');
      router.push('/schemes');
    } finally {
      setLoading(false);
    }
  };
  
  const handleCheckEligibility = async () => {
    setCheckingEligibility(true);
    try {
      const response = await api.post<{ eligibility: EligibilityExplanation }>(
        `/schemes/${schemeId}/eligibility-explanation`
      );
      setEligibility(response.eligibility);
      addToast('success', 'Eligibility checked successfully');
    } catch (error) {
      console.error('Error checking eligibility:', error);
      addToast('error', 'Failed to check eligibility');
    } finally {
      setCheckingEligibility(false);
    }
  };
  
  const handleGenerateActionPlan = async () => {
    setGeneratingPlan(true);
    try {
      const response = await api.post<{ actionPlan: ActionPlanStep[] }>(
        `/schemes/${schemeId}/action-plan`
      );
      setActionPlan(response.actionPlan);
      addToast('success', 'Action plan generated');
    } catch (error) {
      console.error('Error generating action plan:', error);
      addToast('error', 'Failed to generate action plan');
    } finally {
      setGeneratingPlan(false);
    }
  };
  
  const handleSaveScheme = async () => {
    try {
      if (isSaved) {
        await api.delete(`/schemes/${schemeId}/save`);
        setIsSaved(false);
        addToast('success', 'Scheme removed from saved list');
      } else {
        await api.post(`/schemes/${schemeId}/save`);
        setIsSaved(true);
        addToast('success', 'Scheme saved successfully');
      }
    } catch (error) {
      addToast('error', 'Failed to save scheme');
    }
  };
  
  const handleApplyNow = () => {
    router.push(`/applications/new?schemeId=${schemeId}`);
  };
  
  if (loading) {
    return (
      <div className="animate-pulse">
        <div className="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
        <div className="h-4 bg-gray-200 rounded w-2/3 mb-8"></div>
        <div className="h-64 bg-gray-200 rounded"></div>
      </div>
    );
  }
  
  if (!scheme) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-semibold text-gray-900 mb-2">Scheme not found</h2>
        <p className="text-gray-600 mb-4">The scheme you're looking for doesn't exist</p>
        <Button onClick={() => router.push('/schemes')}>Back to Schemes</Button>
      </div>
    );
  }
  
  return (
    <div className="max-w-4xl mx-auto">
      {/* Back Button */}
      <button
        onClick={() => router.back()}
        className="flex items-center text-gray-600 hover:text-gray-900 mb-4 transition-colors"
      >
        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
        </svg>
        Back to Schemes
      </button>
      
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">{scheme.name['en'] || Object.values(scheme.name)[0]}</h1>
            <div className="flex flex-wrap gap-2">
              <Badge>{scheme.category}</Badge>
              <Badge variant="info">{scheme.state}</Badge>
              {scheme.isActive && <Badge variant="success">Active</Badge>}
            </div>
          </div>
          
          <button
            onClick={handleSaveScheme}
            className={`p-3 rounded-lg transition-colors ${
              isSaved 
                ? 'text-orange-600 bg-orange-50 hover:bg-orange-100' 
                : 'text-gray-400 hover:text-orange-600 hover:bg-orange-50'
            }`}
          >
            <svg className="w-6 h-6" fill={isSaved ? 'currentColor' : 'none'} stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
            </svg>
          </button>
        </div>
        
        <p className="text-lg text-gray-700">{scheme.description['en'] || Object.values(scheme.description)[0]}</p>
      </div>
      
      {/* Scheme Details */}
      <Card className="mb-6 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Scheme Details</h2>
        
        <div className="space-y-4">
          {scheme.benefits && (
            <div>
              <h3 className="font-medium text-gray-900 mb-1">Benefits</h3>
              <p className="text-gray-700">{scheme.benefits['en'] || Object.values(scheme.benefits)[0]}</p>
            </div>
          )}
          
          {scheme.eligibilityCriteria && (
            <div>
              <h3 className="font-medium text-gray-900 mb-2">Eligibility Criteria</h3>
              <ul className="list-disc list-inside space-y-1 text-gray-700">
                {(scheme.eligibilityCriteria.minAge || scheme.eligibilityCriteria.maxAge) && (
                  <li>Age: {scheme.eligibilityCriteria.minAge || 0} - {scheme.eligibilityCriteria.maxAge || '∞'} years</li>
                )}
                {scheme.eligibilityCriteria.gender && scheme.eligibilityCriteria.gender.length > 0 && (
                  <li>Gender: {scheme.eligibilityCriteria.gender.join(', ')}</li>
                )}
                {scheme.eligibilityCriteria.incomeLimit && (
                  <li>Income: Up to ₹{scheme.eligibilityCriteria.incomeLimit.toLocaleString()}</li>
                )}
                {scheme.eligibilityCriteria.categories && scheme.eligibilityCriteria.categories.length > 0 && (
                  <li>Categories: {scheme.eligibilityCriteria.categories.join(', ')}</li>
                )}
              </ul>
            </div>
          )}
          
          {scheme.requiredDocuments && scheme.requiredDocuments.length > 0 && (
            <div>
              <h3 className="font-medium text-gray-900 mb-2">Required Documents</h3>
              <ul className="list-disc list-inside space-y-1 text-gray-700">
                {scheme.requiredDocuments.map((doc, index) => (
                  <li key={index}>{doc}</li>
                ))}
              </ul>
            </div>
          )}
          
          {scheme.portalUrl && (
            <div>
              <h3 className="font-medium text-gray-900 mb-1">Official Portal</h3>
              <a 
                href={scheme.portalUrl} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-orange-600 hover:text-orange-700 underline"
              >
                {scheme.portalUrl}
              </a>
            </div>
          )}
        </div>
      </Card>
      
      {/* Action Buttons */}
      {!eligibility && (
        <div className="flex gap-4 mb-6">
          <Button
            variant="primary"
            onClick={handleCheckEligibility}
            disabled={checkingEligibility}
            className="flex-1"
          >
            {checkingEligibility ? 'Checking...' : 'Check Eligibility'}
          </Button>
          <Button variant="secondary" onClick={handleApplyNow} className="flex-1">
            Apply Now
          </Button>
        </div>
      )}
      
      {/* Eligibility Results */}
      {eligibility && (
        <div className="mb-6">
          {/* <EligibilityCard eligibility={eligibility} /> */}
          <Card>
            <h3 className="text-lg font-semibold mb-2">Eligibility Results</h3>
            <p>Status: {eligibility.status}</p>
            <p>Score: {eligibility.score}</p>
          </Card>
        </div>
      )}
      
      {/* Generate Action Plan */}
      {eligibility && !actionPlan && (
        <div className="mb-6">
          <Button
            variant="primary"
            onClick={handleGenerateActionPlan}
            disabled={generatingPlan}
            className="w-full"
          >
            {generatingPlan ? 'Generating Plan...' : 'Get Step-by-Step Action Plan'}
          </Button>
        </div>
      )}
      
      {/* Action Plan */}
      {actionPlan && (
        <div className="mb-6">
          {/* <ActionPlan steps={actionPlan} scheme={scheme} /> */}
          <Card>
            <h3 className="text-lg font-semibold mb-2">Action Plan</h3>
            <p>{actionPlan.length} steps available</p>
          </Card>
        </div>
      )}
    </div>
  );
}
