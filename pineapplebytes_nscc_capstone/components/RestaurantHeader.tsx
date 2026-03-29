'use client'

import { Settings } from 'lucide-react'

interface RestaurantHeaderProps {
  currentView: 'overview' | 'summary'
  onViewChange: (view: 'overview' | 'summary') => void
}

export function RestaurantHeader({ currentView, onViewChange }: RestaurantHeaderProps) {
  return (
    <div className="bg-white border-b border-gray-200 px-6 py-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-indigo-600 rounded flex items-center justify-center">
            <span className="text-white text-sm font-bold">PB</span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <span className="font-semibold text-gray-900">Pineapple Bytes</span>
            <span className="text-gray-400">-</span>
            <button
              onClick={() => onViewChange('overview')}
              className={`${
                currentView === 'overview' ? 'text-indigo-600 font-medium' : 'text-gray-600'
              } hover:text-indigo-600`}
            >
              Client Overview
            </button>
            <span className="text-gray-400">|</span>
            <button
              onClick={() => onViewChange('summary')}
              className={`${
                currentView === 'summary' ? 'text-indigo-600 font-medium' : 'text-gray-600'
              } hover:text-indigo-600`}
            >
              Support Summary / Logistics
            </button>
          </div>
        </div>
        
        <div className="flex items-center gap-4">
          <button className="text-sm text-gray-600 hover:text-gray-900">Recent</button>
          <button className="flex items-center gap-1 text-sm text-gray-600 hover:text-gray-900">
            <Settings className="w-4 h-4" />
            Settings
          </button>
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-700">Andrew Grant</span>
            <div className="w-8 h-8 bg-gray-900 rounded-full"></div>
          </div>
        </div>
      </div>
    </div>
  )
}