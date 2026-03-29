<<<<<<< HEAD
﻿'use client'
=======
'use client'
>>>>>>> e46fdbbaf44880c2cb0f4e0fb06bafc7d464da49

import { useState, useEffect } from 'react'
import { RestaurantHeader } from '@/components/RestaurantHeader'
import { OverviewView } from '@/components/OverviewView'
import { SummaryView } from '@/components/SummaryView'
import { Restaurant, SystemTicket, TicketVolumeData, SystemFailure, RiskNote } from '@/data/restaurantData'

function transformApiProfileToRestaurant(apiProfile: any, companyId: number): Restaurant {
  // Extract company info from the profile
  const company = apiProfile.company || {}
  
  // Build properly typed arrays with correct interface types
  const systemTickets: SystemTicket[] = []
  const ticketVolumeHistory: TicketVolumeData[] = []
  const recurringFailures: SystemFailure[] = []
  const operationalRisks: RiskNote[] = []
  
  // Generate a summary from the AI response if available
  const aiSummary = apiProfile.summary || "AI-generated summary would be displayed here based on the complete analysis of client data, system performance, and operational metrics."
  
  const executiveSummary = aiSummary
  const networkInfrastructureNotes = "Network infrastructure analysis pending complete data integration."
  const hardwareDegradation = "Hardware status assessment in progress."
  const staffTrainingGaps = "Staff training evaluation based on system usage patterns."

  const result: Restaurant = {
    id: String(companyId),
    name: company.company_name || `Company ${companyId}`,
    location: company.location || 'Unknown',
    generalManager: 'Unknown',
    regionTier: company.department || 'Unknown',
    reportingPeriod: 'Last 90 Days (Late 2024 - Mar 2025)',
    
    halCertHealth: 95,
    miamiBoardHealth: 92,
    coreSystemsOverall: 90,
    networkInfrastructure: 94,
    
    systemTickets: systemTickets,
    ticketVolumeHistory: ticketVolumeHistory,
    totalTicketsLast90Days: 0,
    
    recurringFailures: recurringFailures,
    
    operationalRisks: operationalRisks,
    
    executiveSummary: executiveSummary,
    networkInfrastructureNotes: networkInfrastructureNotes,
    hardwareDegradation: hardwareDegradation,
    staffTrainingGaps: staffTrainingGaps,
    
    recommendations: {
      technical: [
        'CONNECTIVITY: Add 24/7 backup AP',
        'Deploy Ethernet at 5 POS terminals',
        'Enable Network Segmentation for SuperWiFi 6E',
      ],
      operational: [
        'OPERATIONAL REQUIREMENTS: 3',
        'Implement weekly financial clearing',
        'Staff daily resolution procedures',
      ],
    },
    
    totalTickets: 0,
    criticalIncidents: 0,
    avgResponseTime: 0,
    systemUptime: 99,
    caseResponseVerified: true,
  }
  
  // Ensure all arrays are non-null
  result.recurringFailures = recurringFailures
  result.operationalRisks = operationalRisks
  result.systemTickets = systemTickets
  result.ticketVolumeHistory = ticketVolumeHistory
  
  return result
}

export default function Home() {
  const [currentView, setCurrentView] = useState<'overview' | 'summary'>('overview')
  const [searchInput, setSearchInput] = useState<string>('26')
  const [activeCompanyId, setActiveCompanyId] = useState<string>('26')
  const [restaurant, setRestaurant] = useState<Restaurant | null>(null)
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchRestaurantData = async () => {
<<<<<<< HEAD
=======
      // Guard: Don't fetch if we don't have an ID yet
      if (!activeCompanyId) {
        setIsLoading(false)
        return
      }
      
>>>>>>> e46fdbbaf44880c2cb0f4e0fb06bafc7d464da49
      const companyIdNum = parseInt(activeCompanyId, 10)
      
      if (isNaN(companyIdNum) || companyIdNum <= 0) {
        setError('Invalid company ID')
        setIsLoading(false)
        return
      }
      
      setIsLoading(true)
      setError(null)
      setRestaurant(null)

      try {
<<<<<<< HEAD
        const response = await fetch(`http://127.0.0.1:5000/api/company/${companyIdNum}/summary`)
=======
        // Use environment variable for API URL, fallback to localhost for development
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:5000';
        const response = await fetch(`${apiUrl}/api/company/${companyIdNum}/summary`)
>>>>>>> e46fdbbaf44880c2cb0f4e0fb06bafc7d464da49
        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}))
          if (response.status === 404) {
            const message = errorData.message || 'Company not found'
            const suggestion = errorData.suggestion || 'Please check the company ID and try again.'
            throw new Error(`${message}. ${suggestion}`)
          }
          if (response.status === 429) {
            const message = errorData.message || 'OpenRouter API is rate-limited'
            const suggestion = errorData.suggestion || 'Please try again in a few minutes.'
            throw new Error(`${message}. ${suggestion}`)
          }
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const data = await response.json()
        
        // Transform the API profile into Restaurant format
        const transformedData = transformApiProfileToRestaurant(data.profile, companyIdNum)
        
        // Additional safety check: ensure all arrays are initialized
        if (!transformedData.recurringFailures) transformedData.recurringFailures = []
        if (!transformedData.operationalRisks) transformedData.operationalRisks = []
        if (!transformedData.systemTickets) transformedData.systemTickets = []
        if (!transformedData.ticketVolumeHistory) transformedData.ticketVolumeHistory = []
        
        setRestaurant(transformedData)
      } catch (err) {
        console.error('Fetch error:', err)
        setError(err instanceof Error ? err.message : 'Failed to fetch data')
        setRestaurant(null)
      } finally {
        setIsLoading(false)
      }
    }

    fetchRestaurantData()
  }, [activeCompanyId])

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    const companyIdNum = parseInt(searchInput, 10)
    if (!isNaN(companyIdNum) && companyIdNum > 0) {
      setActiveCompanyId(String(companyIdNum))
    } else {
      setError('Please enter a valid company ID')
    }
  }

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
      
      {/* Company Search Form */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-[1400px] mx-auto">
          <form onSubmit={handleSearch} className="flex items-center gap-3">
            <label htmlFor="company-search" className="text-sm font-medium text-gray-700">Company ID:</label>
            <input
              id="company-search"
              type="number"
              min="1"
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
              className="w-32 px-3 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-900 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              placeholder="Enter ID..."
            />
            <button
              type="submit"
              className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors"
            >
              Search
            </button>
            {isLoading && <span className="text-sm text-gray-500">Loading...</span>}
            {error && <span className="text-sm text-red-600">{error}</span>}
          </form>
        </div>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center py-20">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading company {activeCompanyId} data...</p>
          </div>
        </div>
      ) : restaurant ? (
        <>
          {currentView === 'overview' ? (
            <OverviewView
              restaurant={restaurant}
              onExportWord={handleExportWord}
              onExportPDF={handleExportPDF}
              onRegenerate={handleRegenerate}
            />
          ) : (
            <SummaryView
              restaurant={restaurant}
              onGenerateOverview={handleGenerateOverview}
            />
          )}
        </>
      ) : (
        <div className="flex items-center justify-center py-20">
          <p className="text-gray-600">No data available.</p>
        </div>
      )}
    </div>
  )
<<<<<<< HEAD
}
=======
}
>>>>>>> e46fdbbaf44880c2cb0f4e0fb06bafc7d464da49
