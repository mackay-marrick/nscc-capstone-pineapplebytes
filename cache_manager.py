#!/usr/bin/env python3
"""
Cache Manager for Offline/Demo Mode

This module handles caching of company profiles and AI summaries to disk,
allowing the application to work without network connectivity when needed.
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class CacheManager:
    """
    Manages persistent caching of company data and AI summaries.
    
    Cache structure:
    cache/
      company_26.json
        {
          "profile": {...},
          "summary": "...",
          "cached_at": "2025-03-24T...",
          "company_name": "..."
        }
    """
    
    def __init__(self, cache_dir: str = 'cache'):
        """
        Initialize cache manager.
        
        Args:
            cache_dir: Directory to store cache files (default: 'cache')
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        logger.info(f"Cache manager initialized with directory: {cache_dir}")
    
    def get_cache_path(self, company_id: int) -> str:
        """Get the file path for a company's cache file"""
        return os.path.join(self.cache_dir, f'company_{company_id}.json')
    
    def save_to_cache(self, company_id: int, profile: Dict[str, Any], summary: str) -> None:
        """
        Save company data and summary to cache.
        
        Args:
            company_id: Company identifier
            profile: Masked company profile dictionary
            summary: AI-generated summary text
        """
        cache_path = self.get_cache_path(company_id)
        
        cache_data = {
            'profile': profile,
            'summary': summary,
            'cached_at': datetime.now().isoformat(),
            'company_name': profile.get('company', {}).get('company_name', 'Unknown')
        }
        
        try:
            with open(cache_path, 'w') as f:
                json.dump(cache_data, f, indent=2)
            logger.info(f"Saved company {company_id} data to cache: {cache_path}")
        except Exception as e:
            logger.error(f"Failed to save cache for company {company_id}: {e}")
            raise
    
    def load_from_cache(self, company_id: int) -> Optional[Dict[str, Any]]:
        """
        Load company data and summary from cache.
        
        Args:
            company_id: Company identifier
            
        Returns:
            Dictionary with 'profile' and 'summary' keys, or None if not cached
        """
        cache_path = self.get_cache_path(company_id)
        
        if not os.path.exists(cache_path):
            logger.info(f"No cache found for company {company_id}")
            return None
        
        try:
            with open(cache_path, 'r') as f:
                cache_data = json.load(f)
            
            cached_at = cache_data.get('cached_at', 'unknown')
            logger.info(f"Loaded company {company_id} from cache (cached: {cached_at})")
            return cache_data
        except Exception as e:
            logger.error(f"Failed to load cache for company {company_id}: {e}")
            return None
    
    def delete_from_cache(self, company_id: int) -> bool:
        """
        Delete a company's cached data.
        
        Args:
            company_id: Company identifier
            
        Returns:
            True if deleted, False if not found
        """
        cache_path = self.get_cache_path(company_id)
        
        if os.path.exists(cache_path):
            try:
                os.remove(cache_path)
                logger.info(f"Deleted cache for company {company_id}")
                return True
            except Exception as e:
                logger.error(f"Failed to delete cache for company {company_id}: {e}")
                return False
        return False
    
    def list_cached_companies(self) -> list:
        """
        Get list of all cached company IDs.
        
        Returns:
            List of company IDs that have cached data
        """
        companies = []
        if not os.path.exists(self.cache_dir):
            return companies
        
        for filename in os.listdir(self.cache_dir):
            if filename.startswith('company_') and filename.endswith('.json'):
                try:
                    company_id = int(filename.replace('company_', '').replace('.json', ''))
                    companies.append(company_id)
                except ValueError:
                    continue
        
        return sorted(companies)
    
    def clear_all_cache(self) -> None:
        """Delete all cached company data"""
        if not os.path.exists(self.cache_dir):
            return
        
        for filename in os.listdir(self.cache_dir):
            if filename.startswith('company_') and filename.endswith('.json'):
                try:
                    os.remove(os.path.join(self.cache_dir, filename))
                except Exception as e:
                    logger.error(f"Failed to delete cache file {filename}: {e}")
        
        logger.info("Cleared all cache data")