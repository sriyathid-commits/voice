'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Card } from '@/components/ui/Card';

export const dynamic = 'force-dynamic';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { useToast } from '@/components/ui/Toast';
import { api } from '@/lib/api';

interface Application {
  applicationId: string;
  schemeId: string;
  schemeName: string;
  status: string;
  submittedAt: string;
  updatedAt: string;
  applicantDetails: any;
  statusHistory: Array<{
    status: string;
    timestamp: string;
    remarks?: string;
  }>;
}

export default function ApplicationDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { addToast } = useToast();
  
  const applicationId = params.id as string;
  
  const [application, setApplication] = useState<Application | null>(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    if (applicationId) {
      fetchApplication();
    }
  }, [applicationId]);
  
  const fetchApplication = async () => {
    setLoading(true);
    try {
      const response = await api.get<{ application: Application }>(`/applications/${applicationId}`);
      setApplication(response.application);
    } catch (error) {
      console.error('Error fetching application:', error);
      addToast('error', 'Failed to load application');
      router.push('/dashboard');
    } finally {
      setLoading(false);
    }
  };
  
  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      DRAFT: 'bg-gray-100 text-gray-800',
      SUBMITTED: 'bg-blue-100 text-blue-800',
      UNDER_REVIEW: 'bg-yellow-100 text-yellow-800',
      APPROVED: 'bg-green-100 text-green-800',
      REJECTED: 'bg-red-100 text-red-800',
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };
  
  if (loading) {
    return (
      <div className="animate-pulse space-y-6">
        <div className="h-8 bg-gray-200 rounded w-1/3"></div>
        <div className="h-64 bg-gray-200 rounded"></div>
      </div>
    );
  }
  
  if (!application) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-semibold text-gray-900 mb-2">Application not found</h2>
        <Button onClick={() => router.push('/dashboard')}>Back to Dashboard</Button>
      </div>
    );
  }
  
  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <button
          onClick={() => router.push('/dashboard')}
          className="flex items-center text-gray-600 hover:text-gray-900 mb-4 transition-colors"
        >
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to Dashboard
        </button>
        
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Application Details</h1>
            <p className="text-gray-600">Application ID: {application.applicationId}</p>
          </div>
          <Badge className={getStatusColor(application.status)}>
            {application.status.replace('_', ' ')}
          </Badge>
        </div>
      </div>
      
      {/* Scheme Info */}
      <Card className="mb-6 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Scheme Information</h2>
        <div className="space-y-2">
          <div>
            <span className="text-gray-600">Scheme: </span>
            <span className="font-medium">{application.schemeName}</span>
          </div>
          <div>
            <span className="text-gray-600">Submitted: </span>
            <span className="font-medium">
              {new Date(application.submittedAt).toLocaleDateString('en-IN')}
            </span>
          </div>
          <div>
            <span className="text-gray-600">Last Updated: </span>
            <span className="font-medium">
              {new Date(application.updatedAt).toLocaleDateString('en-IN')}
            </span>
          </div>
        </div>
      </Card>
      
      {/* Status Timeline */}
      <Card className="mb-6 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Status Timeline</h2>
        <div className="space-y-4">
          {application.statusHistory?.map((item, index) => (
            <div key={index} className="flex gap-4">
              <div className="flex flex-col items-center">
                <div className="w-3 h-3 bg-orange-500 rounded-full"></div>
                {index < application.statusHistory.length - 1 && (
                  <div className="w-0.5 h-full bg-gray-300 my-1"></div>
                )}
              </div>
              <div className="flex-1 pb-4">
                <div className="flex items-center gap-2 mb-1">
                  <Badge className={getStatusColor(item.status)}>
                    {item.status.replace('_', ' ')}
                  </Badge>
                  <span className="text-sm text-gray-500">
                    {new Date(item.timestamp).toLocaleString('en-IN')}
                  </span>
                </div>
                {item.remarks && (
                  <p className="text-sm text-gray-600 mt-1">{item.remarks}</p>
                )}
              </div>
            </div>
          ))}
        </div>
      </Card>
      
      {/* Applicant Details */}
      <Card className="mb-6 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Applicant Details</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          {Object.entries(application.applicantDetails || {}).map(([key, value]) => (
            <div key={key}>
              <span className="text-gray-600 capitalize">{key.replace(/([A-Z])/g, ' $1')}: </span>
              <span className="font-medium">{value as string}</span>
            </div>
          ))}
        </div>
      </Card>
      
      {/* Actions */}
      {application.status === 'DRAFT' && (
        <div className="flex gap-4">
          <Button
            variant="secondary"
            onClick={() => router.push(`/applications/${applicationId}/edit`)}
            className="flex-1"
          >
            Edit Application
          </Button>
          <Button variant="primary" className="flex-1">
            Submit Application
          </Button>
        </div>
      )}
    </div>
  );
}
