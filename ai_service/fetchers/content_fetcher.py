
import logging
import requests
import io
from bs4 import BeautifulSoup
from typing import Optional
from ai_service.config import Settings

logger = logging.getLogger(__name__)

class ContentFetcher:
    """
    Fetches full text content from URLs for Deep Analysis.
    Handles HTML scrubbing and PDF extraction.
    """
    
    def __init__(self, settings: Settings = None):
        self.settings = settings or Settings()
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })

    def fetch_url(self, url: str) -> Optional[str]:
        """Fetch and extract cleaner text from a URL (HTML or PDF)."""
        if not url:
            return None
            
        try:
            # Handle PDF detection (simple extension check for now)
            if url.lower().endswith('.pdf'):
                return self._fetch_pdf(url)
            
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                logger.warning(f"Failed to fetch {url}: Status {response.status_code}")
                return None
                
            # Check content type header for PDF check
            content_type = response.headers.get('Content-Type', '').lower()
            if 'application/pdf' in content_type:
                return self._extract_pdf_from_bytes(response.content)
            
            return self._extract_html_text(response.text)
            
        except Exception as e:
            logger.warning(f"Fetch error for {url}: {e}")
            return None

    def _extract_html_text(self, html_content: str) -> str:
        """Parse HTML and extract visible text."""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove scripts, styles, metadata
            for element in soup(["script", "style", "header", "footer", "nav", "noscript", "meta"]):
                element.extract()
            
            # Get text
            text = soup.get_text(separator=' ')
            
            # Clean whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return clean_text[:10000] # Limit to 10k chars to save tokens
            
        except Exception as e:
            logger.warning(f"HTML parse error: {e}")
            return ""

    def _fetch_pdf(self, url: str) -> Optional[str]:
        """Fetch PDF and extract text."""
        try:
            response = self.session.get(url, timeout=15)
            if response.status_code == 200:
                return self._extract_pdf_from_bytes(response.content)
        except Exception as e:
            logger.warning(f"PDF fetch error {url}: {e}")
        return None

    def _extract_pdf_from_bytes(self, pdf_bytes: bytes) -> str:
        """Extract text from PDF bytes using pypdf."""
        try:
            from pypdf import PdfReader
            
            f = io.BytesIO(pdf_bytes)
            reader = PdfReader(f)
            text = ""
            for page in reader.pages[:5]: # First 5 pages only
                text += page.extract_text() + "\n"
                
            return text[:10000]
        except Exception as e:
            logger.warning(f"PDF extract error: {e}")
            return ""
