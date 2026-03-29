#!/usr/bin/env python3
"""
Flask Backend API for PineappleBytes Middleware

Provides REST API endpoint to access middleware engine functionality.
Supports offline mode using cached data when network is unavailable.
"""

import os
import json
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from middleware_engine import MiddlewareEngine

# Import cache manager for cache management endpoints
from cache_manager import CacheManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
# Enable CORS for all routes and origins (adjust for production)
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/company/<int:company_id>/summary', methods=['GET'])
def get_company_summary(company_id: int):
    """
    API endpoint to process company data and return AI summary + masked profile.
    
    Supports offline mode using cached data when network is unavailable.
    
    Args:
        company_id: The company identifier passed via URL
        
    Returns:
        JSON response with keys:
        - summary: AI-generated summary text from OpenRouter
        - profile: Masked company data dictionary
        - offline_mode: (optional) true if data came from cache
    """
    logger.info(f"Received API request for company_id: {company_id}")
    
    # Check if offline mode is forced via query parameter
    force_offline = request.args.get('offline', 'false').lower() == 'true'
    
    # Read OFFLINE_MODE from environment (default: true for school network compatibility)
    offline_mode_env = os.getenv('OFFLINE_MODE', 'true').lower()
    enable_cache = offline_mode_env != 'false'
    
    # Check for cache-only mode (skip OpenRouter API entirely, use only cached summaries)
    cache_only_mode = os.getenv('CACHE_ONLY_MODE', 'false').lower() == 'true'
    
    try:
        # Initialize middleware engine with cache support
        engine = MiddlewareEngine(enable_cache=enable_cache)
        
        # Process company data (with offline fallback if needed)
        # If cache_only_mode is true, force offline to skip API calls
        summary = engine.process_company(
            company_id=company_id,
            save_token_map=True,
            force_offline=force_offline or cache_only_mode
        )
        
        # Get the masked profile from cache if available (for response consistency)
        # Note: The engine already tokenizes data internally, but we need the profile for response
        # We'll extract it from the cache or re-process minimally
        if engine.cache_manager:
            cached_data = engine.cache_manager.load_from_cache(company_id)
            if cached_data:
                profile = cached_data['profile']
            else:
                # If not cached and we're in offline mode, this shouldn't happen
                # But provide a minimal profile structure
                profile = {
                    'company': {'company_id': company_id, 'company_name': f'Company {company_id}'},
                    'contacts': [], 'agreements': [], 'tickets': []
                }
        else:
            # No cache, need to get profile - but this path shouldn't occur with errors
            profile = {'company': {'company_id': company_id}, 'contacts': [], 'agreements': [], 'tickets': []}
        
        response = {
            'summary': summary,
            'profile': profile
        }
        
        # Indicate if offline mode was used
        if engine.offline_mode_used:
            response['offline_mode'] = True
            response['message'] = 'Using cached data (offline mode) due to network restrictions.'
            logger.info(f"Company {company_id} served from cache (offline mode)")
        else:
            logger.info(f"Successfully processed company_id {company_id} (online mode)")
        
        return jsonify(response), 200
        
    except ValueError as e:
        logger.error(f"Validation error for company_id {company_id}: {e}")
        
        # Check for "company not found" specifically
        if 'not found' in str(e).lower():
            return jsonify({
                'error': 'Company not found',
                'message': f'Company with ID {company_id} does not exist in the database.',
                'suggestion': 'Please check the company ID and try again. Valid company IDs start from 26.'
            }), 404
        
        return jsonify({
            'error': str(e),
            'message': 'Invalid request'
        }), 400
    
    except ConnectionError as e:
        logger.error(f"Database connection failed for company_id {company_id}: {e}")
        return jsonify({
            'error': 'Database connection failed',
            'message': 'Cannot connect to the database. This may be due to network restrictions (e.g., school/work network blocking AWS RDS).',
            'suggestion': 'Try connecting from a different network (home network, mobile hotspot) or check with your network administrator. You can also add ?offline=true to use cached data if available.'
        }), 500
    
    except TimeoutError as e:
        logger.error(f"Request timeout for company_id {company_id}: {e}")
        return jsonify({
            'error': 'Request timeout',
            'message': 'The request timed out. This could be due to slow network connectivity or the AI model taking too long to respond.',
            'suggestion': 'Please try again. If the problem persists, check your internet connection or try a different network. You can also add ?offline=true to use cached data if available.'
        }), 500
    
    except Exception as e:
        logger.error(f"Processing failed for company_id {company_id}: {e}", exc_info=True)
        
        # Check for rate limit errors from OpenRouter
        error_str = str(e)
        if '429' in error_str or 'rate-limited' in error_str or 'rate limit' in error_str.lower():
            # Return 429 status for rate limiting
            return jsonify({
                'error': 'Rate limit exceeded',
                'message': 'OpenRouter API is currently rate-limited. Please try again in a few moments or use your own API key for higher limits.',
                'suggestion': 'This is a known issue with the free tier. Consider adding your own OpenRouter API key in the .env file. You can also add ?offline=true to use cached data if available.'
            }), 429
        
        # Check for connection-related errors
        if any(keyword in error_str.lower() for keyword in ['connection', 'timeout', 'network', 'unreachable', 'refused']):
            return jsonify({
                'error': 'Network or connection error',
                'message': 'Failed to connect to external service (database or AI API). This may be due to network restrictions.',
                'suggestion': 'Check your internet connection. If you are on a school/work network, it may block external APIs. Try a different network. You can also add ?offline=true to use cached data if available.'
            }), 500
        
        return jsonify({
            'error': 'Processing failed',
            'message': 'An unexpected error occurred while processing your request.',
            'suggestion': 'Please try again later. If the problem persists, contact support.'
        }), 500


# ============================================================================
# CACHE MANAGEMENT ENDPOINTS
# ============================================================================

@app.route('/api/cache/status', methods=['GET'])
def get_cache_status():
    """Get cache status - list all cached companies"""
    try:
        cache_manager = CacheManager()
        cached_companies = cache_manager.list_cached_companies()
        
        return jsonify({
            'cache_enabled': True,
            'cached_companies': cached_companies,
            'total_cached': len(cached_companies)
        }), 200
    except Exception as e:
        logger.error(f"Cache status check failed: {e}")
        return jsonify({
            'error': 'Cache status unavailable',
            'message': str(e)
        }), 500


@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    """Clear all cached data"""
    try:
        cache_manager = CacheManager()
        cache_manager.clear_all_cache()
        
        return jsonify({
            'success': True,
            'message': 'Cache cleared successfully'
        }), 200
    except Exception as e:
        logger.error(f"Cache clear failed: {e}")
        return jsonify({
            'error': 'Cache clear failed',
            'message': str(e)
        }), 500


@app.route('/api/cache/preload', methods=['POST'])
def preload_cache():
    """
    Preload cache for all companies or specific company IDs.
    Useful for preparing offline mode before going to restricted networks.
    
    Query params:
        company_ids: Comma-separated list of company IDs (optional, defaults to all)
    """
    try:
        from middleware_engine import MiddlewareEngine
        
        company_ids_param = request.args.get('company_ids', '')
        if company_ids_param:
            company_ids = [int(cid.strip()) for cid in company_ids_param.split(',') if cid.strip()]
        else:
            # Get all company IDs from database
            # For now, use range 26-75 (adjust based on your data)
            company_ids = list(range(26, 76))
        
        cache_manager = CacheManager()
        engine = MiddlewareEngine(enable_cache=True)
        
        results = []
        for company_id in company_ids:
            try:
                logger.info(f"Preloading cache for company {company_id}")
                summary = engine.process_company(company_id, save_token_map=False)
                
                # Get cached info
                cached_data = cache_manager.load_from_cache(company_id)
                results.append({
                    'company_id': company_id,
                    'success': True,
                    'cached_at': cached_data.get('cached_at') if cached_data else None
                })
                logger.info(f"Successfully cached company {company_id}")
            except Exception as e:
                logger.error(f"Failed to cache company {company_id}: {e}")
                results.append({
                    'company_id': company_id,
                    'success': False,
                    'error': str(e)
                })
        
        engine.cleanup()
        
        successful = sum(1 for r in results if r['success'])
        total = len(results)
        
        return jsonify({
            'success': True,
            'message': f'Preloaded cache: {successful}/{total} companies cached successfully',
            'results': results
        }), 200
        
    except Exception as e:
        logger.error(f"Cache preload failed: {e}")
        return jsonify({
            'error': 'Cache preload failed',
            'message': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    # Run Flask development server
    # For production, use a proper WSGI server (e.g., gunicorn, waitress)
    logger.info("Starting Flask backend server...")
    app.run(host='0.0.0.0', port=5000, debug=True)


@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    # Run Flask development server
    # For production, use a proper WSGI server (e.g., gunicorn, waitress)
    logger.info("Starting Flask backend server...")
    app.run(host='0.0.0.0', port=5000, debug=True)