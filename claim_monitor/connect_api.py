# API CONNECTOR
# ----------------------------------------------------------------------

import cl_utils as u
import requests
import os
import json

def auth():
    return os.environ.get("BEARER_TOKEN")

def createQuery(author):
    # Function that takes an author for a Twitter account
    # returns query including one or more keywords from the file keywords.txt.
    # becarefull that len(query) is inferior to 1024
    listKeywords = u.keywords("data/keywords.txt")
    query =  "from:"+ author + " ("+ listKeywords[0]
    for i in range(len(listKeywords)-1):
        query = query + ' OR ' + listKeywords[i+1] 
    return query +")"

def create_url(author,nbtweets,date):
    query = createQuery(author)
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    tweet_fields = "tweet.fields=id,created_at"
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&start_time={}&max_results={}".format(
        query,tweet_fields,date,nbtweets
    )
    return url

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print("API status code:", response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()
