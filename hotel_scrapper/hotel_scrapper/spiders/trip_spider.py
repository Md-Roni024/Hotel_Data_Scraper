import scrapy

class HotelSpider(scrapy.Spider):
    name = 'trip'
    start_urls = ['https://uk.trip.com/hotels/?locale=en-GB&curr=GBP']

    def parse(self, response):
        # Extract the title
        title = response.css('.boundCities_title::text').get()
        self.log(f'Title found: {title}')
        
        # Yield the results as items
        yield {
            'title': title,
        }
