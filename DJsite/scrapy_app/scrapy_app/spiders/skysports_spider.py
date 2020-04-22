import scrapy
from ..items import Skysports_item
from .cbs_spider import MyHTMLParser


class Skysports_links(scrapy.Spider):
    name = 'skysports_content'
    start_urls = ['https://www.skysports.com']

    def parse(self, response):
        menu_links = self.parse_menu_links(response)
        for link in menu_links:
            if link == '/mma' or link == '/nba':
                request = response.follow(link + '/news', callback=self.parse_nba_mma)
                request.meta['menu_link'] = link
                yield request
            else:
                for page_number in range(1, 2, 1):
                    request = response.follow(link + '/news/more/' + str(page_number), callback=self.parse_news_links)
                    request.meta['menu_link'] = link
                    yield request

    def parse_menu_links(self, response):
        sport_category_menu = response.xpath("//div[contains(@class,'site-header')]"
                                             "//div[@id='site-nav-desktop-sports-more-nav']"
                                             "//ul[@class='site-nav-desktop__menu-links']//@href").getall()
        return sport_category_menu

    def parse_news_links(self, response):
        menu_link = response.meta['menu_link']
        form_menu_link = menu_link.replace('/', '')

        links = response.xpath("//div[contains(@class,'grid__col site-layout-secondary__col1')]"
                               "//a[contains(@class,'news-list__figure')]//@href").getall()
        tags = response.xpath("//div[contains(@class,'grid__col site-layout-secondary__col1')]"
                              "//a[contains(@class,'label__tag')]/text()").getall()
        number_of_link = 1
        link = links[number_of_link]
        # for link in links:
        if form_menu_link in link.split('/'):
            request = response.follow(link, callback=self.parse_skysports_content)
            request.meta['menu_link'] = form_menu_link
            request.meta['link'] = link
            request.meta['tag'] = tags[number_of_link]
            yield request
            number_of_link += 1

    def parse_nba_mma(self, response):
        menu_link = response.meta['menu_link']
        form_menu_link = menu_link.replace('/', '')
        images = None
        links = response.xpath("//div[@id='load-more-list']//a[@class='sdc-site-tile__headline-link']//@href").getall()
        if form_menu_link == 'mma':
            images = response.xpath(
                "//div[@id='load-more-list']//div[contains(@class,'sdc-site-tile__image-wrap')]//img").getall()
        number_of_link = 0
        link = links[number_of_link]
        # for link in links:
        if form_menu_link in link.split('/'):
            request = response.follow(link, callback=self.parse_skysports_content)
            request.meta['menu_link'] = form_menu_link
            request.meta['link'] = link
            request.meta['tag'] = None
            if images:
                request.meta['image'] = images[number_of_link]
            else:
                request.meta['image'] = images
            yield request
            number_of_link += 1

    def parse_skysports_content(self, response):
        items = Skysports_item()
        article = response.xpath("//div[contains(@class,'article')]//p|"
                                 "//div[contains(@class,'article')]//h3|"
                                 "//div[contains(@class,'article')]//div[@class='article__widge-container "
                                 "article__widge-container--edge']//img|"
                                 "//div[contains(@class,'article')]//figure[@class='widge-figure widge-figure--video']//img|"
                                 "//div[contains(@class,'widge-figure__text')]|"
                                 "//div[contains(@class,'sdc-article-widget sdc-article-image')]//span[@class='sdc-article-image__caption-text']/text()|"
                                 "//div[contains(@class,'article')]//img[contains(@class,'sdc-article-image__item')]").getall()
        long_title = response.xpath("//span[@class='article__long-title']/text()|"
                                    "//span[@class='sdc-article-header__long-title']/text()").get()
        author = response.xpath("//h3[@class='article__writer-name']/text()").get()
        title = response.xpath('//h1[@class="article__title"]/@data-short-title|'
                               '//h1[@class="sdc-article-header__title"]/@data-short-title').get()
        formatted_article = list()
        number_of_image = 0
        image = None
        form_image = None
        for string in article:
            if string.startswith('<h3>'):
                formatted_article.append(string)
            if string.startswith('<p>') and 'class="widge-marketing__text">' not in string :
                # and "<strong>" not in string \
                #     and '<em>' not in string:
                formatted_article.append(string)
            if string.startswith(
                    '<img') and 'excluded-article' not in string and 'class="sdc-article-video__media"' not in string \
                    and 'widge-figure__image auto-size__target' not in string:
                # and 'auto-size__target postpone-load postpone-load--fade-in widge-figure__image' not in string:
                number_of_image += 1
                if number_of_image == 1:
                    image = string
                else:
                    str = string.replace('data-src', 'src')
                    formatted_article.append('<div>' + str + '</div>')
            if string.startswith('<div'):
                str1 = string.replace('<div class="widge-figure__text" property="caption">', '<h4>')
                str2 = str1.replace('</div>', '</h4>')
                formatted_article.append(str2)
            if not string.startswith('<'):
                str = '<h4>'+string+'</h4>'
                formatted_article.append(str)
        parser = MyHTMLParser()
        if image:
            parser.feed(image)
            form_image = parser.d

        items['body'] = formatted_article
        items['long_title'] = long_title
        items['author'] = author
        items['link'] = response.meta['link']
        items['menu_link'] = response.meta['menu_link']
        items['tags'] = []
        items['tags'].append(response.meta['tag'])
        items['tags'].append(response.meta['menu_link'])
        items['title'] = title
        items['image'] = form_image
        yield items
