import os

BOT_NAME = "github_spiders"

SPIDER_MODULES = ["github_spiders.spiders"]
NEWSPIDER_MODULE = "github_spiders.spiders"


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 "
    "Safari/537.36 Edg/91.0.864.59 "
)

FEED_URI = os.getenv("FEED_URI", "output/crawler/%(name)s.jsonl")
FEED_FORMAT = "csv"
FEED_EXPORT_ENCODING = "utf-8"
FEED_STORE_EMPTY = False
FEED_EXPORTERS = {
    "jsonlines": "github_spiders.exporters.UserExporter",
}

# Enable to print all duplicate filter detected (for development/debug purposes)
DUPEFILTER_DEBUG = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 40

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
AUTOTHROTTLE_ENABLED = True
DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 40

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "github_spiders.pipelines.UserPipeline": 300,
}

# RETRY MIDDLEWARE
# https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#retry-enabled

RETRY_ENABLED = True
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]
# RETRY_TIMES = 4
HTTPERROR_ALLOWED_CODES = [404]
