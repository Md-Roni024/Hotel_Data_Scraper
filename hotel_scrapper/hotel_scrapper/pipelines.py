from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from scrapy.utils.project import get_project_settings
import requests
from scrapy.exceptions import DropItem
import os

Base = declarative_base()

class HotelDetails(Base):
    pass
    __tablename__ = 'hotels_data_1'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    rating = Column(Float)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    room_type = Column(String)
    price = Column(Float)
    image_url = Column(String) 
    image_path = Column(String)

class HotelPipeline:
    pass
    def __init__(self):
        settings = get_project_settings()
        self.engine = create_engine(settings.get('DATABASE_URL'))
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def process_item(self, item, spider):
        session = self.Session()
        # print(f"Image path received in HotelPipeline: {item.get('image_path')}")
        hotel = HotelDetails(
            title=item.get('title'),
            rating=self.parse_float(item.get('rating')),
            location=item.get('location'),
            latitude=self.parse_float(item.get('latitude')),
            longitude=self.parse_float(item.get('longitude')),
            room_type=item.get('room_type'),
            price=self.parse_float(item.get('price')),
            image_url=item.get('image_url'),
            image_path=item.get('image_path')
        )
        # print(f"Image path to be inserted into the database: {hotel.image_path}")

        try:
            session.add(hotel)
            session.commit()
            print("Data successfully inserted")
        except Exception as e:
            session.rollback()
            spider.logger.error(f"Failed to insert data into database: {e}")
        finally:
            session.close()

        return item

    def parse_float(self, value):
        try:
            if isinstance(value, (int, float)):
                return float(value)
            if value in [None, '']:
                return 0.0
            parsed_value = float(value.replace('£', '').replace(',', '').strip())
            print(f"Parsed float value: {parsed_value} from {value}")
            return parsed_value
        except (ValueError, AttributeError):
            print(f"Failed to parse float value: {value}")
            return 0.0

class ImageDownloadPipeline:
    def process_item(self, item, spider):
        image_url = item.get('image_url')
        
        if not image_url:
            raise DropItem("Missing image URL in %s" % item)

        images_dir = 'images'
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)

        image_name = image_url.split('/')[-1]
        image_path = os.path.join(images_dir, image_name)

        response = requests.get(image_url)
        if response.status_code == 200:
            with open(image_path, 'wb') as f:
                f.write(response.content)
            item['image_path'] = image_path
            print(f"Image path set in ImageDownloadPipeline: {item['image_path']}")  # Debugging line
        else:
            raise DropItem("Failed to download image from %s" % image_url)

        return item

