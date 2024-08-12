# Scrapy Assignment
The assignment involves developing a Scrapy project to scrape hotel property data from Trip.com and store the information in a PostgreSQL database using SQLAlchemy. The project must handle various web structures, paginate through pages, and store images in a directory with database references. Additionally, the assignment requires the implementation of random selection from specific sections of the website, ensuring comprehensive data collection and proper documentation.
### Technology stack
As the name suggests, this repository is built by Scrapy & PostgreSQL, however, in the implementation detail, we will find other supporting technologies as well.

<img src="https://img.shields.io/badge/Scrapy-%23007A8F?style=for-the-badge&logo=scrapy&logoColor=white" alt="Scrapy" width="60" height="25"/>: For web scraping to extract hotel property data from Trip.com.

<img src="https://img.shields.io/badge/PostgreSQL-%2331575F?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" width="60" height="25"/>: For the database to store user information, complaints, and other relevant data.

<img src="https://img.shields.io/badge/Postman-%23FF6C37?style=for-the-badge&logo=postman&logoColor=white" alt="Postman" width="60" height="25"/> : For testing API endpoints and ensuring smooth communication.





### Running the backend 
Before running the application, make sure you have the following installed:

1. Clone the project
    ```bash
    git clone https://github.com/Md-Roni024/Scrapy_Assignment
    ```  

2. Go to the project directory and Create Virtual Environment
    ```
    cd hotel_scrapper
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3. Create a .env file then add your variables credentials as like:
    ```
    DB_USER=Database User Name
    HOST=Hostname
    DATABASE=Database Name
    PASSWORD=Database Password
    PORT=Database Port
    ```
4. Run Spider
    ```
    cd hotel_scrapper
    scrapy crawl trip -o hotels.json

    ```
  

### Design Database Schema
- Database Name: <span style="color:red;font-size:15px;font-weight:bold">hotel_db</span>

- Hotel Deatils Table
  ```sql
    CREATE TABLE hotel_details (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        address TEXT,
        rating DECIMAL(3, 2),
        location VARCHAR(255),
        latitude DECIMAL(9, 6),
        longitude DECIMAL(9, 6),
        room_type VARCHAR(255),
        price DECIMAL(10, 2),
        image_path TEXT
    );
  ```

  

### Contributing
- Contributing is an open invitation for collaboration on the project. You're encouraged to participate by opening issues for bugs or feature requests and submitting pull requests with your improvements or fixes. Your contributions help enhance and grow the project, making it better for everyone.


### Contact

- For any questions or feedback, please reach out to me at roni.cse024@gmail.com. I welcome all inquiries and look forward to hearing from you. Your input is valuable and appreciated!


