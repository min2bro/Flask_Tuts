# The Common `$regex` Anti-Pattern

If you are building a full-text search app with MongoDB and use a case-insensitive regex, stop and re-consider MongoDB Atlas Search. You are probably paying for it in many ways, over-consumption of resources, angry customers, and more. Spin up a cluster on Atlas and create a Search Index on <a href="https://docs.atlas.mongodb.com/atlas-search?utm_source=regex_replacement" target="_blank">MongoDB Atlas Search</a> with the click of a button.

## About this Project

This project is actually a very simple fork of an existing project and blogpost where someone built a full-text search app in MongoDB using case-insensitive regex. Going forward, case-insensitive regex queries to power full-text search should be considered an anti-pattern. This repo is not an example of how to build a Flask App. Lots of the code could be improved. I read a blogpost about a search app built using $regex in and revised it to use Atlas Search. Hopefully this README makes it it easy to see how you could immediately get value from a small refactor to move case-insensitive regex to Atlas Search.

This revised repo is meant to demonstrate a few of the many benefits of moving most case-insentive regex queries (`$regex`) in MongoDB Atlas to <a href="https://docs.atlas.mongodb.com/atlas-search" target="_blank">MongoDB Atlas Search</a>, a Lucene-powered search engine built for the job. After a list of benefits, there's a tutorial below, along with some sample code in this repo. You can find the regex query code in the `regex_version` branch, and the Atlas Search code in the `fts_version` branch.

Here's a picture of an Atlas Search fuzzy match, which would be exceedingly difficult and expensive to set up using the case-insenentive regex query shape. Apparently, there are lots of bagels near the MongoDB HQ:
<br/>
<br/>
<img src="https://user-images.githubusercontent.com/2353608/100299681-18324d80-2f49-11eb-9d9f-bb0bd8b84827.png" alt="Image of Atlas Search Fuzzy Match" width="800" height="600">

## The Benefits of `$search` Compared to `$regex`:


* _Resource consumption_ - case-insensitive regex queries are expensive in any database engine. If you run them often and on even a modest dataset, e.g. ~50,000 documents, you will start to see performance hits on those queries and others. Atlas Search runs as a separate process in your replica set, `mongot`, so your workload can continue per usual without unnecessary disruption from a computationally expensive query shape. 

* _Speed_ - case-insensitive queries hurt the user experience of your application because they can be very slow. Atlas Search is built on Apache Lucene and optimized for the text search use case in ways that a database cannot be.

* _Autocomplete_ - users have grown accustomed to autcomplete in the search box. While you could hack together autocomplete for a case-insensitive regex queries, they would be slow, often inaccurate, and prohibitively expensive. I don't demonstrate that in this blogpost.

* _Fuzzy matching_ - typos are frequent, especially on those tiny mobile keyboards. Rest assured that if your user types a query with a typo, relevant results are still returned. 

* _Diacritic folding_ - again, I am sure there is a way to do this with case-insensitive regex, but it cannot be as easy or predictable at it is in Atlas Search. There, you just need to include a boolean variable for the `foldDiacritics` variable in your index definition.

* _Many search operators_ - perhaps the best feature you get from Atlas Search when compared to case-insensitive regex queries would be the collection of <a href="https://docs.atlas.mongodb.com/atlas-search?utm_source=regex_replacement" target="_blank">search operators</a>. With them, you can craft a search experience that truly captures your user's intent.


# Building the App

- note: this is a restaurant finder flask, mongodb and leaflet js tutorial forked another, somewhat incomplete tutorial. These instructions were developed on Mac OS X, but they should work on Unix systems. If you are here to compare the search functionality of `$regex` to `$search`, I recommend you set up the project using the instructions seen below because it will be challenging for some to get set up unless you are experienced with wrestling your Python environments on Mac OS X.

### Pre-Requisites:

-   At Atlas Cluster. If you don't have one, you can create one create one <a href="https://www.mongodb.com/cloud/atlas?utm_source=regex_replacement" target="_blank">here</a>.
*  Two versions of the connection string: (1) for Compass and (2) for Python Applications

1. Clone this repo, cd into the project.

  `cd Flask_Tuts`


2. Create and activate a virtual Environment.

  `python3 -m venv mongo_atlas_regex_bad/`

  `source mongo_atlas_regex_bad/bin/activate`

3. Install the dependencies to run the app.

`pip install -r requirements.txt`

4. Checkout the `regex_version` branch of the repo.

`git checkout regex_version`

5. Add your connection string to a file in the root project called `config.json`.

* It should look something like this: 

`{
  "ATLAS_URI": "mongodb+srv://<db_user>:<db_password>@cluster0.xh91t.mongodb.net/?retryWrites=true&w=majority"
}`

6. Load the <a href="https://raw.githubusercontent.com/mongodb/docs-assets/geospatial/restaurants.json" target="_blank">sample data</a> into the cluster using [Compass](https://www.mongodb.com/products/compass) or the Mongo Shell.

7. Configure the Flask runtime environment and run the app.

`FLASK_ENVIRONMENT=development` 

`flask run`

8. Visit http://127.0.0.1:5000 in the browser and try out the search. Feel free to use your own query but for a consistent comparison, try entering `kentucky` in the name field, `10451` in the zip field, and `5` in the radius field then clicking `Submit`.

This should work fine but what about typo tolerance? Try the same query, except this time change the name input from `kentucky` to `kentucke`.efore clicking submit, click the clear results button in the bottom right of the map. No results. 

If you were to add one million more restaurants, the query would be too slow to be usable. Your clusters are hurting from this experience and they should really move to the MongoDB product that is designed for the job. To replace the search experience with Atlas Search, let's checkout the `fts_version` branch of this repo:

`git checkout fts_version`.

9. Head to the restaurants collection in Atlas and create a search index with the button on the far right side of the screen.

[helpful gif coming soon]

### An Example Search Index Definition

There are many variations of a search index definition that you could use, but here is one to start:

```javascript
// index name: rest_fts_sample

{
  "mappings": {
    "dynamic": false,
    "fields": {
      "address":{
        "type": "document",
        "fields":{
            "coord":{
                "indexShapes": false,
                "type": "geo"
                }
        }
      },
      "name": {
        "analyzer": "lucene.standard",
        "type": "string"
      }
    }
  }
}
```

Here is the autocomplete index definition used in the project 

```javascript

// index name: rest_name_autocomplete_sample

{
  "mappings": {
    "dynamic": false,
    "fields": {
      "address.coord": {
        "indexShapes": false,
        "type": "geo"
      },
      "name": [
        {
          "foldDiacritics": true,
          "maxGrams": 15,
          "minGrams": 2,
          "tokenization": "edgeGram",
          "type": "autocomplete"
        }
      ]
    }
  }
}
```


10. Add the credentials from step 5, althogh the connection code will look slightly different and like this:

`db = pymongo.MongoClient("mongodb+srv://<username>:<password>@connection_string.mongodb.net/?retryWrites=true&w=majority").sample_restaurants`

11. Run the app again.

`flask run`

12. Again, visit http://127.0.0.1:5000 in the browser and try out the search. Feel free to use your own query but for a consistent comparison, try entering `kentucky` in the name field, `10451` in the zip field, and `5` in the radius field then clicking `Submit`. Now, the greater number of results isn't totally due to Atlas Search's superioirity for the search use case, though one could argue.<sup>1</sup> If you want to be underwhelmed, `git checkout regex_version` and try it again. 


Try the `kentucke` search again. This, time, all the same results show up as in the previous correctly spelled search. That's because of the fuzzy parameter for the text operator.

For reference, here are the two very similar though not identical queries, with the clear winner in terms of performance, customizability, and user experience on the left:


<table>
  <tr>
    <th>MongoDB Atlas Search</th>
    <th>Case-Insensitive Regex</th>
  </tr>
  <tr>
    <td>Typical GeoJSON Search Query</td>
    <td>Original GeoJSON Regex Query</td>
  </tr>
  <tr>
    <td class="highlight highlight-source-js">
<pre>
        { 
          "$search": { 
            "index": "rest_fts_sample",
            "compound":  { 
              "must": { 
                "text": { 
                  "query": restname, 
                  "path": "name", 
                  "fuzzy": { 
                    "maxEdits":2
                } } },
              "should": { 
                "near": { 
                  "origin": { 
                    "type": "Point",
                    "coordinates": [ lat, lon ] 
                    }, 
                  "pivot": int(rad) * METERS_PER_MILE, 
                  "path": "address.coord"     
            } } } } }
    </pre>
</td>
<td class="highlight highlight-source-js">  

        {
          "address.coord": { 
            "$nearSphere": { 
              "$geometry": { 
                "type": "Point", 
                "coordinates": [ lon, lat ] 
                }, 
              "$maxDistance": int(rad) * METERS_PER_MILE 
              } },
            "name": {
              "$regex": restname, 
              "$options" : "i"
          } }
</td>
  </tr>
  <tr>
    
  </tr>
</table>
<br/>

There's a lot more room for customization and improvement in this example, but this is an introduction into how you could use MongoDB Atlas Search to replace the case-insensitive `$regex` anti-pattern. I hope you enjoy. If you have any improvements to this repo, or want to share an index that you built with Atlas Search, please feel free to open a PR. I want to incorporate as much feedback as possible so that the MongoDB database can continue to free developers from the constraints of `sq`ueezal`l`.


#### Footnote

1. We could make the compound operator filter out results that are farther than the desired radius. The reason for this result set is due to the fact that location here is a score factor, not a filter factor. Most search engines use location in this manner to start and offer users the option to filter out results greater than a certain distance away from a point of interest. 


