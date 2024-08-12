import re
import json
from scrapy import Spider
import random 

class TripSpider(Spider):
    name = 'trip'
    start_urls = ['https://uk.trip.com/hotels/?locale=en-GB&curr=GBP']  # Update with your start URL

    def parse(self, response):
        script = response.xpath('//script[contains(., "window.IBU_HOTEL")]/text()').get()
        
        if script:
            match = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', script, re.DOTALL)
            if match:
                ibu_hotel_data = match.group(1)
                ibu_hotel_data = ibu_hotel_data.strip()
                
                try:
                    hotel_data_dict = json.loads(ibu_hotel_data)
                    
                    Translate = hotel_data_dict['translate']
                    polular_hotel_country = Translate['key.hotel.homepage.hotelrecommendation.hotdomestichotels'].split('%')[0]
                    polular_hotel_worldwide = Translate['key.hotel.homepage.hotelrecommendation.hotoverseashotels']
                    polular_hotel_citiesIn = Translate['key.hotel.homepage.hotelrecommendation.hotdomesticcities'].split('%')[0]
                    polular_hotel_cities_worldwide = Translate['key.hotel.homepage.hotelrecommendation.hotoverseascities']
                    polular_hotel_hot5starhotels = Translate['key.hotel.homepage.hotelrecommendation.hot5starhotels']
                    polular_hotel_hotcheaphotels = Translate['key.hotel.homepage.hotelrecommendation.hotcheaphotels']

                    combined_list = [
                        polular_hotel_country,
                        polular_hotel_worldwide,
                        polular_hotel_citiesIn,
                        polular_hotel_cities_worldwide,
                        polular_hotel_hot5starhotels,
                        polular_hotel_hotcheaphotels
                    ]
                    print("Combined:",combined_list)

                    # Randomly select 3 items from the list
                    random_items = random.sample(combined_list, 3)

                    # Call the hotelDetails method
                    for item in random_items:
                        self.hotelDetails(item, hotel_data_dict)

                except json.JSONDecodeError as e:
                    # Handle JSON parsing errors
                    self.log(f"Error decoding JSON: {e}")
                    self.log("Raw data:")
                    self.log(ibu_hotel_data)

    def hotelDetails(self,random_items,hotel_data_dict):
        if random_items =="Popular Hotels Worldwide" or random_items=="Top Luxury 5-star Hotels" or random_items=="Budget-friendly Hotels Worldwide":
            if random_items =="Popular Hotels in ":
                cities = [338,722,318,1270,706,3194]
                random_city = random.sample(cities)
                url = f"https://uk.trip.com/hotels/list?city={random_city}&checkin=2024/8/12&checkout=2024/08/13"
                self.log(f"Fetching details from: {url}")
                # Make a new request to the generated URL
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_hotel_details
                )

        else:
            if random_items =="Popular Hotels in ":
                cities = [338,722,318,1270,706,3194]
                random_city = random.sample(cities)
                url = f"https://uk.trip.com/hotels/list?city={random_city}&checkin=2024/8/12&checkout=2024/08/13"
                self.log(f"Fetching details from: {url}")
                # Make a new request to the generated URL
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_hotel_details
                )

            elif random_items =="Popular Cities in ":
                cities = [338,722,318]
                random_city = random.sample(cities)
                url = f"https://uk.trip.com/hotels/list?city={random_city}&checkin=2024/8/12&checkout=2024/08/13"
                self.log(f"Fetching details from: {url}")
                # Make a new request to the generated URL
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_hotel_details
                )
            else:
                cities = [338,722,318]
                random_city = random.sample(cities)
                url = f"https://uk.trip.com/hotels/list?city={random_city}&checkin=2024/8/12&checkout=2024/08/13"
                self.log(f"Fetching details from: {url}")
                # Make a new request to the generated URL
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_hotel_details
                )

        def parse_hotel_details(self, response):
            for hotel in response.xpath('//div[contains(@class, "hotel-info")]'):
                title = hotel.xpath('.//span[contains(@class, "name")]/text()').get()
                yield {
                    'title': title,
                    'rating': hotel.xpath('.//section[contains(@class, "list-card-comment")]//span[contains(@class, "real")]/text()').get(),
                    'location': hotel.xpath('.//div[contains(@class, "list-card-transport-v8")]//span[contains(@class, "trans-icon")]/following-sibling::span/text()').get(),
                    'latitude': hotel.xpath('.//meta[@itemprop="latitude"]/@content').get(),
                    'longitude': hotel.xpath('.//meta[@itemprop="longitude"]/@content').get(),
                    'room_type': hotel.xpath('.//span[contains(@class, "room-panel-roominfo-name")]/text()').get(),
                    'price': hotel.xpath('.//div[contains(@class, "room-panel-rt")]//div[contains(@class, "whole")]//div[contains(@class, "real")]/span/div/text()').get().strip(),
                    'images': hotel.xpath('.//div[contains(@class, "multi-images")]//img/@src').getall(),
                }

