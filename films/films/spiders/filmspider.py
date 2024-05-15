import random

import scrapy
from scrapy import Request

import random
import scrapy
from scrapy import Request


#TMDB

class TMDBSpider(scrapy.Spider):
    name = 'tmdb'
    allowed_domains = ['themoviedb.org']
    start_urls = ['https://www.themoviedb.org/movie?language=tr&page=1']
    custom_settings = {
        'DOWNLOAD_DELAY': 2
    }

    def parse(self, response):
        # Film bilgilerini çekme
        movies = response.css('div.card.style_1')
        for movie in movies:
            detail_url = response.urljoin(movie.css('h2 a::attr(href)').get())
            yield scrapy.Request(detail_url, callback=self.parse_movie_details)

        current_page = int(response.url.split('page=')[-1])
        next_page = current_page + 1
        next_page_url = f'https://www.themoviedb.org/movie?language=tr&page={next_page}'

        if next_page <= 500:  # 500 sayfa veri var
            yield response.follow(next_page_url, callback=self.parse)

    def parse_movie_details(self, response):
        facts = response.css('section.split_column p')

        # 'Orijinal Başlık' her filmde yok, ona göre veri çekiyoruz.
        has_original_title = 'Orijinal Başlık' in facts[0].css('::text').extract_first()

        if has_original_title:
            original_language_index = 2
            budget_index = 3
            revenue_index = 4
        else:
            original_language_index = 1
            budget_index = 2
            revenue_index = 3

        original_language = facts[original_language_index].css('::text').extract()
        original_language = original_language[1].strip() if len(original_language) > 1 else None

        budget_and_revenue = facts[budget_index].css('::text').extract()
        budget = budget_and_revenue[1].strip() if len(budget_and_revenue) > 1 else None

        revenue_and_revenue = facts[revenue_index].css('::text').extract()
        revenue = revenue_and_revenue[1].strip() if len(revenue_and_revenue) > 1 else None

        yield {
            'title': response.css('div.single_column h2 a::text').get(),
            'release_date': response.css('div.facts span.release::text').get().strip(),
            'rating': response.css('.user_score_chart::attr(data-percent)').get(),
            'director': response.css('ol.people.no_image li.profile:contains("Director") a::text').get(),
            'writer': response.css('ol.people.no_image li.profile:contains("Writer") a::text').get(),
            'genres': response.css('span.genres a::text').getall(),
            'runtime': response.css('span.runtime::text').get().strip(),
            'original_language': original_language,
            'budget': budget,
            'revenue': revenue
        }











'''

#Letterboxd


class FilmspiderSpider(scrapy.Spider):
    name = "filmspider"
    allowed_domains = ["letterboxd.com"]
    start_urls = ["https://letterboxd.com/films/popular/this/week/decade/2020s/"]

    ## myspider.py

    import random

    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
    ]



    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse,
                           headers={"User-Agent": self.user_agent_list[random.randint(0, len(self.user_agent_list) - 1)]})



    def parse(self, response):
        films = response.css('li.listitem.poster-container.film-not-watched')
        for film in films:
            # Film adını ve yılı çek
            name = film.css('div.film-poster a img::attr(alt)').get()
            url = response.urljoin(film.css('div.film-poster a::attr(href)').get())

            # Yield yapısı ile veriyi döndür
            yield {
                'name': name,
                'url': url
            }
            
            
            '''


'''          
        next_page = response.css('li.next a ::attr(href)').get()
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback=self.parse)


'''







'''

#BeyazPerde

import random
import scrapy
from scrapy import Request

class BeyazperdeSpider(scrapy.Spider):
    name = "beyazperde"
    allowed_domains = ["beyazperde.com"]
    start_urls = ["https://www.beyazperde.com/filmler/tum/"]

    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse,
                          headers={"User-Agent": random.choice(self.user_agent_list)})

    def parse(self, response):
        # Film bilgilerini çekme
        films = response.css('div.card.entity-card.entity-card-list.cf')
        for film in films:
            yield {
                'name': film.css('h2.meta-title a::text').get().strip(),
                'release_date': film.css('div.meta-body-info::text').re_first(r'\d{1,2} \w+ \d{4}'),
                'director': film.css('span.light a::text').get(),
                'actors': film.css('span.light::text').extract(),
                'url': response.urljoin(film.css('h2.meta-title a::attr(href)').get())
            }

        next_page = response.css('a.button.button-md.button-primary::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

'''
















'''

import scrapy

class LetterboxSpider(scrapy.Spider):
    name = "letterboxd"
    allowed_domains = ["letterboxd.com"]
    start_urls = ["https://letterboxd.com/films/decade/2020s/"]

    def parse(self, response):
        # Filmlerin sayfa linklerini çek
        film_links = response.css('ul.poster-list li div.film-poster a::attr(href)').getall()
        for link in film_links:
            full_url = response.urljoin(link)
            yield scrapy.Request(full_url, callback=self.parse_movie)

    def parse_movie(self, response):
        # Her bir film sayfasından detayları çek
        title = response.css('h1::text').get()
        year = response.css('small a::text').get()
        director = response.css('a[href*="/director/"]::text').get()
        cast_links = response.css('div.cast-list a::attr(href)').getall()
        cast_names = response.css('div.cast-list a::text').getall()

        yield {
            'title': title,
            'year': year,
            'director': director,
            'cast_links': cast_links,
            'cast_names': cast_names
        }



'''