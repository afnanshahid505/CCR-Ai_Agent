import asyncio
import json
from datetime import datetime
from pathlib import Path

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

START_URL = "https://govt.westlaw.com/calregs"

OUTPUT_FILE = Path("data/all_discovered_urls.jsonl")
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)


async def main():

    config = CrawlerRunConfig(
        word_count_threshold=0,
        cache_mode=CacheMode.BYPASS,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )

    async with AsyncWebCrawler(verbose=True) as crawler:

        result = await crawler.arun(url=START_URL, config=config)

        record = {
            "url": START_URL,
            "crawled_at": datetime.utcnow().isoformat(),
            "html": result.html or "",
            "markdown": result.markdown or ""
        }

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

        print("\nSaved page to:", OUTPUT_FILE)


if __name__ == "__main__":
    asyncio.run(main())