import scrapy

class MySpider(scrapy.Spider):
    name = 'hotel'
    start_urls = ['https://uk.trip.com/hotels/?locale=en-GB&curr=GBP']

    def parse(self, response):
        # Extract all elements with class 'recommend_box'
        elements = response.css('.recommend_box')

        for element in elements:
            # Extract text or other attributes from the element
            text = element.css('::text').get().strip()  # Extract text content
            # If you need other attributes, e.g., href in <a> tags inside the element
            # link = element.css('a::attr(href)').get()

            # Print the extracted text
            print(text)

            # Optionally, you can also yield the items
            yield {'recommend_box_text': text}
