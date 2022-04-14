## OVERVIEW

This README contains information about the scraping and data engineering homework challenges. The two challenges have been developed separately and come with separate docker images. 

### Scraping part
The goal of this task was to scrape real estate listings from Immowelt API based on the given parameters and store the results into a json file. In order to do this, we first had to obtain a session access token from https://api.immowelt.com/auth/oauth/token. For this purpose we built ImmoweltAccessToken that returns the token along with its expiration time. This token is being used by the search_listings() function that reads search parameters (distribution type, estate type, location ids, etc) from a configuration file and returns the corresponding data. Users can easily adjust their search by changing the search parameters. The output file is then being stored in the output directory. In order not to overwhelm the API with requests, we are calling 1000 pages per request and with the help of time.sleep() function we make a break between each call. 

Aside from this base functionality that is being executed once and that returns a file, we can also run our programm in a scheduled mode that stores the output results into the MongoDB database. The idea behind this functionality was to demonstrate how repetitive tasks could be executed. In order to run the program in scheduled mode, you need to add -s command into the docker-compose file, which would be explained further in the Instructions section.

 
  
### Data enginering
The goal of this task was to find duplicate real estate listings between and within different platform files. Files were provided in jsonl format which required of us to load them in a different manner than a json file would be loaded (first we read the file and put it in a list and then we iterate over each element of the list and cast it into a dictionary with json.loads() and then append them to a final list). Files were stored in the files directory (the directory from which we are reading files could be changed by issuing a command in docker-compose file). We iterate over all the files in the directory and then read them one by one and concatenate them into a single dataframe. During this process we also add a platform column (file name without the extension) which helps us identify from which source each row came. 
 
In the next step we look for the duplicates. It is important to point out that after we analyzed the data, we realized that there is no real primary_key column combination and that we couldn't possibly identify all the duplicates without either missing some duplicates or identifying false duplicates. For that reason, we chose a combination of 6 key columns that could get us close to the desired results: key_columns = ['living_space','floor', 'rooms', 'zip_code', 'sale_type', 'price']. Those columns are being loaded from the configuration file which allows users to change their combination and that way include or exclude some possible duplicate listings. For example, if we included title or description fields in key_columns list, we would drop some false duplicates but would lose those real duplicates that have different titles and descriptions. Also, we decided to drop those rows that contain a lot of NaN values in key_columns (at least 4), because for those records it is impossible to tell if they are duplicates or not. 

After we create a dataframe with duplicate listings, we create a single key column (combination of key columns) that has a shared value between the duplicates and acts as a pivot point. With pandas groupby() function we are then able to create small subsets based on unique key values and then parse them from dataframe into a list of dictionaries. The endput result is then stored in a json file. 

Once again, it is important to point out that we are aware of inaccuracy in the output results. Adding home address and number to the files would be a solution to this issue as they represent try unique identifiers of a real estate listing. 



## Instructions

### Task1
1. Go to the crawling directory.
2. In docker-compose.yaml set IMMOWELT_KEY value ('authorization' token that is being posted to https://api.immowelt.com/auth/oauth/token to generate token, without the word Basic).
3. Under commands, if -s argument is passed and is set to 300, it means that the program will be scheduled to run and will run every 5 minutes. To execute the script only once just remove -s argument. If running on linux, uncomment the code on line 9, user: '1000:1000', which would then set Docker linux user to your local user, not root.
4. From the crawling directory run  `docker-compose build` and wait for the images to be built (python, mongo, mongo-express).
5. Run `docker-compose up` to start the containers. If the service runs in scheduled mode (with parameter -s), you can go to the mongo-express client in your browser (localhost:8081) and see the database (crawling) and the data collection (EstateSearch). This serves only for testing purposes since the mongo-express client is acting very slow and for that reason we recommend that you slice the list sent to MongoDB (line 41 in scrape.py).
6. If service runs in schedule mode, stop the program by pressing ctrl+c

### Task2
1. Go to the data_engineering directory.
2. From there run `docker-compose build`. Since the pandas package comes with a lot of dependencies, running this command for the first time can take more than 10 minutes to download and install all the packages.
3. Run `docker-compose up`
4. Output file will be saved in the output directory. 



## Future suggestions
For the first task (crawling) we should implement a function that checks if the token has expired and then to use the old one if it is still active or generate a new one if not. With the current solution we are requesting a new token for each run.

For the second task, we should try and bring additional columns that could help to more accurately identify duplicates (e.g. home number and address) through scraping links provided or through joining the data with additional data collections available that could potentially have more information. 
