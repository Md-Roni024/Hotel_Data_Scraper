import re
import json
import scrapy
import random

class TripSpider(scrapy.Spider):
    name = 'hotel_spider'
    start_urls = ['https://uk.trip.com/hotels/?locale=en-GB&curr=GBP']

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
                    random_items = random.sample(combined_list, 3)    
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
                random_city = random.choice(cities)
                url = f"https://uk.trip.com/hotels/list?city={random_city}&checkin=2024/8/12&checkout=2024/08/13"
                self.log(f"Fetching details from: {url}")
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_hotel_details
                )
            elif random_items == "Top Luxury 5-star Hotels":
                random_city = random.choice(cities)
                url = f"https://uk.trip.com/hotels/list?city={random_city}&checkin=2024/8/12&checkout=2024/08/13"
                self.log(f"Fetching details from: {url}")
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_hotel_details
                )

            else:
                random_city = random.choice(cities)
                url = f"https://uk.trip.com/hotels/list?city={random_city}&checkin=2024/8/12&checkout=2024/08/13"
                self.log(f"Fetching details from: {url}")
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_hotel_details
                )

        else:
            random_city = random.choice(cities)
            url = f"https://uk.trip.com/hotels/list?city={random_city}&checkin=2024/8/12&checkout=2024/08/13"
            self.log(f"Fetching details from: {url}")
            yield scrapy.Request(
                url=url,
                callback=self.parse_hotel_details
            )

    def parse_hotel_details(self, response):
        script = response.xpath('//script[contains(., "window.IBU_HOTEL")]/text()').get()
        
        if script:
            match = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', script, re.DOTALL)
            if match:
                ibu_hotel_data = match.group(1).strip()
                
                try:
                    hotel_data_dict = json.loads(ibu_hotel_data)
                    Translate = hotel_data_dict['initData']
                    firstPageList = Translate['firstPageList']
                    hotelList = firstPageList['hotelList']

                    # Iterating over each hotel
                    for hotel in hotelList:
                        hotel_info = hotel.get('hotelBasicInfo')
                        hotel_name = hotel_info.get('hotelName')
                        hotelAddress = hotel_info.get('hotelAddress')
                        price = hotel_info.get('price')
                        image_url = hotel_info.get('hotelImg')

                        comment_info = hotel.get('commentInfo', {})
                        rating = comment_info.get('commentScore')

                        roomInfo = hotel.get('roomInfo', {})
                        roomType = roomInfo.get('physicalRoomName')


                        positionInfo = hotel.get('positionInfo', {})
                        coordinate = positionInfo.get('coordinate',{})
                        longitude = coordinate.get('lng')
                        latitude = coordinate.get('lat')
                        yield {
                            'title': hotel_name,
                            'rating': rating,
                            'location': hotelAddress,
                            'latitude': latitude,
                            'longitude': longitude,
                            'room_type': roomType,
                            'price': price,
                            'image_url': image_url,
                        }

                except json.JSONDecodeError as e:
                    self.log(f"Error decoding JSON: {e}")
                    self.log(f"Raw data: {ibu_hotel_data}")
