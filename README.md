# Job Scraper Gold 
This repository contains the creation and script ```app.py``` of an agnostic job scraper. At the current moment, this sraper will only get jobs from indeed and will post them to ```postings``` which is to represent a jobs board API. 

The entire application works as a back-end API and is split to two functonal routes: 
```/scrape/<what>/<location>``` where ```what``` where represent the type of job to scrape. ```location``` will represent where to search for those jobs in geographic sense. 

The other functional route is ```push_to_posting/<what>/<amount>``` which will search the post-scraped DB for ```what``` job you are searching for. and will push onto ```postings``` collection which represents an actual job board. 

We've implmented fuzzy search to find the best match. 

## Installing
To first install clone this repository. 

Run 
```
pip install requirements.txt
``` 
to install appropriate libraries and packages

## Running app
To simply run the app Run:
```
python app.py
```

This will start the flask app and run the server on localhost. 

Then you will be prompted to use the following routes:
* ```/scrape/<what>/<location>```
    * This will scape jobs from indeed and post them to our DB
* ```push_to_postings/<what>/<amount>```
    * This will search for matching jobs and post them to a job board | which is a DB collection for this version