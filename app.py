# imports
from exp.indeed_to_mongo import *
from exp.push_to_board import *
from flask import Flask, request
from pymongo import MongoClient
import json

# connecting to our collections and db
client = MongoClient('mongodb+srv://test:test@cluster0-ehci6.mongodb.net/test?retryWrites=true&w=majority')
db = client.get_database('Job_Scraper')

# pulling from records
records = db.Scraped_Jobs

# pushing to postings
postings = db.Postings

# instantiating our app
app = Flask(__name__)

# scraping_to_db route
@app.route('/scrape/<what>/<location>', methods=['GET'])
def scrape_to_db(what, location):
    
    # 1. Grabbing url
    url = get_indeed_url_(what, location)
    
    # 2. grabbing our parased data from indeed
    data = parse_indeed_(url)
    
    # 3. converting to DF
    # we will use DF for c-time normalization of data
    df = data_to_df(data)
    
    # 4. sorting by date posted
    convert_dates_(df)
    
    # 5. Drop duplicates
    df.drop_duplicates(inplace=True)
    
    # 6. Reset index and drop index column
    df.reset_index(inplace=True)
    df.drop('index', axis=1, inplace=True)

    try:
        # 7. Push to our db: MongoDB
        push_to_mongo(df, records)
    
        # return response
        return json.dumps({'title search': what, 'location search': location, 'status': '200: pushed to db'})
    
    except:
        return json.dump({'status': '400: error occured check logs.'})
    
# push_to_postings route
@app.route('/push_to_posting/<what>/<amount>', methods=['GET'])
def push_to_postings(what, amount):
    
    amount = int(amount)
    
    # 1. finding matches
    # finding matches in the db based on user input
    values = find_values_(what, records)
    
    # 2. Finding best matches
    # we are using fuzzy search to return the best
    # mathces, returned in DF format
    matches = find_best_match(what, values)
    
    try:
        # 3. posting to the board
        # will be posting to our posting collection for now
        post_to_board(matches, postings, amount)
        
        return json.dumps({'job type posted': what, 'amount posted to postings': amount, 'status': '200: posted on job board'})
    
    except:
        return json.dumps({'status': '400: error occured check logs', 'what': what, 'amount': amount})

    
if __name__  == "__main__":
    app.run(debug=False)