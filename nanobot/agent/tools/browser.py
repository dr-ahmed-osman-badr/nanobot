"""Playwright-based browser automation tool."""

import asyncio
import base64
from typing import Any

from loguru import logger
from nanobot.agent.tools.base import Tool

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


class BrowserTool(Tool):
    """Tool to browse websites using a real browser (Playwright)."""
    
    def __init__(self, headless: bool = True, timeout: int = 30000):
        self.headless = headless
        self.timeout = timeout
        
    @property
    def name(self) -> str:
        return "browser"
    
    @property
    def description(self) -> str:
        return (
            "Visit a website and spy on its content using a real browser. "
            "Useful for dynamic sites (SPA) that fetch fails on. "
            "Returns text content and page title."
        )
    
    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL to visit"
                },
                "screenshot": {
                    "type": "boolean",
                    "description": "Whether to take a screenshot (returns path)",
                    "default": False
                },
                "wait_for_selector": {
                    "type": "string",
                    "description": "Optional CSS selector to wait for before extracting content"
                }
            },
            "required": ["url"]
        }
    
    async def execute(self, url: str, screenshot: bool = False, wait_for_selector: str | None = None, **kwargs: Any) -> str:
        if not PLAYWRIGHT_AVAILABLE:
            return "Error: Playwright is not installed. Please run `pip install playwright && playwright install`."
            
        logger.info(f"Browser visiting: {url}")
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=self.headless)
                context = await browser.new_context(
                    viewport={"width": 1280, "height": 720},
                    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
                page = await context.new_page()
                
                # Navigate
                try:
                    await page.goto(url, timeout=self.timeout, wait_until="domcontentloaded")
                except Exception as e:
                    await browser.close()
                    return f"Error navigating to {url}: {str(e)}"
                
                # Wait for specific element if requested
                if wait_for_selector:
                    try:
                        await page.wait_for_selector(wait_for_selector, timeout=10000)
                    except Exception:
                        logger.warning(f"Timeout waiting for selector: {wait_for_selector}")
                else:
                    # Generic small wait for dynamic content
                    await asyncio.sleep(2)
                
                # Extract data
                title = await page.title()
                content = await page.evaluate("() => document.body.innerText")
                
                result_parts = [
                    f"URL: {url}",
                    f"Title: {title}",
                    "-" * 40,
                    content[:8000] + ("\n... (truncated)" if len(content) > 8000 else "")
                ]
                
                if screenshot:
                    from pathlib import Path
                    media_dir = Path.home() / ".nanobot" / "screenshots"
                    media_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Create safe filename from URL
                    safe_name = "".join(c if c.isalnum() else "_" for c in url.split("//")[-1])[:50]
                    file_path = media_dir / f"{safe_name}.png"
                    
                    await page.screenshot(path=str(file_path))
                    result_parts.insert(0, f"[Screenshot saved to: {file_path}]")
                
                await browser.close()
                return "\n\n".join(result_parts)
                
        except Exception as e:
            logger.error(f"Browser tool error: {e}")
            return f"Error using browser: {str(e)}"
