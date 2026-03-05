'use client'

import { useState } from 'react'
import { RestaurantHeader } from '@/components/RestaurantHeader'
import { RestaurantSelector } from '@/components/RestaurantSelector'
import { OverviewView } from '@/components/OverviewView'
import { SummaryView } from '@/components/SummaryView'
import { mockRestaurants } from '@/data/restaurantData'


export default function Home() {
  const [currentView, setCurrentView] = useState<'overview' | 'summary'>('overview')
  const [selectedRestaurantId, setSelectedRestaurantId] = useState(mockRestaurants[0].id)

  const selectedRestaurant = mockRestaurants.find(r => r.id === selectedRestaurantId) || mockRestaurants[0]

  const handleExportWord = () => {
    alert('Export to Word functionality:\n\nIn a production environment, this would generate a formatted Word document with the complete client overview report.')
  }

  const handleExportPDF = () => {
    alert('Export to PDF functionality:\n\nIn a production environment, this would generate a PDF document with the complete client overview report.')
  }

  const handleRegenerate = () => {
    alert('Regenerate functionality:\n\nIn a production environment, this would re-run the AI analysis and regenerate all insights and recommendations based on the latest data.')
  }

  const handleGenerateOverview = () => {
    alert('Generate Client Overview:\n\nSwitching to the detailed overview report...')
    setCurrentView('overview')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <RestaurantHeader currentView={currentView} onViewChange={setCurrentView} />
      <RestaurantSelector
        restaurants={mockRestaurants}
        selectedId={selectedRestaurantId}
        onSelect={setSelectedRestaurantId}
      />

      {currentView === 'overview' ? (
        <OverviewView
          restaurant={selectedRestaurant}
          onExportWord={handleExportWord}
          onExportPDF={handleExportPDF}
          onRegenerate={handleRegenerate}
        />
      ) : (
        <SummaryView
          restaurant={selectedRestaurant}
          onGenerateOverview={handleGenerateOverview}
        />
      )}
    </div>
  )
}