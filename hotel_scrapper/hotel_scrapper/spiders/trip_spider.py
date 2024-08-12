import scrapy
import json
import re

class HotelSpider(scrapy.Spider):
    name = 'trip'
    start_urls = ['https://uk.trip.com/hotels/?locale=en-GB&curr=GBP']  # Replace with the actual URL

    def parse(self, response):
        # Extract all script tags
        scripts = response.xpath('//script/text()').getall()

        for script in scripts:
            # Use regex to find window.IBU_HOTEL
            match = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', script, re.DOTALL)
            if match:
                ibu_hotel_str = match.group(1)
                try:
                    # Convert the JSON-like string to a Python dictionary
                    ibu_hotel = json.loads(ibu_hotel_str)
                    self.log(f'IBU_HOTEL: {ibu_hotel}')
                    # Further processing here
                except json.JSONDecodeError:
                    self.log('Failed to decode JSON')
                break
