import scrapy


class LccFbPostItem(scrapy.Item):
    source = scrapy.Field()      # page name
    type = scrapy.Field()        # text | photo | video | link
    url = scrapy.Field()         # canonical post url
    body = scrapy.Field()        # post text
    image_url = scrapy.Field()   # photo url (photo posts)
    link_url = scrapy.Field()    # external link (link posts)
    posted_at = scrapy.Field()   # timestamp if available
