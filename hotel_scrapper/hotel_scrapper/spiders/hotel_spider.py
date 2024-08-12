import re
import json
import scrapy
import random

class TripSpider(scrapy.Spider):
    name = 'trip'
    start_urls = ['https://uk.trip.com/hotels/?locale=en-GB&curr=GBP']  # Update with your start URL

    def parse(self, response):
        script = response.xpath('//script[contains(., "window.IBU_HOTEL")]/text()').get()
        
        if script:
            match = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', script, re.DOTALL)
            if match:
                ibu_hotel_data = match.group(1).strip()
                
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
                    # self.log(f"Combined List: {combined_list}")
                    random_items = random.sample(combined_list, 3)
                    # self.log(f"Random Items: {random_items}")
                    
                    for item in random_items:
                        self.log(f"Processing Item: {item}")
                        yield from self.hotelDetails(item)

                except json.JSONDecodeError as e:
                    self.log(f"Error decoding JSON: {e}")
                    self.log(f"Raw data: {ibu_hotel_data}")

    def hotelDetails(self, random_items):
        self.log(f"Hello_2: {random_items}")
        cities = [338, 722, 318, 1270, 706, 3194]
        if random_items in ["Popular Hotels Worldwide", "Top Luxury 5-star Hotels", "Budget-friendly Hotels Worldwide"]:
            if random_items == "Popular Hotels in ":
                # self.log("Fetching from Popular Hotels in")
                random_city = random.choice(cities)
                url = f"https://uk.trip.com/hotels/list?city={random_city}&checkin=2024/8/12&checkout=2024/08/13"
                self.log(f"Fetching details from: {url}")
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_hotel_details
                )
            elif random_items == "Top Luxury 5-star Hotels":
                # self.log("Fetching from Top Luxury 5-star Hotels")
                random_city = random.choice(cities)
                url = f"https://uk.trip.com/hotels/list?city={random_city}&checkin=2024/8/12&checkout=2024/08/13"
                self.log(f"Fetching details from: {url}")
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_hotel_details
                )

            else:
                # self.log("Fetching from Popular Budget-friendly Hotels Worldwide")
                random_city = random.choice(cities)
                url = f"https://uk.trip.com/hotels/list?city={random_city}&checkin=2024/8/12&checkout=2024/08/13"
                self.log(f"Fetching details from: {url}")
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_hotel_details
                )

        else:
            # self.log("Fetching from Popular Cities in")
            random_city = random.choice(cities)
            url = f"https://uk.trip.com/hotels/list?city={random_city}&checkin=2024/8/12&checkout=2024/08/13"
            self.log(f"Fetching details from: {url}")
            yield scrapy.Request(
                url=url,
                callback=self.parse_hotel_details
            )

    def parse_hotel_details(self, response):
        for hotel in response.xpath('//div[contains(@class, "hotel-info")]'):
            title = hotel.xpath('.//span[contains(@class, "name")]/text()').get(default='').strip()
            rating = hotel.xpath('.//section[contains(@class, "list-card-comment")]//span[contains(@class, "real")]/text()').get(default='').strip()
            location = hotel.xpath('.//div[contains(@class, "list-card-transport-v8")]//span[contains(@class, "trans-icon")]/following-sibling::span/text()').get(default='').strip()
            latitude = hotel.xpath('.//meta[@itemprop="latitude"]/@content').get(default='').strip()
            longitude = hotel.xpath('.//meta[@itemprop="longitude"]/@content').get(default='').strip()
            room_type = hotel.xpath('.//span[contains(@class, "room-panel-roominfo-name")]/text()').get(default='').strip()
            price_text = hotel.xpath('.//div[contains(@class, "room-panel-rt")]//div[contains(@class, "whole")]//div[contains(@class, "real")]/span/div/text()').get()
            price = price_text.strip() if price_text else ''
            images = hotel.xpath('.//div[contains(@class, "multi-images")]//img/@src').getall()
            
            yield {
                'title': title,
                'rating': rating,
                'location': location,
                'latitude': latitude,
                'longitude': longitude,
                'room_type': room_type,
                'price': price,
                'images': images,
            }
