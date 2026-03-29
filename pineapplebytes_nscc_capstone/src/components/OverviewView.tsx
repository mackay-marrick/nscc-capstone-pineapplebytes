<<<<<<< HEAD
﻿'use client'
=======
'use client'
>>>>>>> e46fdbbaf44880c2cb0f4e0fb06bafc7d464da49

import { Download, FileText, RotateCw, MapPin, User, Tag } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { Restaurant } from '@/data/restaurantData'

interface OverviewViewProps {
  restaurant: Restaurant
  onExportWord: () => void
  onExportPDF: () => void
  onRegenerate: () => void
}

export function OverviewView({ restaurant, onExportWord, onExportPDF, onRegenerate }: OverviewViewProps) {
  return (
    <div className="max-w-[1400px] mx-auto px-6 py-6 space-y-6">
      {/* Title and Actions */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-1">{restaurant.name}</h1>
          <p className="text-sm text-gray-600">
            <span className="font-medium">Reporting Period:</span> {restaurant.reportingPeriod}
          </p>
        </div>
        
        <div className="flex items-center gap-3">
          <button
            onClick={onExportWord}
            className="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 flex items-center gap-2"
          >
            <Download className="w-4 h-4" />
            Export Word
          </button>
          <button
            onClick={onExportPDF}
            className="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 flex items-center gap-2"
          >
            <FileText className="w-4 h-4" />
            Export PDF
          </button>
          <button
            onClick={onRegenerate}
            className="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 flex items-center gap-2"
          >
            <RotateCw className="w-4 h-4" />
            Regenerate
          </button>
        </div>
      </div>

      {/* Two Column Layout */}
      <div className="grid grid-cols-2 gap-6">
        {/* Left Column */}
        <div className="space-y-6">
          {/* Restaurant Profile */}
          <div className="bg-white rounded-lg border border-gray-200 p-5">
            <h2 className="text-base font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <div className="w-1 h-5 bg-indigo-600 rounded"></div>
              Restaurant Profile
            </h2>
            <div className="space-y-3">
              <div className="flex items-center gap-2 text-sm">
                <MapPin className="w-4 h-4 text-gray-400" />
                <span className="text-gray-600">Location ID:</span>
                <span className="font-medium text-gray-900">{restaurant.location}</span>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <User className="w-4 h-4 text-gray-400" />
                <span className="text-gray-600">General Manager:</span>
                <span className="font-medium text-gray-900">{restaurant.generalManager}</span>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <Tag className="w-4 h-4 text-gray-400" />
                <span className="text-gray-600">Region / Tier:</span>
                <span className="font-medium text-gray-900">{restaurant.regionTier}</span>
              </div>
            </div>
          </div>

          {/* Support Ticket Volume Trends */}
          <div className="bg-white rounded-lg border border-gray-200 p-5">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-base font-semibold text-gray-900 flex items-center gap-2">
                <div className="w-1 h-5 bg-indigo-600 rounded"></div>
                Support Ticket Volume Trends
              </h2>
              <div className="text-right">
                <div className="text-2xl font-bold text-indigo-600">{restaurant.totalTicketsLast90Days}</div>
                <div className="text-xs text-gray-500">Total (Last 90 Days)</div>
              </div>
            </div>
            <div className="text-xs text-gray-500 mb-3">Daily breakdown of reported technical incidents</div>
            
            <ResponsiveContainer width="100%" height={200}>
              <LineChart data={restaurant.ticketVolumeHistory} key={restaurant.id}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis 
                  dataKey="month" 
                  tick={{ fill: '#6b7280', fontSize: 11 }}
                  stroke="#e5e7eb"
                />
                <YAxis 
                  tick={{ fill: '#6b7280', fontSize: 11 }}
                  stroke="#e5e7eb"
                />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#fff', 
                    border: '1px solid #e5e7eb',
                    borderRadius: '6px',
                    fontSize: '12px'
                  }}
                />
                <Line 
                  type="monotone" 
                  dataKey="count" 
                  stroke="#6366f1" 
                  strokeWidth={2}
                  dot={{ fill: '#6366f1', r: 3 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Recurring System Failures */}
          <div className="bg-white rounded-lg border border-gray-200 p-5">
            <h2 className="text-base font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <div className="w-1 h-5 bg-indigo-600 rounded"></div>
              Recurring System Failures
            </h2>
            
            <div className="space-y-3">
              {restaurant.recurringFailures.map((failure, index) => (
                <div key={index} className="flex items-start justify-between py-2 border-b border-gray-100 last:border-0">
                  <div className="flex-1">
                    <div className="text-sm font-medium text-gray-900">{failure.system}</div>
                    <div className="text-xs text-gray-600 mt-0.5">{failure.issue}</div>
                  </div>
                  <span className={`px-2 py-1 rounded text-xs font-medium ${
                    failure.impact === 'High' ? 'bg-red-100 text-red-700' :
                    failure.impact === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                    'bg-gray-100 text-gray-700'
                  }`}>
                    {failure.impact}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column */}
        <div className="space-y-6">
          {/* Core Systems Health */}
          <div className="bg-white rounded-lg border border-gray-200 p-5">
            <h2 className="text-base font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <div className="w-1 h-5 bg-indigo-600 rounded"></div>
              Core Systems Health
            </h2>
            <div className="text-xs text-gray-500 mb-4">Last-90-day availability and uptime metrics</div>
            
            <div className="space-y-4">
              <div>
                <div className="flex items-center justify-between text-sm mb-2">
                  <span className="text-gray-700">HAL-CERT-M</span>
                  <span className="font-semibold text-gray-900">{restaurant.halCertHealth}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-green-500 h-2 rounded-full" 
                    style={{ width: `${restaurant.halCertHealth}%` }}
                  ></div>
                </div>
              </div>
              
              <div>
                <div className="flex items-center justify-between text-sm mb-2">
                  <span className="text-gray-700">Miami Sterling</span>
                  <span className="font-semibold text-gray-900">{restaurant.miamiBoardHealth}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-green-500 h-2 rounded-full" 
                    style={{ width: `${restaurant.miamiBoardHealth}%` }}
                  ></div>
                </div>
              </div>
              
              <div className="pt-3 border-t border-gray-100">
                <div className="flex items-center justify-between text-sm mb-2">
                  <span className="text-gray-700 font-medium">Core Systems Overall</span>
                  <span className="font-bold text-gray-900">{restaurant.coreSystemsOverall}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2.5">
                  <div 
                    className="bg-indigo-600 h-2.5 rounded-full" 
                    style={{ width: `${restaurant.coreSystemsOverall}%` }}
                  ></div>
                </div>
              </div>
              
              <div>
                <div className="flex items-center justify-between text-sm mb-2">
                  <span className="text-gray-700 font-medium">Network Infrastructure</span>
                  <span className="font-bold text-gray-900">{restaurant.networkInfrastructure}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2.5">
                  <div 
                    className="bg-indigo-600 h-2.5 rounded-full" 
                    style={{ width: `${restaurant.networkInfrastructure}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>

          {/* Operational Risk Notes */}
          <div className="bg-white rounded-lg border border-gray-200 p-5">
            <h2 className="text-base font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <div className="w-1 h-5 bg-indigo-600 rounded"></div>
              Operational Risk Notes
            </h2>
            
            <div className="space-y-4">
              {restaurant.operationalRisks.map((risk, index) => (
                <div key={index} className="border-l-4 pl-3" style={{
                  borderLeftColor: risk.severity === 'High' ? '#ef4444' : risk.severity === 'Medium' ? '#f59e0b' : '#6b7280'
                }}>
                  <div className="flex items-center gap-2 mb-1">
                    <div className="text-sm font-semibold text-gray-900">{risk.title}</div>
                  </div>
                  <p className="text-xs text-gray-600 leading-relaxed">{risk.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* AI-Generated Strategic Overview */}
      <div className="bg-white rounded-lg border border-gray-200 p-5">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-base font-semibold text-gray-900 flex items-center gap-2">
            <div className="w-1 h-5 bg-indigo-600 rounded"></div>
            AI-Generated Strategic Overview
          </h2>
          <a href="#" className="text-xs text-indigo-600 hover:text-indigo-700">All Report | Full</a>
        </div>
        
        <div className="space-y-4 text-sm text-gray-700 leading-relaxed">
          <div>
            <span className="font-semibold text-gray-900">Executive Summary:</span> {restaurant.executiveSummary}
          </div>
          
          <div>
            <span className="font-semibold text-gray-900">Network Infrastructure:</span> {restaurant.networkInfrastructureNotes}
          </div>
          
          <div>
            <span className="font-semibold text-gray-900">Hardware Degradation:</span> {restaurant.hardwareDegradation}
          </div>
          
          <div>
            <span className="font-semibold text-gray-900">Staff Training Gaps:</span> {restaurant.staffTrainingGaps}
          </div>
        </div>
      </div>

      {/* Recommendations (5 Next Steps) */}
      <div className="bg-white rounded-lg border border-gray-200 p-5">
        <h2 className="text-base font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <div className="w-1 h-5 bg-indigo-600 rounded"></div>
          Recommendations (5 Next Steps)
        </h2>
        
        <div className="grid grid-cols-2 gap-6">
          <div>
            <h3 className="text-sm font-semibold text-gray-900 mb-3">TECHNICAL ACTION ITEMS</h3>
            <div className="space-y-2">
              {restaurant.recommendations.technical.map((rec, index) => (
                <div key={index} className="flex gap-2">
                  <input type="checkbox" className="mt-0.5" />
                  <span className="text-sm text-gray-700">{rec}</span>
                </div>
              ))}
            </div>
          </div>
          
          <div>
            <h3 className="text-sm font-semibold text-gray-900 mb-3">OPERATIONAL REQUIREMENTS</h3>
            <div className="space-y-2">
              {restaurant.recommendations.operational.map((rec, index) => (
                <div key={index} className="flex gap-2">
                  <input type="checkbox" className="mt-0.5" />
                  <span className="text-sm text-gray-700">{rec}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="text-xs text-gray-500 text-center py-4 border-t border-gray-200">
        &copy; 2024 Pineapple Bytes - AI Client-Operational - Privacy Policy - Terms of Service - Support Area
      </div>
    </div>
  )
}
