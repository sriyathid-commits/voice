'use client';

import { useState, useEffect } from 'react';
import { Card } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { Dropdown } from '@/components/ui/Dropdown';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { useToast } from '@/components/ui/Toast';
import { useAuthStore } from '@/store/authStore';
import { api } from '@/lib/api';
import { INDIAN_STATES } from '@/lib/constants';

const GENDER_OPTIONS = [
  { value: 'Male', label: 'Male' },
  { value: 'Female', label: 'Female' },
  { value: 'Other', label: 'Other' },
];

const CATEGORY_OPTIONS = [
  { value: 'General', label: 'General' },
  { value: 'OBC', label: 'OBC' },
  { value: 'SC', label: 'SC' },
  { value: 'ST', label: 'ST' },
  { value: 'EWS', label: 'EWS' },
];

const OCCUPATION_OPTIONS = [
  { value: 'Farmer', label: 'Farmer' },
  { value: 'Student', label: 'Student' },
  { value: 'Self-employed', label: 'Self-employed' },
  { value: 'Salaried', label: 'Salaried' },
  { value: 'Business', label: 'Business' },
  { value: 'Daily Wage Worker', label: 'Daily Wage Worker' },
  { value: 'Unemployed', label: 'Unemployed' },
  { value: 'Retired', label: 'Retired' },
  { value: 'Other', label: 'Other' },
];

const EDUCATION_OPTIONS = [
  { value: 'Below 10th', label: 'Below 10th' },
  { value: '10th Pass', label: '10th Pass' },
  { value: '12th Pass', label: '12th Pass' },
  { value: 'Graduate', label: 'Graduate' },
  { value: 'Post-Graduate', label: 'Post-Graduate' },
  { value: 'Doctorate', label: 'Doctorate' },
];

export default function ProfilePage() {
  const { user, updateProfile } = useAuthStore();
  const { addToast } = useToast();
  
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  
  // Form state
  const [formData, setFormData] = useState({
    name: '',
    dateOfBirth: '',
    gender: '',
    state: '',
    district: '',
    pincode: '',
    category: '',
    occupation: '',
    educationLevel: '',
    annualIncome: '',
    aadhaarNumber: '',
    panNumber: '',
    bankAccountNumber: '',
    ifscCode: '',
  });
  
  const [errors, setErrors] = useState<Record<string, string>>({});
  
  // Fetch profile on mount
  useEffect(() => {
    fetchProfile();
  }, []);
  
  const fetchProfile = async () => {
    setLoading(true);
    try {
      const response = await api.get<{ user: any }>('/profile');
      
      if (response.user?.profile) {
        const profile = response.user.profile;
        setFormData({
          name: profile.name || '',
          dateOfBirth: profile.dateOfBirth || '',
          gender: profile.gender || '',
          state: profile.state || '',
          district: profile.district || '',
          pincode: profile.pincode || '',
          category: profile.category || '',
          occupation: profile.occupation || '',
          educationLevel: profile.educationLevel || '',
          annualIncome: profile.annualIncome?.toString() || '',
          aadhaarNumber: profile.aadhaarNumber || '',
          panNumber: profile.panNumber || '',
          bankAccountNumber: profile.bankDetails?.accountNumber || '',
          ifscCode: profile.bankDetails?.ifscCode || '',
        });
      }
    } catch (error) {
      console.error('Error fetching profile:', error);
      addToast('error', 'Failed to load profile');
    } finally {
      setLoading(false);
    }
  };
  
  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};
    
    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }
    
    if (formData.aadhaarNumber && !/^\d{12}$/.test(formData.aadhaarNumber)) {
      newErrors.aadhaarNumber = 'Aadhaar must be 12 digits';
    }
    
    if (formData.panNumber && !/^[A-Z]{5}[0-9]{4}[A-Z]{1}$/.test(formData.panNumber)) {
      newErrors.panNumber = 'Invalid PAN format';
    }
    
    if (formData.pincode && !/^\d{6}$/.test(formData.pincode)) {
      newErrors.pincode = 'Pincode must be 6 digits';
    }
    
    if (formData.annualIncome && isNaN(Number(formData.annualIncome))) {
      newErrors.annualIncome = 'Must be a valid number';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };
  
  const handleSave = async () => {
    if (!validateForm()) {
      addToast('error', 'Please fix the errors before saving');
      return;
    }
    
    setSaving(true);
    try {
      await api.put('/profile', {
        profile: {
          name: formData.name,
          dateOfBirth: formData.dateOfBirth,
          gender: formData.gender,
          state: formData.state,
          district: formData.district,
          pincode: formData.pincode,
          category: formData.category,
          occupation: formData.occupation,
          educationLevel: formData.educationLevel,
          annualIncome: formData.annualIncome ? Number(formData.annualIncome) : undefined,
          aadhaarNumber: formData.aadhaarNumber,
          panNumber: formData.panNumber,
          bankDetails: {
            accountNumber: formData.bankAccountNumber,
            ifscCode: formData.ifscCode,
          },
        },
      });
      
      // Update local state
      updateProfile({
        name: formData.name,
        gender: formData.gender,
        state: formData.state,
        category: formData.category,
        occupation: formData.occupation,
      });
      
      addToast('success', 'Profile updated successfully');
      setIsEditing(false);
      fetchProfile(); // Refresh to get profile strength
    } catch (error) {
      console.error('Error saving profile:', error);
      addToast('error', 'Failed to save profile');
    } finally {
      setSaving(false);
    }
  };
  
  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear error for this field
    if (errors[field]) {
      setErrors(prev => {
        const next = { ...prev };
        delete next[field];
        return next;
      });
    }
  };
  
  const calculateProfileStrength = (): number => {
    const fields = [
      'name', 'dateOfBirth', 'gender', 'state', 'district', 'pincode',
      'category', 'occupation', 'educationLevel', 'annualIncome',
      'aadhaarNumber', 'panNumber', 'bankAccountNumber', 'ifscCode'
    ];
    
    const completedFields = fields.filter(field => {
      const value = formData[field as keyof typeof formData];
      return value && value.trim() !== '';
    }).length;
    
    return Math.round((completedFields / fields.length) * 100);
  };
  
  const profileStrength = calculateProfileStrength();
  
  const getStrengthColor = (strength: number) => {
    if (strength >= 80) return 'bg-green-500';
    if (strength >= 50) return 'bg-yellow-500';
    return 'bg-red-500';
  };
  
  const getStrengthLabel = (strength: number) => {
    if (strength >= 80) return 'Strong';
    if (strength >= 50) return 'Good';
    return 'Weak';
  };
  
  if (loading) {
    return (
      <div className="animate-pulse space-y-6">
        <div className="h-8 bg-gray-200 rounded w-1/3"></div>
        <div className="h-64 bg-gray-200 rounded"></div>
      </div>
    );
  }
  
  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">My Profile</h1>
            <p className="text-gray-600">
              Complete your profile to get better scheme recommendations
            </p>
          </div>
          
          {!isEditing ? (
            <Button onClick={() => setIsEditing(true)}>
              Edit Profile
            </Button>
          ) : (
            <div className="flex gap-2">
              <Button variant="outline" onClick={() => {
                setIsEditing(false);
                fetchProfile(); // Reset form
              }}>
                Cancel
              </Button>
              <Button onClick={handleSave} disabled={saving}>
                {saving ? 'Saving...' : 'Save Changes'}
              </Button>
            </div>
          )}
        </div>
        
        {/* Profile Strength */}
        <Card className="p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">Profile Strength</span>
            <div className="flex items-center gap-2">
              <span className="text-sm font-semibold text-gray-900">{profileStrength}%</span>
              <Badge className={`${getStrengthColor(profileStrength)} text-white`}>
                {getStrengthLabel(profileStrength)}
              </Badge>
            </div>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className={`${getStrengthColor(profileStrength)} h-2 rounded-full transition-all duration-300`}
              style={{ width: `${profileStrength}%` }}
            />
          </div>
          {profileStrength < 80 && (
            <p className="text-xs text-gray-500 mt-2">
              Complete more fields to improve your profile strength and get better scheme matches
            </p>
          )}
        </Card>
      </div>
      
      {/* Personal Information */}
      <Card className="mb-6 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Personal Information</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label="Full Name *"
            value={formData.name}
            onChange={(e) => handleInputChange('name', e.target.value)}
            error={errors.name}
            disabled={!isEditing}
            placeholder="Enter your full name"
          />
          
          <Input
            label="Date of Birth"
            type="date"
            value={formData.dateOfBirth}
            onChange={(e) => handleInputChange('dateOfBirth', e.target.value)}
            disabled={!isEditing}
          />
          
          <Dropdown
            label="Gender"
            options={GENDER_OPTIONS}
            value={formData.gender}
            onChange={(value) => handleInputChange('gender', value)}
            disabled={!isEditing}
            placeholder="Select gender"
          />
          
          <Dropdown
            label="Category"
            options={CATEGORY_OPTIONS}
            value={formData.category}
            onChange={(value) => handleInputChange('category', value)}
            disabled={!isEditing}
            placeholder="Select category"
          />
        </div>
      </Card>
      
      {/* Address Information */}
      <Card className="mb-6 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Address</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Dropdown
            label="State"
            options={INDIAN_STATES.map(state => ({ value: state, label: state }))}
            value={formData.state}
            onChange={(value) => handleInputChange('state', value)}
            disabled={!isEditing}
            placeholder="Select state"
          />
          
          <Input
            label="District"
            value={formData.district}
            onChange={(e) => handleInputChange('district', e.target.value)}
            disabled={!isEditing}
            placeholder="Enter district"
          />
          
          <Input
            label="Pincode"
            value={formData.pincode}
            onChange={(e) => handleInputChange('pincode', e.target.value.replace(/\D/g, '').slice(0, 6))}
            error={errors.pincode}
            disabled={!isEditing}
            placeholder="6-digit pincode"
            maxLength={6}
          />
        </div>
      </Card>
      
      {/* Professional Information */}
      <Card className="mb-6 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Professional Details</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Dropdown
            label="Occupation"
            options={OCCUPATION_OPTIONS}
            value={formData.occupation}
            onChange={(value) => handleInputChange('occupation', value)}
            disabled={!isEditing}
            placeholder="Select occupation"
          />
          
          <Dropdown
            label="Education Level"
            options={EDUCATION_OPTIONS}
            value={formData.educationLevel}
            onChange={(value) => handleInputChange('educationLevel', value)}
            disabled={!isEditing}
            placeholder="Select education"
          />
          
          <Input
            label="Annual Income (₹)"
            value={formData.annualIncome}
            onChange={(e) => handleInputChange('annualIncome', e.target.value.replace(/\D/g, ''))}
            error={errors.annualIncome}
            disabled={!isEditing}
            placeholder="Enter annual income"
          />
        </div>
      </Card>
      
      {/* Identity Documents */}
      <Card className="mb-6 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Identity Documents</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label="Aadhaar Number"
            value={formData.aadhaarNumber}
            onChange={(e) => handleInputChange('aadhaarNumber', e.target.value.replace(/\D/g, '').slice(0, 12))}
            error={errors.aadhaarNumber}
            disabled={!isEditing}
            placeholder="12-digit Aadhaar"
            maxLength={12}
          />
          
          <Input
            label="PAN Number"
            value={formData.panNumber}
            onChange={(e) => handleInputChange('panNumber', e.target.value.toUpperCase().slice(0, 10))}
            error={errors.panNumber}
            disabled={!isEditing}
            placeholder="ABCDE1234F"
            maxLength={10}
          />
        </div>
      </Card>
      
      {/* Bank Details */}
      <Card className="mb-6 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Bank Details</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label="Bank Account Number"
            value={formData.bankAccountNumber}
            onChange={(e) => handleInputChange('bankAccountNumber', e.target.value.replace(/\D/g, ''))}
            disabled={!isEditing}
            placeholder="Enter account number"
          />
          
          <Input
            label="IFSC Code"
            value={formData.ifscCode}
            onChange={(e) => handleInputChange('ifscCode', e.target.value.toUpperCase().slice(0, 11))}
            disabled={!isEditing}
            placeholder="ABCD0123456"
            maxLength={11}
          />
        </div>
      </Card>
      
      {/* Footer */}
      {isEditing && (
        <div className="flex justify-end gap-3">
          <Button variant="outline" onClick={() => {
            setIsEditing(false);
            fetchProfile();
          }}>
            Cancel
          </Button>
          <Button onClick={handleSave} disabled={saving}>
            {saving ? 'Saving...' : 'Save All Changes'}
          </Button>
        </div>
      )}
    </div>
  );
}
