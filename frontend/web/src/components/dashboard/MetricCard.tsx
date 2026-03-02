import React from 'react'
import { Card, CardContent } from '@/components/ui/Card'
import { cn } from '@/lib/utils'

interface MetricCardProps {
  title: string
  count: number
  icon: React.ReactNode
  backgroundColor?: string
  onClick?: () => void
}

export function MetricCard({ 
  title, 
  count, 
  icon, 
  backgroundColor = 'bg-blue-50',
  onClick 
}: MetricCardProps) {
  return (
    <Card 
      className={cn(
        'cursor-pointer transition-transform hover:scale-105',
        backgroundColor,
        onClick && 'hover:shadow-md'
      )}
      onClick={onClick}
    >
      <CardContent className="flex items-center space-x-4">
        <div className="flex-shrink-0">
          {icon}
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium text-gray-600 truncate">
            {title}
          </p>
          <p className="text-2xl font-bold text-gray-900">
            {count.toLocaleString()}
          </p>
        </div>
      </CardContent>
    </Card>
  )
}