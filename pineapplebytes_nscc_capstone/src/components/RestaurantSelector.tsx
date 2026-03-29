'use client'

import { ChevronDown } from 'lucide-react'
import { Restaurant } from '@/data/restaurantData'

interface RestaurantSelectorProps {
  restaurants: Restaurant[]
  selectedId: string
  onSelect: (id: string) => void
}

export function RestaurantSelector({ restaurants, selectedId, onSelect }: RestaurantSelectorProps) {
  const selectedRestaurant = restaurants.find(r => r.id === selectedId)

  return (
    <div className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="max-w-[1400px] mx-auto">
        <div className="flex items-center gap-3">
          <label className="text-sm font-medium text-gray-700">Location:</label>
          <div className="relative">
            <select
              value={selectedId}
              onChange={(e) => onSelect(e.target.value)}
              className="appearance-none px-4 py-2 pr-10 border border-gray-300 rounded-lg bg-white text-sm font-medium text-gray-900 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent cursor-pointer min-w-[300px]"
            >
              {restaurants.map((restaurant) => (
                <option key={restaurant.id} value={restaurant.id}>
                  {restaurant.name}
                </option>
              ))}
            </select>
            <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" />
          </div>
          {selectedRestaurant && (
            <span className="text-sm text-gray-500">
              ({selectedRestaurant.location})
            </span>
          )}
        </div>
      </div>
    </div>
  )
}
