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

        # Save image and get its filename
        image_url = item.get('image_url')
        image_filename = os.path.join(self.image_dir, os.path.basename(image_url))
        urllib.request.urlretrieve(image_url, image_filename)
        
        hotel = HotelDetails(
            name=item.get('name'),
            rating=float(item.get('rating', 0).split()[0].replace(',', '')),
            location=item.get('location'),
            latitude=float(item.get('latitude', 0)),
            longitude=float(item.get('longitude', 0)),
            room_type=item.get('room_type'),
            price=float(item.get('price', 0).replace('£', '').replace(',', '')),
            image_url=image_filename
        )

        session.add(hotel)
        session.commit()
        session.close()

        return item
