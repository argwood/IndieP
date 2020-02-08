import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
#test with a smaller subset of games, only 41 results, 2 pages

class SteamSpider(CrawlSpider):
    name = 'indie_action_rpg_f2p'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['http://store.steampowered.com/search/?sort_by=Name_ASC&tags=492%2C21%2C122%2C113%2C4182&category1=998&supportedlang=english']
    rules = (Rule(LinkExtractor(allow='page=(\d+)', restrict_css='.search_pagination_right'), callback='parse_page', follow=True),)

    def parse_page(self, response):
        #for game in response.css('a.search_result_row.ds_collapse_flag.app_impression_tracked'):
        for game in response.css('a.search_result_row'):
        #for game in response.css('div.responsive_search_name_combined'):
            #print(game.xpath('span[@class="title"]/text()').extract())
            yield {
                    'appid': game.css('a::attr(data-ds-appid)').get(),
                    'url': game.css('a[href*=store]::attr(href)').get(),
                    'title': game.css('span.title::text').get(),
                    #'title': game.css('div/span/span.title::text').get(),
                    'release_date': game.css('div.col.search_released.responsive_secondrow::text').get(),
                    'price': game.css('div.col.search_price.responsive_secondrow::text').get().strip(),
            }
            #next_page = response.css('a.pagebtn a::attr("href")').get()
            #if next_page is not None:
            #    yield response.follow(next_page, self.parse)
