#!/usr/bin/env python3
"""
Flask Backend API for PineappleBytes Middleware

Provides REST API endpoint to access the middleware engine functionality.
"""

import os
import json
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from middleware_engine import MiddlewareEngine, DataTokenizer

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
    
    Args:
        company_id: The company identifier passed via URL
        
    Returns:
        JSON response with keys:
        - summary: AI-generated summary text from OpenRouter
        - profile: Masked company data dictionary
    """
    logger.info(f"Received API request for company_id: {company_id}")
    
    try:
        # Initialize middleware engine (uses .env for DB connection)
        engine = MiddlewareEngine()
        tokenizer = DataTokenizer()
        
        # STEP 1 & 2: Extract data and tokenize PII
        profile = engine.extractor.extract_company_profile(company_id)
        masked_data = tokenizer.tokenize_profile(profile)
        
        # Save token map for reference (optional)
        tokenizer.save_token_map()
        
        # STEP 3: Prepare payload (for API) but we also want to return masked profile
        payload = engine.payload_preparer.prepare_payload(masked_data)
        
        # STEP 4: Generate summary via OpenRouter
        summary = engine.api_client.generate_summary(payload)
        
        # Build response JSON
        response = {
            'summary': summary,
            'profile': masked_data
        }
        
        logger.info(f"Successfully processed company_id {company_id}")
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
    
    except Exception as e:
        logger.error(f"Processing failed for company_id {company_id}: {e}")
        
        # Check for rate limit errors from OpenRouter
        error_str = str(e)
        if '429' in error_str or 'rate-limited' in error_str or 'rate limit' in error_str.lower():
            # Return 429 status for rate limiting
            return jsonify({
                'error': 'Rate limit exceeded',
                'message': 'OpenRouter API is currently rate-limited. Please try again in a few moments or use your own API key for higher limits.',
                'suggestion': 'This is a known issue with the free tier. Consider adding your own OpenRouter API key in the .env file.'
            }), 429
        
        return jsonify({
            'error': str(e),
            'message': 'Failed to process company data'
        }), 500
        
    finally:
        # Cleanup: close database connection
        if 'engine' in locals():
            engine.cleanup()


@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    # Run Flask development server
    # For production, use a proper WSGI server (e.g., gunicorn, waitress)
    logger.info("Starting Flask backend server...")
    app.run(host='0.0.0.0', port=5000, debug=True)