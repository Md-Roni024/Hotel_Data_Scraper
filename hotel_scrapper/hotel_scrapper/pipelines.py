import os
import urllib.request
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from scrapy.utils.project import get_project_settings

Base = declarative_base()

class HotelDetails(Base):
    __tablename__ = 'hotel_details'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    rating = Column(Float)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    room_type = Column(String)
    price = Column(Float)
    image_url = Column(String)

class HotelPipeline:
    def __init__(self):
        settings = get_project_settings()
        self.engine = create_engine(settings.get('DATABASE_URL'))
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        
        # Directory to store images
        self.image_dir = 'images'
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)
    
    def process_item(self, item, spider):
        session = self.Session()

        # Handle image URL
        image_url = item.get('image_url', [])
        image_filename = None
        if image_url:
            image_url = image_url[0]  # Assuming image_url is a list and taking the first element
            image_filename = os.path.join(self.image_dir, os.path.basename(image_url))
            try:
                urllib.request.urlretrieve(image_url, image_filename)
            except Exception as e:
                spider.logger.error(f"Failed to download image {image_url}: {e}")
                image_filename = None
        
        # Prepare data for insertion
        hotel = HotelDetails(
            name=item.get('title'),
            rating=self.parse_float(item.get('rating')),
            location=item.get('location'),
            latitude=self.parse_float(item.get('latitude')),
            longitude=self.parse_float(item.get('longitude')),
            room_type=item.get('room_type'),
            price=self.parse_float(item.get('price')),
            image_url=image_filename
        )

        try:
            session.add(hotel)
            session.commit()
        except Exception as e:
            session.rollback()
            spider.logger.error(f"Failed to insert data into database: {e}")
        finally:
            session.close()

        return item

    def parse_float(self, value):
        try:
            if value in [None, '']:
                return 0.0
            return float(value.replace('£', '').replace(',', '').strip())
        except (ValueError, AttributeError):
            return 0.0
