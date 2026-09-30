'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { useToast } from '@/components/ui/Toast';
import { useAuthStore } from '@/store/authStore';
import { api } from '@/lib/api';

export default function LoginPage() {
  const router = useRouter();
  const { addToast } = useToast();
  const { setUser, setToken } = useAuthStore();
  
  const [step, setStep] = useState<'phone' | 'otp'>('phone');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [otp, setOtp] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Validate Indian phone number (10 digits)
  const validatePhoneNumber = (phone: string): boolean => {
    const phoneRegex = /^[6-9]\d{9}$/;
    return phoneRegex.test(phone);
  };
  
  const handleSendOTP = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    if (!validatePhoneNumber(phoneNumber)) {
      setError('Please enter a valid 10-digit Indian phone number');
      return;
    }
    
    setLoading(true);
    
    try {
      const response = await api.post('/register', {
        phoneNumber: `+91${phoneNumber}`,
      });
      
      if ((response as any).success) {
        addToast('success', 'OTP sent successfully! Check your phone.');
        setStep('otp');
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.message || 'Failed to send OTP. Please try again.';
      setError(errorMessage);
      addToast('error', errorMessage);
    } finally {
      setLoading(false);
    }
  };
  
  const handleVerifyOTP = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    if (otp.length !== 6) {
      setError('Please enter a valid 6-digit OTP');
      return;
    }
    
    setLoading(true);
    
    try {
      const response = await api.post('/verify-otp', {
        phoneNumber: `+91${phoneNumber}`,
        otp,
      });
      
      if ((response as any).success) {
        // Store auth data
        setToken((response as any).token);
        setUser((response as any).user);
        
        addToast('success', 'Login successful! Welcome to Voice for Bharat.');
        
        // Redirect to dashboard
        router.push('/dashboard');
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.message || 'Invalid OTP. Please try again.';
      setError(errorMessage);
      addToast('error', errorMessage);
    } finally {
      setLoading(false);
    }
  };
  
  const handleResendOTP = async () => {
    setError('');
    setLoading(true);
    
    try {
      await api.post('/register', {
        phoneNumber: `+91${phoneNumber}`,
      });
      addToast('success', 'OTP resent successfully!');
    } catch (err: any) {
      addToast('error', 'Failed to resend OTP. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-orange-50 via-white to-green-50 p-4">
      <div className="w-full max-w-md">
        {/* Logo/Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-orange-500 to-green-500 rounded-full mb-4">
            <span className="text-3xl">🎤</span>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Voice for Bharat
          </h1>
          <p className="text-gray-600">
            Breaking language barriers with AI
          </p>
        </div>
        
        {/* Login Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8">
          {step === 'phone' ? (
            <form onSubmit={handleSendOTP}>
              <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                Welcome Back
              </h2>
              <p className="text-gray-600 mb-6">
                Enter your phone number to get started
              </p>
              
              <Input
                label="Phone Number"
                type="tel"
                placeholder="9876543210"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value.replace(/\D/g, '').slice(0, 10))}
                error={error}
                leftIcon={
                  <span className="text-sm font-medium">+91</span>
                }
                maxLength={10}
                autoFocus
              />
              
              <Button
                type="submit"
                variant="primary"
                className="w-full mt-6"
                disabled={loading || phoneNumber.length !== 10}
              >
                {loading ? 'Sending OTP...' : 'Send OTP'}
              </Button>
              
              <p className="text-sm text-gray-500 mt-4 text-center">
                We'll send you a 6-digit verification code
              </p>
            </form>
          ) : (
            <form onSubmit={handleVerifyOTP}>
              <button
                type="button"
                onClick={() => {
                  setStep('phone');
                  setOtp('');
                  setError('');
                }}
                className="flex items-center text-gray-600 hover:text-gray-900 mb-4 transition-colors"
              >
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                Back
              </button>
              
              <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                Verify OTP
              </h2>
              <p className="text-gray-600 mb-6">
                Enter the 6-digit code sent to +91 {phoneNumber}
              </p>
              
              <Input
                label="OTP"
                type="text"
                placeholder="123456"
                value={otp}
                onChange={(e) => setOtp(e.target.value.replace(/\D/g, '').slice(0, 6))}
                error={error}
                maxLength={6}
                autoFocus
                className="text-center text-2xl tracking-widest"
              />
              
              <Button
                type="submit"
                variant="primary"
                className="w-full mt-6"
                disabled={loading || otp.length !== 6}
              >
                {loading ? 'Verifying...' : 'Verify & Login'}
              </Button>
              
              <div className="mt-4 text-center">
                <button
                  type="button"
                  onClick={handleResendOTP}
                  disabled={loading}
                  className="text-sm text-orange-600 hover:text-orange-700 font-medium disabled:opacity-50"
                >
                  Didn't receive OTP? Resend
                </button>
              </div>
            </form>
          )}
        </div>
        
        {/* Footer */}
        <p className="text-center text-sm text-gray-500 mt-6">
          By continuing, you agree to our Terms of Service and Privacy Policy
        </p>
      </div>
    </div>
  );
}
