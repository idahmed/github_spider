from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose

from github_spiders.items import User


class UserLoader(ItemLoader):
    default_input_processor = MapCompose(str)
    default_output_processor = Join(";")
    default_item_class = User
