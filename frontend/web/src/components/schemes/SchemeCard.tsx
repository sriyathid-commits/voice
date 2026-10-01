'use client';

import React from 'react';
import Link from 'next/link';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import type { Scheme } from '@/types';

interface SchemeCardProps {
  scheme: Scheme;
  onSave?: (schemeId: string) => void;
  isSaved?: boolean;
}

export const SchemeCard: React.FC<SchemeCardProps> = ({ scheme, onSave, isSaved = false }) => {
  const getCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      Agriculture: 'bg-green-100 text-green-800',
      Education: 'bg-blue-100 text-blue-800',
      Health: 'bg-red-100 text-red-800',
      Housing: 'bg-purple-100 text-purple-800',
      Employment: 'bg-orange-100 text-orange-800',
      Social: 'bg-pink-100 text-pink-800',
      Financial: 'bg-yellow-100 text-yellow-800',
    };
    return colors[category] || 'bg-gray-100 text-gray-800';
  };
  
  return (
    <Card className="hover:shadow-lg transition-shadow duration-200">
      <div className="p-6">
        {/* Header */}
        <div className="flex items-start justify-between mb-3">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              {scheme.name['en'] || Object.values(scheme.name)[0]}
            </h3>
            <div className="flex flex-wrap gap-2">
              <Badge className={getCategoryColor(scheme.category)}>
                {scheme.category}
              </Badge>
              <Badge variant="info">
                {scheme.state}
              </Badge>
            </div>
          </div>
          
          {onSave && (
            <button
              onClick={() => onSave(scheme.schemeId)}
              className={`ml-4 p-2 rounded-lg transition-colors ${
                isSaved 
                  ? 'text-orange-600 bg-orange-50 hover:bg-orange-100' 
                  : 'text-gray-400 hover:text-orange-600 hover:bg-orange-50'
              }`}
              title={isSaved ? 'Saved' : 'Save scheme'}
            >
              <svg className="w-5 h-5" fill={isSaved ? 'currentColor' : 'none'} stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
              </svg>
            </button>
          )}
        </div>
        
        {/* Description */}
        <p className="text-gray-600 text-sm mb-4 line-clamp-2">
          {scheme.description['en'] || Object.values(scheme.description)[0]}
        </p>
        
        {/* Benefits */}
        {scheme.benefits && (
          <div className="mb-4">
            <p className="text-sm font-medium text-gray-700 mb-1">Benefits:</p>
            <p className="text-sm text-green-600">
              {scheme.benefits['en'] || Object.values(scheme.benefits)[0]}
            </p>
          </div>
        )}
        
        {/* Eligibility Score */}
        {/* {scheme.eligibilityScore !== undefined && (
          <div className="mb-4">
            <div className="flex items-center justify-between mb-1">
              <span className="text-sm font-medium text-gray-700">Eligibility Match</span>
              <span className="text-sm font-semibold text-gray-900">{scheme.eligibilityScore}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className={`${getEligibilityColor(scheme.eligibilityScore)} h-2 rounded-full transition-all duration-300`}
                style={{ width: `${scheme.eligibilityScore}%` }}
              />
            </div>
          </div>
        )} */}
        
        {/* Footer Actions */}
        <div className="flex flex-wrap gap-2">
          <Link href={`/schemes/${scheme.schemeId}`} className="flex-1">
            <Button variant="primary" size="sm" className="w-full">
              View Details
            </Button>
          </Link>
          <Link href={`/schemes/${scheme.schemeId}?action=apply`} className="flex-1">
            <Button variant="secondary" size="sm" className="w-full">
              Apply Now
            </Button>
          </Link>
        </div>
      </div>
    </Card>
  );
};
