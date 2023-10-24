import logging

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import S3FilesStore

logger = logging.getLogger(__name__)


class S3FilesStore(S3FilesStore):
    @classmethod
    def from_settings(cls, settings):
        uri = settings.get("FEED_URI")
        return S3FilesStore(uri)

class UserPipeline(object):
    def process_item(self, item, spider):
        return item
