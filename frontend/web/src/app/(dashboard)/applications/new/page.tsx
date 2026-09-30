'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Card } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { useToast } from '@/components/ui/Toast';
import { useAuthStore } from '@/store/authStore';
import { api } from '@/lib/api';
import type { Scheme } from '@/types';

interface UploadedDocument {
  id: string;
  type: string;
  name: string;
  url: string;
  uploadedAt: string;
}

export default function NewApplicationPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { addToast } = useToast();
  const { user } = useAuthStore();
  
  const schemeId = searchParams.get('schemeId');
  
  const [scheme, setScheme] = useState<Scheme | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [uploadingDoc, setUploadingDoc] = useState<string | null>(null);
  
  const [formData, setFormData] = useState({
    applicantName: '',
    fatherName: '',
    motherName: '',
    contactNumber: '',
    email: '',
    address: '',
    purpose: '',
    additionalInfo: '',
  });
  
  const [documents, setDocuments] = useState<UploadedDocument[]>([]);
  const [errors, setErrors] = useState<Record<string, string>>({});
  
  useEffect(() => {
    if (!schemeId) {
      addToast('error', 'No scheme selected');
      router.push('/schemes');
      return;
    }
    
    fetchScheme();
    prefillFromProfile();
  }, [schemeId]);
  
  const fetchScheme = async () => {
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
  
  const prefillFromProfile = () => {
    if (user?.profile) {
      setFormData(prev => ({
        ...prev,
        applicantName: user.profile?.name || '',
        contactNumber: user.phoneNumber || '',
      }));
    }
  };
  
  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => {
        const next = { ...prev };
        delete next[field];
        return next;
      });
    }
  };
  
  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>, docType: string) => {
    const file = event.target.files?.[0];
    if (!file) return;
    
    // Validate file size (5MB max)
    if (file.size > 5 * 1024 * 1024) {
      addToast('error', 'File size must be less than 5MB');
      return;
    }
    
    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'application/pdf'];
    if (!allowedTypes.includes(file.type)) {
      addToast('error', 'Only JPG, PNG, and PDF files are allowed');
      return;
    }
    
    setUploadingDoc(docType);
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('documentType', docType);
      formData.append('schemeId', schemeId!);
      
      const response = await api.post<{ document: UploadedDocument }>('/documents/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      setDocuments(prev => [...prev, response.document]);
      addToast('success', `${docType} uploaded successfully`);
    } catch (error) {
      console.error('Error uploading document:', error);
      addToast('error', `Failed to upload ${docType}`);
    } finally {
      setUploadingDoc(null);
    }
  };
  
  const handleDeleteDocument = async (docId: string) => {
    try {
      await api.delete(`/documents/${docId}`);
      setDocuments(prev => prev.filter(doc => doc.id !== docId));
      addToast('success', 'Document deleted');
    } catch (error) {
      addToast('error', 'Failed to delete document');
    }
  };
  
  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};
    
    if (!formData.applicantName.trim()) {
      newErrors.applicantName = 'Name is required';
    }
    
    if (!formData.contactNumber.trim()) {
      newErrors.contactNumber = 'Contact number is required';
    } else if (!/^\d{10}$/.test(formData.contactNumber)) {
      newErrors.contactNumber = 'Must be 10 digits';
    }
    
    if (formData.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Invalid email format';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };
  
  const handleSubmit = async () => {
    if (!validateForm()) {
      addToast('error', 'Please fix all errors before submitting');
      return;
    }
    
    setSubmitting(true);
    
    try {
      // Create application
      const response = await api.post<{ applicationId: string }>('/applications', {
        schemeId,
        applicantDetails: formData,
        documents: documents.map(doc => doc.id),
      });
      
      // Submit application
      await api.post(`/applications/${response.applicationId}/submit`);
      
      addToast('success', 'Application submitted successfully!');
      router.push(`/applications/${response.applicationId}`);
    } catch (error) {
      console.error('Error submitting application:', error);
      addToast('error', 'Failed to submit application');
      setSubmitting(false);
    }
  };
  
  const handleSaveDraft = async () => {
    setSubmitting(true);
    
    try {
      await api.post<{ applicationId: string }>('/applications', {
        schemeId,
        applicantDetails: formData,
        documents: documents.map(doc => doc.id),
        status: 'DRAFT',
      });
      
      addToast('success', 'Draft saved successfully');
      router.push('/dashboard');
    } catch (error) {
      console.error('Error saving draft:', error);
      addToast('error', 'Failed to save draft');
      setSubmitting(false);
    }
  };
  
  if (loading) {
    return (
      <div className="animate-pulse space-y-6">
        <div className="h-8 bg-gray-200 rounded w-1/3"></div>
        <div className="h-64 bg-gray-200 rounded"></div>
      </div>
    );
  }
  
  if (!scheme) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-semibold text-gray-900 mb-2">Scheme not found</h2>
        <Button onClick={() => router.push('/schemes')}>Back to Schemes</Button>
      </div>
    );
  }
  
  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <button
          onClick={() => router.back()}
          className="flex items-center text-gray-600 hover:text-gray-900 mb-4 transition-colors"
        >
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back
        </button>
        
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Apply for Scheme</h1>
        <p className="text-lg text-gray-700">{typeof scheme.name === 'object' ? scheme.name.en || scheme.name[Object.keys(scheme.name)[0]] : scheme.name}</p>
      </div>
      
      {/* Applicant Details */}
      <Card className="mb-6 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Applicant Details</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label="Full Name *"
            value={formData.applicantName}
            onChange={(e) => handleInputChange('applicantName', e.target.value)}
            error={errors.applicantName}
            placeholder="Enter your full name"
          />
          
          <Input
            label="Father's Name"
            value={formData.fatherName}
            onChange={(e) => handleInputChange('fatherName', e.target.value)}
            placeholder="Enter father's name"
          />
          
          <Input
            label="Mother's Name"
            value={formData.motherName}
            onChange={(e) => handleInputChange('motherName', e.target.value)}
            placeholder="Enter mother's name"
          />
          
          <Input
            label="Contact Number *"
            value={formData.contactNumber}
            onChange={(e) => handleInputChange('contactNumber', e.target.value.replace(/\D/g, '').slice(0, 10))}
            error={errors.contactNumber}
            placeholder="10-digit mobile number"
            maxLength={10}
          />
          
          <Input
            label="Email"
            type="email"
            value={formData.email}
            onChange={(e) => handleInputChange('email', e.target.value)}
            error={errors.email}
            placeholder="your.email@example.com"
          />
          
          <div className="md:col-span-2">
            <Input
              label="Address"
              value={formData.address}
              onChange={(e) => handleInputChange('address', e.target.value)}
              placeholder="Enter your complete address"
            />
          </div>
          
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Purpose of Application
            </label>
            <textarea
              value={formData.purpose}
              onChange={(e) => handleInputChange('purpose', e.target.value)}
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-orange-500 focus:ring-2 focus:ring-orange-500 focus:ring-opacity-50 focus:outline-none"
              rows={3}
              placeholder="Briefly explain why you need this scheme"
            />
          </div>
          
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Additional Information
            </label>
            <textarea
              value={formData.additionalInfo}
              onChange={(e) => handleInputChange('additionalInfo', e.target.value)}
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-orange-500 focus:ring-2 focus:ring-orange-500 focus:ring-opacity-50 focus:outline-none"
              rows={3}
              placeholder="Any other relevant information"
            />
          </div>
        </div>
      </Card>
      
      {/* Document Upload */}
      <Card className="mb-6 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Required Documents</h2>
        
        {scheme.requiredDocuments && scheme.requiredDocuments.length > 0 ? (
          <div className="space-y-4">
            {scheme.requiredDocuments.map((docType, index) => {
              const uploaded = documents.find(d => d.type === docType);
              const isUploading = uploadingDoc === docType;
              
              return (
                <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div className="flex-1">
                    <p className="font-medium text-gray-900">{docType}</p>
                    {uploaded && (
                      <p className="text-sm text-green-600">✓ Uploaded: {uploaded.name}</p>
                    )}
                  </div>
                  
                  <div className="flex gap-2">
                    {uploaded ? (
                      <Button
                        variant="danger"
                        size="sm"
                        onClick={() => handleDeleteDocument(uploaded.id)}
                      >
                        Delete
                      </Button>
                    ) : (
                      <label className="cursor-pointer">
                        <span className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed">
                          {isUploading ? 'Uploading...' : 'Upload'}
                        </span>
                        <input
                          type="file"
                          className="hidden"
                          accept=".pdf,.jpg,.jpeg,.png"
                          onChange={(e) => handleFileUpload(e, docType)}
                          disabled={isUploading}
                        />
                      </label>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <p className="text-gray-600">No specific documents required for this scheme.</p>
        )}
        
        <div className="mt-4 p-3 bg-blue-50 rounded-lg">
          <p className="text-sm text-blue-800">
            <strong>Accepted formats:</strong> PDF, JPG, PNG (Max 5MB per file)
          </p>
        </div>
      </Card>
      
      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-4">
        <Button
          variant="outline"
          onClick={handleSaveDraft}
          disabled={submitting}
          className="flex-1"
        >
          Save as Draft
        </Button>
        <Button
          variant="primary"
          onClick={handleSubmit}
          disabled={submitting}
          className="flex-1"
        >
          {submitting ? 'Submitting...' : 'Submit Application'}
        </Button>
      </div>
      
      {/* Disclaimer */}
      <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
        <p className="text-sm text-yellow-800">
          <strong>Note:</strong> Please ensure all information is accurate. False information may lead to rejection of your application.
        </p>
      </div>
    </div>
  );
}
