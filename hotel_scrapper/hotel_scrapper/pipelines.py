from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from scrapy.utils.project import get_project_settings

Base = declarative_base()

class HotelDetails(Base):
    __tablename__ = 'hotels_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
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
    
    def process_item(self, item, spider):
        session = self.Session()
        hotel = HotelDetails(
            title=item.get('title'),
            rating=self.parse_float(item.get('rating')),
            location=item.get('location'),
            latitude=self.parse_float(item.get('latitude')),
            longitude=self.parse_float(item.get('longitude')),
            room_type=item.get('room_type'),
            price=self.parse_float(item.get('price')),
            image_url=item.get('image_url'),
        )
        print(f"Hotel object to be inserted: {hotel}")

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
