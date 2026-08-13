BOT_NAME = "lcchub_spider"
SPIDER_MODULES = ["lcchub_spider.spiders"]
NEWSPIDER_MODULE = "lcchub_spider.spiders"

ROBOTSTXT_OBEY = False

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

DOWNLOAD_DELAY = 2.0
RANDOMIZE_DOWNLOAD_DELAY = True
CONCURRENT_REQUESTS = 1
DOWNLOAD_TIMEOUT = 60

DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
}

RETRY_TIMES = 2

LOG_LEVEL = "INFO"

ITEM_PIPELINES = {}
