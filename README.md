# Scrapy Assignment
This is a full-stack site <span style="color: red;font-size:20px">Backend</span> built with Node.js and Express.js stores hotel and room details. It uses PostgreSQL to manage data like hotel slug,title,host name,host email,bedroom count,guest count and amenities. The backend provides APIs to create & read this information. It ensures data is accurate and easy to query. This setup allows the frontend to display hotel and room details for users.

### Technology stack

As the name suggests, this repository is built on top of Scrapy & PostgreSQL, however, in the implementation detail, we will find other supporting technologies as well.

### Technology Stack

As the name suggests, this repository is built on top of Node.js, Express.js & PostgreSQL, however, in the implementation detail, we will find other supporting technologies as well.

<img src="https://img.shields.io/badge/PostgreSQL-%2331575F?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" width="60" height="25"/>: For the database to store user information, complaints, and other relevant data.

<img src="https://img.shields.io/badge/Postman-%23FF6C37?style=for-the-badge&logo=postman&logoColor=white" alt="Postman" width="60" height="25"/> : For testing API endpoints and ensuring smooth communication between frontend and backend.




### Running the backend 
Before running the application, make sure you have the following installed:

- Scrapy
- Postgresql

1. Clone the project
    ```bash
    git clone https://github.com/Md-Roni024/Scrapy_Assignment
    ```  

2. Go to the project directory and Create Virtual Environment
    ```
    cd hotel_scraper
    python3 -m venv myenv
    source venv/bin/activate
    pip install scrapy
    ```
3. Create a .env file then add your variables credentials as like:
    ```
    USER = "Postgress User Name"
    HOST = "Host Name"
    DATABASE = "Database Name"
    PASSWORD = "Postgress Password"

    //Server Listening PORT
    PORT = ""
    ```
4. Run Spider
    ```
    cd hotel_scrapper
    scrapy crawl hotel -o hotels.json

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


  ### Demo Input Data:
  - For hote_details table
  

### Contributing
- Contributing is an open invitation for collaboration on the project. You're encouraged to participate by opening issues for bugs or feature requests and submitting pull requests with your improvements or fixes. Your contributions help enhance and grow the project, making it better for everyone.


### Contact

- For any questions or feedback, please reach out to me at roni.cse@gmail.com. I welcome all inquiries and look forward to hearing from you. Your input is valuable and appreciated!


