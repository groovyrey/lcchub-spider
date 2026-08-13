import re

import scrapy
from lcchub_spider.items import LccFbPostItem


class LccFbSpider(scrapy.Spider):
    name = "lcc_fb"
    allowed_domains = ["facebook.com", "fbcdn.net"]
    start_urls = ["https://www.facebook.com/laconcepcioncollege"]

    def __init__(self, page=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if page:
            self.start_urls = [f"https://www.facebook.com/{page}"]

    def parse(self, response):
        html = response.text
        page = response.url.rstrip("/").split("/")[-1]

        seen = set()
        for post_id in re.findall(r"/posts/(\d+)", html):
            if post_id in seen:
                continue
            seen.add(post_id)
            yield self._extract_post(html, post_id, page, "posts")

        for photo_id in re.findall(r"/photos/([^\"'\\s]+)", html):
            if photo_id in seen:
                continue
            seen.add(photo_id)
            yield self._extract_post(html, photo_id, page, "photos")

        for video_id in re.findall(r"/(?:videos|reel)/(\d+)", html):
            if video_id in seen:
                continue
            seen.add(video_id)
            yield self._extract_post(html, video_id, page, "videos")

    def _extract_post(self, html, post_id, page, kind):
        idx = html.find(post_id)
        window = html[max(0, idx - 4000): idx + 4000]

        item = LccFbPostItem()
        item["source"] = page
        item["url"] = f"https://www.facebook.com/{page}/{kind}/{post_id}"
        item["posted_at"] = None
        item["image_url"] = None
        item["link_url"] = None

        images = re.findall(r"https://scontent[^\"'\\\\ ]+\.fbcdn\.net[^\"'\\\\ ]+", window)
        item["image_url"] = images[0] if images else None

        text = self._clean_text(window)
        item["body"] = text[:2000] if text else None

        video_link = re.search(r"href=\"(?:/[^\"]*)?(?:videos|reel)/" + post_id, window)
        item["type"] = "photo" if item["image_url"] else "text"

        ext_links = re.findall(r"href=\"(https?://[^\"]+)\"", window)
        external = [u for u in ext_links if "facebook.com" not in u and "fbcdn.net" not in u]
        item["link_url"] = external[0] if external else None
        if external:
            item["type"] = "link"

        if video_link:
            item["type"] = "video"

        return item

    def _clean_text(self, window):
        # strip tags, decode entities, collapse whitespace
        text = re.sub(r"<[^>]+>", " ", window)
        text = text.replace("&amp;", "&").replace("&quot;", '"').replace("&#039;", "'")
        text = re.sub(r"\s+", " ", text).strip()
        # keep the longest natural-language segment (roughly > 30 chars, has spaces)
        best = ""
        for chunk in text.split("  "):
            if len(chunk) > len(best) and " " in chunk:
                best = chunk
        return best or None
