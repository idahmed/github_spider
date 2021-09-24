from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose

from zdmenu_spiders.items import MenuItems


class MenuItemsLoader(ItemLoader):
    default_input_processor = MapCompose(str)
    default_output_processor = Join(";")
    default_item_class = MenuItems
