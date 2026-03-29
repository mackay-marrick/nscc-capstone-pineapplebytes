#!/usr/bin/env python3
"""
Strip UTF-8 BOM from files and save as clean UTF-8
"""

import sys

def strip_bom(filepath):
    """Read file, strip BOM if present, write back as UTF-8 without BOM"""
    with open(filepath, 'rb') as f:
        content = f.read()
    
    # Check for BOM (EF BB BF in hex)
    if content.startswith(b'\xef\xbb\xbf'):
        print(f"BOM found in {filepath}, stripping it...")
        content = content[3:]
    else:
        print(f"No BOM found in {filepath}")
        return
    
    # Write back as UTF-8 without BOM
    with open(filepath, 'wb') as f:
        f.write(content)
    
    print(f"✓ Saved {filepath} as clean UTF-8")

if __name__ == '__main__':
    files = [
        'pineapplebytes_nscc_capstone/package.json',
        'pineapplebytes_nscc_capstone/tsconfig.json'
    ]
    
    for filepath in files:
        try:
            strip_bom(filepath)
        except Exception as e:
            print(f"✗ Error processing {filepath}: {e}")
    
    print("\nBOM stripping complete!")