# Data scraper
Data scraper is a module made to scrap data from an input csv file and insert it into a MySQL database.
The project is made to be run on a Docker container.


### To run the project :   
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
4 Arguments are required to be able to get data : 
MCC
Net  
Area  
Cell

To be sure to retrieve at least one row from the database use this :  
`MCC = 270`  
`Net = 99`  
`Area = 12`  
`Cell = 22222`  


### Logs
Logs are available in the folder `data_scraper/logs`  
If something doesn't work as expected you can consult the logs