# The Common `$regex` Anti-Pattern

If you are building a full-text search app with MongoDB and use a case-insensitive regex, stop and re-consider. You are probably paying for it in many ways, over-consumption of resources, angry customers, and more. Spin up a cluster on Atlas and create a Search Index on <a href="https://docs.atlas.mongodb.com/atlas-search?utm_source=regex_replacement" target="_blank">MongoDB Atlas Search</a> with the click of a button.

## About this Project


This project is actually a very simple fork of an existing project where someone built a full-text search app in MongoDB using case-insensitive regex. Going forward, case-insensitive regex queries to power full-text search should be considered an anti-pattern. This repo is not an axample of how to build a Flask App. In fact, it is simply a fork of another blog post, revised to use Atlas Search and demonstrate how you could immediately get value from a small refactor to move case-insensitive regex to Atlas Search.

This revised repo is meant to demonstrate the many benefits of moving most case-insentive regex queries (`$regex`) in MongoDB Atlas to <a href="https://docs.atlas.mongodb.com/atlas-search" target="_blank">MongoDB Atlas Search</a>, a Lucene-powered search engine built for the job. After a list of benefits, there's a tutorial below, along with some sample code in this repo. You can find the regex query code in the `regex_version` branch, and the Atlas Search code in the `fts_version` branch.

### The Benefits of `$search` Compared to `$regex`:


* _Resource consumption_ - case-insensitive regex queries are expensive in any database engine. If you run them often and on even a modest dataset, e.g. ~50,000 documents, you will start to see performance hits on those queries and others. Atlas Search runs as a separate process in your replica set, `mongot`, so your workload can continue per usual without unnecessary disruption from a computationally expensive query shape. 

* _Speed_ - case-insensitive queries hurt the user experience of your application because they can be very slow. With Atlas Search, most queries are faster the first time, and almost all identical queries are faster because we can cache queries.  

* _Autocomplete_ - users have grown accustomed to autcomplete in the search box. While you could hack together autocomplete for a case-insensitive regex queries, they would be slow, often inaccurate, and prohibitively expensive. 

* _Fuzzy matching_ - typos are frequent, especially on those tiny mobile keyboards. Rest assured that if your user types a query with a typo, relevant results are still returned. 

* _Diacritic folding_ - again, I am sure there is a way to do this with case-insensitive regex, but it cannot be as easy or predictable at it is in Atlas Search. There, you just need to include a boolean variable for the foldDiacritics `variable` in your index definition.

* _Many search operators_ - perhaps the best feature you get from Atlas Search when compared to case-insensitive regex queries would be the collection of <a href="https://docs.atlas.mongodb.com/atlas-search?utm_source=regex_replacement" target="_blank">search operators</a>. With them, you can craft a search experience that truly captures your user's intent.


# Building the App

- note: this is a restaurant finder flask, mongodb and leaflet js tutorial forked another, somewhat incomplete tutorial. These instructions were developed on Mac OS X, but they should work on Unix systems. If you are here to compare the search functionality of `$regex` to `$search`, I recommend you set up the project using the instructions seen below because it will be challenging for some to get set up unless you are experienced with wrestling your Python environments on Mac OS X.

1. Clone this repo, cd into the project, and checkout the `regex_version` branch.

  `cd Flask_Tuts`

2. Create and activate a virtual Environment.

  `python3 -m venv mongo_atlas_regex_bad/`

  `source mongo_atlas_regex_bad/bin/activate`

3. Install the dependencies to run the app.

`pip install -r requirements.txt`

4. Add your credentials to line 15 of `app.py`.

* It should look something like this: 

`db = pymongo.MongoClient("mongodb+srv://marcustest:<password>@connection_string.mongodb.net/?retryWrites=true&w=majority").sample_restaurants`

5. If you have not previously created an Atlas Cluster, create one <a href="https://www.mongodb.com/cloud/atlas?utm_source=regex_replacement" target="_blank">here</a>. You should copy two versions of the connection string. You will need one for Compass and a slightly different one for connecting your application.

6. Load the <a href="https://raw.githubusercontent.com/mongodb/docs-assets/geospatial/restaurants.json" target="_blank">sample data</a> into the cluster using [Compass](https://www.mongodb.com/products/compass) or the Mongo Shell.

7. Configure the Flask runtime environment and run the app.

`FLASK_ENVIRONMENT=development` 

`flask run`

8. Visit http://127.0.0.1:5000 in the browser and try out the search. 


This should work fine but what about typo tolerance? Or, if you were to add 5 million more restaurants, speed? Your clusters are hurting from this experience and they should really move to the MongoDB product that is designed for the job. 



