import scrapy

class User(scrapy.Item):

    login = scrapy.Field()
    id = scrapy.Field()
    node_id = scrapy.Field()
    avatar_url = scrapy.Field()
    gravatar_id = scrapy.Field()
    url = scrapy.Field()
    html_url = scrapy.Field()
    followers_url = scrapy.Field()
    following_url = scrapy.Field()
    gists_url = scrapy.Field()
    starred_url = scrapy.Field()
    subscriptions_url = scrapy.Field()
    organizations_url = scrapy.Field()
    repos_url = scrapy.Field()
    events_url = scrapy.Field()
    received_events_url = scrapy.Field()
    type = scrapy.Field()
    site_admin = scrapy.Field()

