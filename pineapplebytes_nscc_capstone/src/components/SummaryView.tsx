'use client'

import { Calendar } from 'lucide-react'
import { Restaurant } from '@/data/restaurantData'

interface SummaryViewProps {
  restaurant: Restaurant
  onGenerateOverview: () => void
}

export function SummaryView({ restaurant, onGenerateOverview }: SummaryViewProps) {
  return (
    <div className="max-w-[1400px] mx-auto px-6 py-6">
      <div className="grid grid-cols-[1fr,320px] gap-6">
        {/* Left Column - Main Content */}
        <div className="space-y-6">
          {/* Header with Date Filter */}
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900">SUPPORT SUMMARY / LOGISTICS</h1>
            
            <div className="flex items-center gap-3">
              <div className="text-xs text-gray-600">TIME RANGE ANALYSIS</div>
              <div className="flex items-center gap-2">
                <button className="px-3 py-1.5 text-xs border border-gray-300 rounded bg-white hover:bg-gray-50">
                  <Calendar className="w-3 h-3 inline mr-1" />
                  Last 30 Days
                </button>
                <button className="px-3 py-1.5 text-xs bg-indigo-600 text-white rounded hover:bg-indigo-700">
                  Last 7 Days
                </button>
                <button className="px-3 py-1.5 text-xs border border-gray-300 rounded bg-white hover:bg-gray-50">
                  Last 10 Years
                </button>
              </div>
            </div>
          </div>

          {/* Location Selector */}
          <div className="bg-gray-50 px-4 py-3 rounded-lg">
            <div className="flex items-center gap-2 text-sm">
              <span className="text-gray-600">{restaurant.name}</span>
            </div>
          </div>

          {/* Support Ticket Summary Table */}
          <div className="bg-white rounded-lg border border-gray-200">
            <div className="px-5 py-4 border-b border-gray-200">
              <h2 className="text-base font-semibold text-gray-900 flex items-center gap-2">
                <div className="w-1 h-5 bg-indigo-600 rounded"></div>
                Support Ticket Summary
              </h2>
            </div>
            
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200 bg-gray-50">
                    <th className="text-left py-3 px-5 text-xs font-semibold text-gray-600 uppercase">
                      System
                    </th>
                    <th className="text-center py-3 px-5 text-xs font-semibold text-gray-600 uppercase">
                      Open Tickets
                    </th>
                    <th className="text-center py-3 px-5 text-xs font-semibold text-gray-600 uppercase">
                      Resolved
                    </th>
                    <th className="text-center py-3 px-5 text-xs font-semibold text-gray-600 uppercase">
                      Health Status
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {restaurant.systemTickets.map((ticket, index) => (
                    <tr key={index} className="hover:bg-gray-50">
                      <td className="py-3 px-5 text-sm text-gray-900">{ticket.system}</td>
                      <td className="py-3 px-5 text-sm text-center font-medium text-gray-900">
                        {ticket.openTickets}
                      </td>
                      <td className="py-3 px-5 text-sm text-center text-gray-700">
                        {ticket.resolved}
                      </td>
                      <td className="py-3 px-5 text-center">
                        <span className={`inline-flex px-2.5 py-1 rounded-full text-xs font-medium ${
                          ticket.healthStatus === 'Critical' ? 'bg-red-100 text-red-700' :
                          ticket.healthStatus === 'Warning' ? 'bg-yellow-100 text-yellow-700' :
                          'bg-green-100 text-green-700'
                        }`}>
                          {ticket.healthStatus}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            
            <div className="px-5 py-3 bg-gray-50 border-t border-gray-200">
              <p className="text-xs text-gray-500">
                Showing system performance for {restaurant.name}
              </p>
            </div>
          </div>

          {/* Last Updated */}
          <div className="flex items-center justify-center gap-2 text-xs text-gray-500 py-4">
            <span>Last updated: 15 min ago</span>
          </div>
        </div>

        {/* Right Column - Operational Metrics */}
        <div className="space-y-6">
          <div className="bg-white rounded-lg border border-gray-200 p-5">
            <h2 className="text-base font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <div className="w-1 h-5 bg-indigo-600 rounded"></div>
              Operational Metrics
            </h2>
            
            <div className="space-y-4">
              {/* Total Tickets */}
              <div className="pb-3 border-b border-gray-100">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-600">Total Tickets</span>
                  <div className="flex items-center gap-2">
                    <span className="text-2xl font-bold text-gray-900">{restaurant.totalTickets}</span>
                    <span className="text-xs text-gray-500 bg-gray-100 px-2 py-0.5 rounded">Unchanged</span>
                  </div>
                </div>
              </div>

              {/* Critical Incidents */}
              <div className="pb-3 border-b border-gray-100">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-600">Critical Incidents</span>
                  <div className="flex items-center gap-2">
                    <span className={`text-2xl font-bold ${restaurant.criticalIncidents === 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {restaurant.criticalIncidents}
                    </span>
                    <span className="text-xs text-gray-500 bg-gray-100 px-2 py-0.5 rounded">Unchanged</span>
                  </div>
                </div>
              </div>

              {/* Avg Response Time */}
              <div className="pb-3 border-b border-gray-100">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-600">Avg. Response Time</span>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-gray-900">{restaurant.avgResponseTime} hrs</div>
                  </div>
                </div>
              </div>

              {/* System Uptime */}
              <div className="pb-3 border-b border-gray-100">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-600">System Uptime</span>
                  <div className="flex items-center gap-2">
                    <span className="text-2xl font-bold text-gray-900">{restaurant.systemUptime}%</span>
                    <span className="text-xs text-green-600 bg-green-50 px-2 py-0.5 rounded">Stable</span>
                  </div>
                </div>
              </div>

              {/* Case Response Verified */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-600">Case Response: Verified</span>
                  <div className={`w-3 h-3 rounded-full ${restaurant.caseResponseVerified ? 'bg-green-500' : 'bg-gray-300'}`}></div>
                </div>
                <p className="text-xs text-gray-500 leading-relaxed">
                  All critical systems are responding normally
                </p>
              </div>
            </div>
          </div>

          {/* Generate Client Overview Button */}
          <button
            onClick={onGenerateOverview}
            className="w-full px-5 py-3.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium text-sm"
          >
            Generate Client Overview
          </button>

          {/* Info Text */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-xs text-gray-700 leading-relaxed text-center">
              <span className="font-semibold">Ready to create your executive summary?</span>
              <br /><br />
              Once you click &quot;Generate Client Overview&quot; above, the AI will compile a comprehensive summary report for this location.
            </p>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="flex items-center justify-between text-xs text-gray-500 mt-8 pt-4 border-t border-gray-200">
        <div className="flex items-center gap-4">
          <span>&copy; 2024 Pineapple Bytes</span>
          <a href="#" className="hover:text-gray-700">AI Client-Operational</a>
        </div>
        <div className="flex items-center gap-4">
          <a href="#" className="hover:text-gray-700">Privacy Policy</a>
          <a href="#" className="hover:text-gray-700">Terms of Service</a>
          <a href="#" className="hover:text-gray-700">Support Area</a>
        </div>
      </div>
    </div>
  )
}
