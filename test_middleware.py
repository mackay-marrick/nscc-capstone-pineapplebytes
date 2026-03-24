#!/usr/bin/env python3
"""Quick test script to run the middleware engine and see detailed output"""

import sys
import os
import logging
from middleware_engine import MiddlewareEngine

# Enable detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Test with company 26
company_id = 26

print(f"Testing middleware engine for company_id: {company_id}")
print("="*60)

try:
    engine = MiddlewareEngine()
    summary = engine.process_company(company_id, save_token_map=False)
    
    print("\n" + "="*60)
    print("PROCESSING SUCCESSFUL!")
    print("="*60)
    print(f"Summary length: {len(summary)} characters")
    print("\nFirst 500 characters of summary:")
    print(summary[:500])
    print("...")
    
except Exception as e:
    print("\n" + "="*60)
    print("PROCESSING FAILED!")
    print("="*60)
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    engine.cleanup()