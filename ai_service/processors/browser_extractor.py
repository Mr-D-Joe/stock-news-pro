import logging
import asyncio

from playwright.async_api import async_playwright, BrowserContext

from ai_service.models.article import Article, ArticleCollection
from ai_service.pipeline.base import PipelineStep, PipelineContext

logger = logging.getLogger(__name__)

class BrowserExtractor(PipelineStep[ArticleCollection, ArticleCollection]):
    """Extract full text from articles using a headless browser."""
    
    name = "browser_extractor"
    
    def __init__(self, max_concurrent: int = 3, timeout_ms: int = 30000):
        self.max_concurrent = max_concurrent
        self.timeout_ms = timeout_ms

    async def _extract_text_from_url(self, url: str, context: BrowserContext | None) -> str:
        if context is None:
            logger.info("Browser context unavailable; skipping extraction for %s", url)
            return ""
        page = await context.new_page()
        try:
            # Go to URL with timeout
            await page.goto(url, timeout=self.timeout_ms, wait_until="domcontentloaded")
            
            # Simple heuristic to extract main text (could be improved with Readability.js)
            # For now, we get all paragraph text that looks substantial
            text = await page.evaluate(r"""() => {
                // Remove nav, footer, ads to clean up
                const selectorsToRemove = ['nav', 'footer', 'header', 'aside', '.ad', '.advertisement', '.social-share'];
                selectorsToRemove.forEach(sel => {
                    document.querySelectorAll(sel).forEach(el => el.remove());
                });
                
                // Get all paragraphs
                const paragraphs = Array.from(document.querySelectorAll('p'));
                return paragraphs
                    .map(p => p.innerText.trim())
                    .filter(t => t.length > 50) // Filter out short snippets
                    .join('\n\n');
            }""")
            
            return text
        except Exception as e:
            logger.warning(f"Failed to extract {url}: {e}")
            return ""
        finally:
            await page.close()

    async def _process_async(self, input_data: ArticleCollection) -> ArticleCollection:
        tasks = []
        # Calculate how many to process - maybe limit to top N to save time?
        # For now, process all defined in collection, but respect concurrency
        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def sem_task(article: Article, context: BrowserContext | None):
            async with semaphore:
                if not article.content or len(article.content) < 200:  # Only if content is missing or short
                    logger.info(f"Scraping {article.link}...")
                    text = await self._extract_text_from_url(article.link, context)
                    if text:
                        article.content = text
                    else:
                        logger.info(f"No text extracted for {article.link}")

        async def run_tasks(context: BrowserContext | None):
            tasks.clear()
            for article in input_data.articles:
                tasks.append(sem_task(article, context))
            await asyncio.gather(*tasks)

        browser = None
        try:
            async with async_playwright() as p:
                # Launch browser (headless by default)
                browser = await p.chromium.launch()
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
                await run_tasks(context)
        except Exception as e:
            logger.warning("Browser launch failed, falling back to no-op extraction: %s", e)
            await run_tasks(None)
        finally:
            if browser is not None:
                await browser.close()

        return input_data

    def process(self, input_data: ArticleCollection, context: PipelineContext) -> ArticleCollection:
        """Synchronous wrapper for async processing."""
        try:
            return asyncio.run(self._process_async(input_data))
        except Exception as e:
            logger.error(f"Browser extraction failed: {e}")
            return input_data
