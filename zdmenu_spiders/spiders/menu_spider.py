from __future__ import print_function

import datetime
import logging
import re
from typing import Generator
import json

import requests
from bs4 import BeautifulSoup
from scrapy import Request

from zdmenu_spiders import settings
from zdmenu_spiders.items_loader import MenuItemsLoader
from zdmenu_spiders.settings import USER_AGENT
from zdmenu_spiders.spiders import BaseSpider
from zdmenu_spiders.utils.classifier import (
    DirectCompetitorsClassifier,
    FoodAggregatorClassifier,
    IndirectCompetitorsClassifier,
)
from zdmenu_spiders.utils.gsheet import IGSheet

logger = logging.getLogger(__name__)


class MenuSpider(BaseSpider):
    """ MenuSpider Spider uses ZYDA API endpoints to get menu items data.
    """

    name = "menu_spider"
    base_url = "https://www.talabat.com/menuapi/v2/branches/"

    def start_requests(self) -> Request:
        logger.info("Starting spider for ZYDA menu items collection process.")
        
        # talabat API endpoint needs restaurant id
        url = f"{self.base_url}{self.rest_id}/menu"
        
        # Initiating the first request.
        yield Request(
            url,
            callback=self.parse_menu_items,
            dont_filter=True,
            errback=self.parse_menu_items,
        )

    def parse_menu_items(self, response) -> Request:
        """ catch menu items in response and load items to csv file.
        """
        json_response = json.loads(response.text)

        for category in json_response["result"]["menu"]["menuSection"]:
            for itm in category["itm"]:

                loader = MenuItemsLoader()
                for key in itm:
                    loader.add_value(key, itm.get(key, ""))

                yield loader.load_item()
