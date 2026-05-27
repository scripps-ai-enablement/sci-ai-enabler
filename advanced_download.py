#!/usr/bin/env python3
import requests
import time
from pathlib import Path
import urllib.parse
from urllib.robotparser import RobotFileParser

# Paper information from our searches
papers = [
    {
        "title": "MolClaw: An Autonomous Agent with Hierarchical Skills for Drug Molecule Evaluation",
        "doi": "10.64898/2026.04.03.716272",
        "filename": "molclaw_2026.04.03.716272v1.pdf",
        "urls": [
            "https://www.biorxiv.org/content/10.64898/2026.04.03.716272v1.full.pdf",
            "https://www.biorxiv.org/content/10.1101/2026.04.03.716272v1.full.pdf"
        ]
    },
    {
        "title": "Using AI to Build AI: AIDO.Builder Enables Autonomous Machine Learning",
        "doi": "10.64898/2026.04.20.719735", 
        "filename": "aido_builder_2026.04.20.719735v2.pdf",
        "urls": [
            "https://www.biorxiv.org/content/10.64898/2026.04.20.719735v2.full.pdf",
            "https://www.biorxiv.org/content/10.64898/2026.04.20.719735v1.full.pdf",
            "https://www.biorxiv.org/content/10.1101/2026.04.20.719735v2.full.pdf"
        ]
    },
    {
        "title": "Human-supervised Agentic AI for Hypothesis Generation (RepurAgent)",
        "doi": "10.64898/2026.04.20.719538",
        "filename": "repuragent_2026.04.20.719538v1.pdf",
        "urls": [
            "https://www.biorxiv.org/content/10.64898/2026.04.20.719538v1.full.pdf",
            "https://www.biorxiv.org/content/10.1101/2026.04.20.719538v1.full.pdf"
        ]
    },
    {
        "title": "Deep learning for microscopy without machine learning expertise",
        "doi": "10.64898/2026.04.03.716415",
        "filename": "llm_microscopy_2026.04.03.716415v1.pdf",
        "urls": [
            "https://www.biorxiv.org/content/10.64898/2026.04.03.716415v1.full.pdf",
            "https://www.biorxiv.org/content/10.1101/2026.04.03.716415v1.full.pdf"
        ]
    }
]

def create_session():
    """Create a session with realistic browser headers and settings"""
    session = requests.Session()
    
    # Set comprehensive browser headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0'
    }
    
    session.headers.update(headers)
    return session

def try_download_with_session(url, filename, title):
    """Attempt download with session management"""
    print(f"\nTrying to download {title}")
    print(f"URL: {url}")
    
    session = create_session()
    
    try:
        # First, try to get the main page to establish session
        base_url = urllib.parse.urljoin(url, '/')
        print(f"  Establishing session with {base_url}")
        
        # Get the abstract page first
        abstract_url = url.replace('.full.pdf', '')
        resp = session.get(abstract_url, timeout=30)
        print(f"  Abstract page status: {resp.status_code}")
        
        time.sleep(2)  # Be polite
        
        # Now try the PDF
        resp = session.get(url, timeout=30, stream=True)
        print(f"  PDF response status: {resp.status_code}")
        print(f"  Content-Type: {resp.headers.get('content-type', 'unknown')}")
        print(f"  Content-Length: {resp.headers.get('content-length', 'unknown')}")
        
        if resp.status_code == 200:
            content_type = resp.headers.get('content-type', '').lower()
            
            # Check if we got a PDF
            if 'pdf' in content_type:
                filepath = Path(f"sources/{filename}")
                with open(filepath, 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                # Verify it's a real PDF
                if filepath.stat().st_size > 50000:  # At least 50KB
                    print(f"  ✓ Successfully downloaded {len(filepath.read_bytes()):,} bytes")
                    return True
                else:
                    print(f"  File too small ({filepath.stat().st_size} bytes), likely not a real PDF")
                    filepath.unlink()  # Remove small file
            else:
                print(f"  Not a PDF: {content_type}")
                # Save first 1000 chars to see what we got
                content = resp.text[:1000]
                print(f"  Content preview: {content[:200]}...")
                
        else:
            print(f"  HTTP error: {resp.status_code}")
            
    except Exception as e:
        print(f"  Exception: {e}")
        
    return False

# Try downloading each paper
Path("sources").mkdir(exist_ok=True)
successful_downloads = []

for paper in papers:
    print(f"\n{'='*60}")
    print(f"Attempting to download: {paper['title']}")
    
    success = False
    for url in paper['urls']:
        if try_download_with_session(url, paper['filename'], paper['title']):
            successful_downloads.append(paper)
            success = True
            break
        time.sleep(3)  # Wait between attempts
    
    if not success:
        print(f"  ✗ Failed to download {paper['title']}")

print(f"\n{'='*60}")
print(f"DOWNLOAD SUMMARY")
print(f"{'='*60}")
print(f"Successfully downloaded {len(successful_downloads)}/{len(papers)} papers:")
for paper in successful_downloads:
    print(f"  ✓ {paper['title']}")

if successful_downloads:
    print(f"\nFiles saved to sources/ directory")
else:
    print(f"\nNo papers were successfully downloaded due to access restrictions.")