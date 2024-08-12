import re
import json
from scrapy import Spider
import random 

class TripSpider(Spider):
    name = 'trip'
    start_urls = ['http://www.trip.com/hotels/']  # Update with your start URL

    def parse(self, response):
        script = response.xpath('//script[contains(., "window.IBU_HOTEL")]/text()').get()
        
        if script:
            match = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', script, re.DOTALL)
            if match:
                ibu_hotel_data = match.group(1)
                ibu_hotel_data = ibu_hotel_data.strip()
                
                try:
                    hotel_data_dict = json.loads(ibu_hotel_data)
                    # hotel_data_json = json.dumps(hotel_data_dict, indent=2)
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
                    # Randomly select 3 items from the list
                    random_items = random.sample(combined_list, 3)
                    print("Random:",random_items)

                except json.JSONDecodeError as e:
                    # Handle JSON parsing errors
                    self.log(f"Error decoding JSON: {e}")
                    self.log("Raw data:")
                    self.log(ibu_hotel_data)
