from __future__ import print_function

import datetime
import logging
import re
from typing import Generator
import json

import requests
from bs4 import BeautifulSoup
from scrapy import Request

from github_spiders import settings
from github_spiders.items_loader import UserLoader
from github_spiders.settings import USER_AGENT
from github_spiders.spiders import BaseSpider
from github_spiders.utils.classifier import (
    DirectCompetitorsClassifier,
    FoodAggregatorClassifier,
    IndirectCompetitorsClassifier,
)
from github_spiders.utils.gsheet import IGSheet

logger = logging.getLogger(__name__)


class UsersSpider(BaseSpider):
    """ Users spider uses github apis to collect users.
    """

    name = "github_spider"
    base_url = "https://api.github.com/user"

    def start_requests(self) -> Request:
        logger.info("Starting spider for github users collection process.")
        
        # talabat API endpoint needs restaurant id
        url = f"{self.base_url}"
        
        # Initiating the first request.
        yield Request(
            url,
            callback=self.parse_users,
            dont_filter=True,
            errback=self.parse_users,
        )

    def parse_users(self, response) -> Request:
        """ catch users in response and load them to csv file.
        """
        json_response = json.loads(response.text)

        for user in json_response:

            loader = UserLoader()
            for key in user:
                loader.add_value(key, user.get(key, ""))

            yield loader.load_item()
