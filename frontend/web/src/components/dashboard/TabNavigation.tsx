import React from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'

const tabs = [
  { id: 'dashboard', label: 'DASHBOARD', icon: '🏠', href: '/dashboard' },
  { id: 'assistant', label: 'ASSISTANT', icon: '🎤', href: '/assistant' },
  { id: 'schemes', label: 'SCHEMES', icon: '📋', href: '/schemes' },
  { id: 'profile', label: 'PROFILE', icon: '👤', href: '/profile' }
]

export function TabNavigation() {
  const pathname = usePathname()

  return (
    <div className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto">
        <nav className="flex">
          {tabs.map((tab) => {
            const isActive = pathname === tab.href || pathname.startsWith(tab.href + '/')
            
            return (
              <Link
                key={tab.id}
                href={tab.href}
                className={cn(
                  'flex-1 flex items-center justify-center px-4 py-4 text-sm font-medium border-b-2 transition-colors',
                  'min-h-[44px]', // Minimum touch target
                  isActive
                    ? 'border-orange-500 text-orange-600 bg-orange-50'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                )}
              >
                <span className="mr-2 text-lg">{tab.icon}</span>
                <span className="hidden sm:inline">{tab.label}</span>
              </Link>
            )
          })}
        </nav>
      </div>
    </div>
  )
}