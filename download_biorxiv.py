#!/usr/bin/env python3
import requests
import time
from pathlib import Path

# Paper details based on search results
papers = [
    {
        "title": "MolClaw",
        "doi": "10.64898/2026.04.03.716272",
        "filename": "2026.04.03.716272v1.full.pdf"
    },
    {
        "title": "AIDO.Builder",
        "doi": "10.64898/2026.04.20.719735", 
        "filename": "2026.04.20.719735v2.full.pdf"
    },
    {
        "title": "RepurAgent",
        "doi": "10.64898/2026.04.20.719538",
        "filename": "2026.04.20.719538v1.full.pdf"
    },
    {
        "title": "LLM-Autonomous Microscopy",
        "doi": "10.64898/2026.04.03.716415",
        "filename": "2026.04.03.716415v1.full.pdf"
    }
]

def download_paper(doi, filename, title):
    """Try to download a paper with various strategies"""
    
    # Setup session with headers
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    })
    
    # Try various URL formats
    urls = [
        f"https://www.biorxiv.org/content/{doi}v1.full.pdf",
        f"https://www.biorxiv.org/content/{doi}v2.full.pdf",
        f"https://www.biorxiv.org/content/{doi}.full.pdf",
        f"https://www.biorxiv.org/content/biorxiv/early/2026/{doi.split('.')[-1][:2]}/{doi.split('.')[-1][2:4]}/{doi}.full.pdf"
    ]
    
    # Also try 10.1101 prefix
    doi_alt = doi.replace("10.64898", "10.1101")
    urls.extend([
        f"https://www.biorxiv.org/content/{doi_alt}v1.full.pdf",
        f"https://www.biorxiv.org/content/{doi_alt}v2.full.pdf",
        f"https://www.biorxiv.org/content/{doi_alt}.full.pdf"
    ])
    
    for url in urls:
        print(f"Trying {title}: {url}")
        try:
            response = session.get(url, timeout=30, allow_redirects=True)
            
            # Check if we got a PDF
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '').lower()
                if 'pdf' in content_type or len(response.content) > 50000:  # Likely a real PDF
                    filepath = Path(f"sources/{filename}")
                    filepath.write_bytes(response.content)
                    print(f"✓ Downloaded {title} ({len(response.content):,} bytes)")
                    return True
                elif 'html' in content_type and len(response.content) < 10000:
                    print(f"  Got HTML challenge page ({len(response.content)} bytes)")
                else:
                    print(f"  Unexpected content type: {content_type}")
            else:
                print(f"  HTTP {response.status_code}")
                
        except Exception as e:
            print(f"  Error: {e}")
        
        time.sleep(1)  # Be nice to the server
    
    print(f"✗ Failed to download {title}")
    return False

# Create sources directory
Path("sources").mkdir(exist_ok=True)

# Download papers
success_count = 0
for paper in papers:
    if download_paper(paper["doi"], paper["filename"], paper["title"]):
        success_count += 1
    print()

print(f"Successfully downloaded {success_count}/{len(papers)} papers")