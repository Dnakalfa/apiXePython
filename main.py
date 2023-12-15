from secrets_1 import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET
from fastapi import FastAPI
from pyparsing import Any, List, Literal
import tweepy
from pymongo import MongoClient
import uvicorn
from pydantic import BaseModel


client = MongoClient('mongodb://localhost:27017')
db = client.my_arquivo
trends_collection = db.trends

class TrendIten(BaseModel):
    name: str
    url: str
    
BRAZIL_WOE_ID = 23424768

def get_trends(woe_id: int) -> List[dict[Literal, Any]]:
    
    
    auth = tweepy.OAuthHandler(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    trends = api.get_place_trends(woe_id)
    
    return trends[0]["trends"]

app = FastAPI()

@app.get("/trends", response_model=List[TrendIten])
def get_trends_route():
    trends = trends_collection.find({})
    return list(trends)


if __name__ == "__main__":
    trends = trends_collection.find({})
    
    if not list(trends):
        trends = get_trends(woe_id=BRAZIL_WOE_ID)
        trends_collection.insert_many(trends)
        
    uvicorn.run(app, host="0.0.0.0", port=8000)