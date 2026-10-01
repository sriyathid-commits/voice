'use client';

import { useState, useEffect } from 'react';
import { Input } from '@/components/ui/Input';
import { Dropdown } from '@/components/ui/Dropdown';
import { Button } from '@/components/ui/Button';
import { SchemeCard } from '@/components/schemes/SchemeCard';
import { useToast } from '@/components/ui/Toast';
import { api } from '@/lib/api';
import type { Scheme } from '@/types';

const CATEGORIES = [
  { value: 'all', label: 'All Categories' },
  { value: 'Agriculture', label: 'Agriculture' },
  { value: 'Education', label: 'Education' },
  { value: 'Health', label: 'Health' },
  { value: 'Housing', label: 'Housing' },
  { value: 'Employment', label: 'Employment' },
  { value: 'Social', label: 'Social Welfare' },
  { value: 'Financial', label: 'Financial Assistance' },
];

export default function SchemesPage() {
  const { addToast } = useToast();
  
  const [schemes, setSchemes] = useState<Scheme[]>([]);
  const [filteredSchemes, setFilteredSchemes] = useState<Scheme[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedState, setSelectedState] = useState('all');
  const [savedSchemeIds, setSavedSchemeIds] = useState<Set<string>>(new Set());
  
  // Fetch schemes
  useEffect(() => {
    fetchSchemes();
  }, []);
  
  const fetchSchemes = async () => {
    setLoading(true);
    try {
      const response = await api.get<{ schemes: Scheme[] }>('/schemes', {
        params: {
          isActive: true,
          limit: 100,
        },
      });
      
      setSchemes(response.schemes || []);
      setFilteredSchemes(response.schemes || []);
    } catch (error) {
      console.error('Error fetching schemes:', error);
      addToast('error', 'Failed to load schemes. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  // Apply filters
  useEffect(() => {
    let filtered = schemes;
    
    // Search filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(
        (scheme) => {
          const name = scheme.name['en'] || Object.values(scheme.name)[0] || '';
          const description = scheme.description['en'] || Object.values(scheme.description)[0] || '';
          return (
            name.toLowerCase().includes(query) ||
            description.toLowerCase().includes(query) ||
            scheme.category.toLowerCase().includes(query)
          );
        }
      );
    }
    
    // Category filter
    if (selectedCategory !== 'all') {
      filtered = filtered.filter((scheme) => scheme.category === selectedCategory);
    }
    
    // State filter
    if (selectedState !== 'all') {
      filtered = filtered.filter((scheme) => scheme.state === selectedState);
    }
    
    setFilteredSchemes(filtered);
  }, [searchQuery, selectedCategory, selectedState, schemes]);
  
  const handleSaveScheme = async (schemeId: string) => {
    try {
      if (savedSchemeIds.has(schemeId)) {
        // Unsave
        await api.delete(`/schemes/${schemeId}/save`);
        setSavedSchemeIds((prev) => {
          const next = new Set(prev);
          next.delete(schemeId);
          return next;
        });
        addToast('success', 'Scheme removed from saved list');
      } else {
        // Save
        await api.post(`/schemes/${schemeId}/save`);
        setSavedSchemeIds((prev) => new Set([...prev, schemeId]));
        addToast('success', 'Scheme saved successfully');
      }
    } catch (error) {
      console.error('Error saving scheme:', error);
      addToast('error', 'Failed to save scheme. Please try again.');
    }
  };
  
  const handleClearFilters = () => {
    setSearchQuery('');
    setSelectedCategory('all');
    setSelectedState('all');
  };
  
  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Browse Schemes</h1>
        <p className="text-gray-600">
          Explore government welfare schemes available across India
        </p>
      </div>
      
      {/* Filters */}
      <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Search */}
          <div className="md:col-span-2">
            <Input
              placeholder="Search schemes..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              leftIcon={
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              }
            />
          </div>
          
          {/* Category Filter */}
          <Dropdown
            options={CATEGORIES}
            value={selectedCategory}
            onChange={setSelectedCategory}
            placeholder="Category"
          />
          
          {/* State Filter */}
          <Dropdown
            options={[
              { value: 'all', label: 'All States' },
              { value: 'Karnataka', label: 'Karnataka' },
              { value: 'Telangana', label: 'Telangana' },
              { value: 'Tamil Nadu', label: 'Tamil Nadu' },
              { value: 'Maharashtra', label: 'Maharashtra' },
              { value: 'All India', label: 'All India' },
            ]}
            value={selectedState}
            onChange={setSelectedState}
            placeholder="State"
          />
        </div>
        
        {/* Active Filters */}
        {(searchQuery || selectedCategory !== 'all' || selectedState !== 'all') && (
          <div className="flex items-center gap-2 mt-4 pt-4 border-t border-gray-200">
            <span className="text-sm text-gray-600">Active filters:</span>
            <div className="flex flex-wrap gap-2">
              {searchQuery && (
                <span className="px-3 py-1 bg-orange-100 text-orange-800 rounded-full text-sm">
                  Search: "{searchQuery}"
                </span>
              )}
              {selectedCategory !== 'all' && (
                <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                  {selectedCategory}
                </span>
              )}
              {selectedState !== 'all' && (
                <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                  {selectedState}
                </span>
              )}
            </div>
            <Button variant="ghost" size="sm" onClick={handleClearFilters}>
              Clear all
            </Button>
          </div>
        )}
      </div>
      
      {/* Results Count */}
      <div className="flex items-center justify-between mb-4">
        <p className="text-sm text-gray-600">
          Showing {filteredSchemes.length} of {schemes.length} schemes
        </p>
      </div>
      
      {/* Loading State */}
      {loading && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="bg-white rounded-lg shadow-sm p-6 animate-pulse">
              <div className="h-6 bg-gray-200 rounded mb-4"></div>
              <div className="h-4 bg-gray-200 rounded mb-2"></div>
              <div className="h-4 bg-gray-200 rounded mb-4"></div>
              <div className="h-10 bg-gray-200 rounded"></div>
            </div>
          ))}
        </div>
      )}
      
      {/* Empty State */}
      {!loading && filteredSchemes.length === 0 && (
        <div className="text-center py-12">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gray-100 rounded-full mb-4">
            <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No schemes found</h3>
          <p className="text-gray-600 mb-4">
            Try adjusting your filters or search query
          </p>
          <Button variant="outline" onClick={handleClearFilters}>
            Clear Filters
          </Button>
        </div>
      )}
      
      {/* Scheme Grid */}
      {!loading && filteredSchemes.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredSchemes.map((scheme) => (
            <SchemeCard
              key={scheme.schemeId}
              scheme={scheme}
              onSave={handleSaveScheme}
              isSaved={savedSchemeIds.has(scheme.schemeId)}
            />
          ))}
        </div>
      )}
    </div>
  );
}
