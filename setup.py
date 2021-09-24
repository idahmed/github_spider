from setuptools import find_packages, setup

setup(
    name="Zyda menu Crawler",
    version="1.0",
    packages=find_packages(),
    entry_points={"scrapy": ["settings = zdmenu_spiders.settings"]},
)
