#!/usr/bin/env python3
"""
Precache All Company Data for Offline Mode

This script preloads the cache with data for all companies, allowing the
application to work completely offline without consuming OpenRouter tokens.

Usage:
    python precache_all.py                    # Cache all companies (26-75 by default)
    python precache_all.py --start 26 --end 100  # Cache specific range
    python precache_all.py --company_ids 26,27,28  # Cache specific companies

This should be run BEFORE going to a restricted network (like school).
Once cached, the app can run in offline mode without any network access.
"""

import os
import sys
import json
import logging
import argparse
from datetime import datetime
from typing import List, Dict, Any

from middleware_engine import MiddlewareEngine
from cache_manager import CacheManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_cached_companies(cache_dir: str = 'cache') -> List[int]:
    """Get list of already cached company IDs"""
    if not os.path.exists(cache_dir):
        return []
    
    cached = []
    for filename in os.listdir(cache_dir):
        if filename.startswith('company_') and filename.endswith('.json'):
            try:
                company_id = int(filename.replace('company_', '').replace('.json', ''))
                cached.append(company_id)
            except ValueError:
                continue
    
    return sorted(cached)


def get_all_company_ids_from_db(engine: MiddlewareEngine) -> List[int]:
    """
    Query database to get all company IDs.
    This requires database connectivity, so it should be done on an unrestricted network.
    """
    logger.info("Connecting to database to get all company IDs...")
    
    try:
        # Connect to database
        engine.extractor.connect()
        cursor = engine.extractor.connection.cursor()
        
        # Query all company IDs
        query = "SELECT company_id FROM company ORDER BY company_id"
        cursor.execute(query)
        rows = cursor.fetchall()
        
        company_ids = [row[0] for row in rows]
        logger.info(f"Found {len(company_ids)} companies in database")
        
        engine.extractor.disconnect()
        return company_ids
        
    except Exception as e:
        logger.error(f"Failed to get company IDs from database: {e}")
        return []


def precache_company(engine: MiddlewareEngine, cache_manager: CacheManager, company_id: int) -> Dict[str, Any]:
    """
    Process and cache a single company.
    
    Returns:
        Dictionary with result information
    """
    result = {
        'company_id': company_id,
        'success': False,
        'cached_at': None,
        'error': None
    }
    
    try:
        logger.info(f"Processing company {company_id}...")
        
        # Process company (this will extract, tokenize, call OpenRouter, and cache)
        summary = engine.process_company(
            company_id=company_id,
            save_token_map=False,  # Don't save individual token maps for each company
            force_offline=False    # Must use live API to get fresh summary
        )
        
        # Verify cache was created
        cached_data = cache_manager.load_from_cache(company_id)
        if cached_data:
            result['success'] = True
            result['cached_at'] = cached_data.get('cached_at')
            logger.info(f"✓ Company {company_id} cached successfully (summary length: {len(summary)} chars)")
        else:
            result['error'] = "Cache not created"
            logger.error(f"✗ Company {company_id} - cache not created")
            
    except ValueError as e:
        if "not found" in str(e).lower():
            result['error'] = f"Company not found: {e}"
            logger.warning(f"⚠ Company {company_id} not found, skipping")
        else:
            result['error'] = str(e)
            logger.error(f"✗ Company {company_id} - validation error: {e}")
            
    except Exception as e:
        result['error'] = str(e)
        logger.error(f"✗ Company {company_id} failed: {e}")
    
    return result


def main():
    parser = argparse.ArgumentParser(description='Precache company data for offline mode')
    parser.add_argument('--start', type=int, default=26, help='Starting company ID (default: 26)')
    parser.add_argument('--end', type=int, default=75, help='Ending company ID (default: 75)')
    parser.add_argument('--company_ids', type=str, help='Comma-separated list of specific company IDs')
    parser.add_argument('--cache-dir', type=str, default='cache', help='Cache directory (default: cache)')
    parser.add_argument('--force', action='store_true', help='Re-cache companies that are already cached')
    parser.add_argument('--list-only', action='store_true', help='Only list cached companies, do not process')
    parser.add_argument('--use-existing', action='store_true', 
                       help='Use already cached companies, only process missing ones (requires DB connectivity for IDs)')
    
    args = parser.parse_args()
    
    # Initialize cache manager
    cache_manager = CacheManager(cache_dir=args.cache_dir)
    
    # Show current cache status
    already_cached = load_cached_companies(args.cache_dir)
    logger.info(f"Currently cached companies: {already_cached}")
    logger.info(f"Total cached: {len(already_cached)}")
    
    if args.list_only:
        logger.info("List-only mode, exiting.")
        return 0
    
    # Determine which companies to process
    if args.company_ids:
        # Specific companies provided
        company_ids = [int(cid.strip()) for cid in args.company_ids.split(',') if cid.strip()]
    else:
        # Range of companies
        company_ids = list(range(args.start, args.end + 1))
    
    logger.info(f"Target companies: {company_ids}")
    logger.info(f"Total to process: {len(company_ids)}")
    
    # Filter out already cached unless force is used
    if not args.force:
        missing = [cid for cid in company_ids if cid not in already_cached]
        if already_cached and missing:
            logger.info(f"Skipping {len(already_cached)} already cached companies (use --force to re-cache)")
            logger.info(f"Will process {len(missing)} missing companies: {missing}")
        company_ids = missing
    
    if not company_ids:
        logger.info("No companies to process. All requested companies are already cached.")
        return 0
    
    # Check if we have database connectivity to get full company list if needed
    if args.use_existing and already_cached:
        # We want to use existing cache + get fresh for any missing
        try:
            engine = MiddlewareEngine(enable_cache=True)
            db_company_ids = get_all_company_ids_from_db(engine)
            if db_company_ids:
                # Determine which companies actually exist in DB vs just in cache
                existing_ids = set(db_company_ids) & set(already_cached)
                if existing_ids:
                    logger.info(f"Found {len(existing_ids)} companies in both DB and cache:")
                    logger.info(f"These are already cached and exist in DB: {sorted(list(existing_ids))[:10]}...")
        except Exception as e:
            logger.warning(f"Could not verify database companies: {e}")
    
    # Initialize middleware engine (with cache enabled)
    engine = MiddlewareEngine(enable_cache=True)
    
    # Process each company
    results = []
    total = len(company_ids)
    
    for idx, company_id in enumerate(company_ids, 1):
        logger.info(f"[{idx}/{total}] Processing company {company_id}")
        result = precache_company(engine, cache_manager, company_id)
        results.append(result)
        
        # Small delay between requests to avoid rate limiting
        if idx < total:
            import time
            time.sleep(1)
    
    engine.cleanup()
    
    # Summary report
    successful = sum(1 for r in results if r['success'])
    failed = total - successful
    
    print("\n" + "="*60)
    print("PRECACHE COMPLETE")
    print("="*60)
    print(f"Total companies processed: {total}")
    print(f"Successfully cached: {successful}")
    print(f"Failed: {failed}")
    
    if failed > 0:
        print("\nFailed companies:")
        for r in results:
            if not r['success']:
                print(f"  - Company {r['company_id']}: {r['error']}")
    
    # Show updated cache status
    final_cached = load_cached_companies(args.cache_dir)
    print(f"\nTotal cached companies now: {len(final_cached)}")
    print(f"Cache directory: {os.path.abspath(args.cache_dir)}")
    
    if successful > 0:
        print("\n✓ You can now use offline mode by:")
        print("  1. Setting OFFLINE_MODE=true in .env")
        print("  2. Starting the Flask app: python app.py")
        print("  3. Accessing API will use cached data (no network/token usage)")
    
    print("="*60)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())