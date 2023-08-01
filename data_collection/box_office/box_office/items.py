# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BoxOfficeItem(scrapy.Item):
    title = scrapy.Field()
    original_title = scrapy.Field()
    entries = scrapy.Field()
    director = scrapy.Field()
    release_date = scrapy.Field()
    duration = scrapy.Field()


class FeaturesItem(scrapy.Item):
    title = scrapy.Field()
    director = scrapy.Field()
    actors = scrapy.Field()
    id_film = scrapy.Field()
    synopsis = scrapy.Field()
    release_date = scrapy.Field()
    duration = scrapy.Field()
    genre = scrapy.Field()
    language = scrapy.Field()
    country = scrapy.Field()
    original_title = scrapy.Field()
    distrib = scrapy.Field()
