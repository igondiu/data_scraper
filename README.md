# Data scraper
Data scraper is a module made to scrap data from an input csv file and insert it into a MySQL database.
The project is made to be run on a Docker container.


### To run the project :  
Flask is using PORT 5000, make sure that the port is not already in use    
* 1 : Open to the folder `data_scraper` in a terminal window

* 2 : Copy and past this shell command in the terminal window :
`docker-compose -f devops/docker_compose_data_scraper.yml up --build`  
If everything went good you should see something similar to this in your terminal window : 
![alt text](img/TERMINAL_RESULT.png?raw=true "Terminal result")

* 3 : It's time to open the Swagger ! (API's documentation)   
Copy and paste this link into your web browser : `http://0.0.0.0:5000/doc`
The swagger must open in your web browser : 
![alt text](img/SWAGGER.png?raw=true "Terminal result")


### Test the module :

* 1 : Use the first endpoint to post a file to the module, it will take the data from the input file and insert into the MySQL database  
The file is located in the folder `data_scraper/tests/test_data/data_for_tests.csv`

* 2 : Use the second endpoint to check if the data was correctly inserted into MySQL database  
4 arguments are required to be able to get data :  
**MCC**  
**Net**   
**Area**   
**Cell** 

To be sure to retrieve at least one row from the database use this :  
`MCC = 270`  
`Net = 99`  
`Area = 12`  
`Cell = 22222`  

#### Test the module with `curl` :  
Go to the folder where the CSV file is located using `cd` bash command
* 1 To populate database with data from the CSV file use this bash command :  
`curl -X POST "http://localhost:5000/test_upciti/api/v1/populate_db" -F "file=@data_for_tests.csv"`

* 2 To get the data from the database use this bash command :  
`curl -X GET "http://localhost:5000/test_upciti/api/v1/get_cell_towers/270&99&1&531"`

#### Test the module using pytest :  
Unit tests are available in the folder `tests/unit/test_api.py`  
**Be sure that the docker container is running**  
Open a terminal window and go to the root directory of the project (/data_scraper)  
Copy and paste this bash command in your terminal window :  
`pytest --cov-report html --durations=0 --cov=lib --cov=src tests/unit/`



### Logs
Logs are available in the folder `data_scraper/logs`  
If something doesn't work as expected you can consult the logs