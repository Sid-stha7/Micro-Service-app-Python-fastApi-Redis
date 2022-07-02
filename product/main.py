from base64 import decode
from dbm import _Database
from http.client import responses
from typing import Union
from webbrowser import get
from fastapi import FastAPI
import redis
from redis_om import get_redis_connection
app = FastAPI()

redis = get_redis_connection(
    host= "redis-17800.c252.ap-southeast-1-1.ec2.cloud.redislabs.com",
    port= 17800,
    password="esA0v5XkKAUQtMmliPvUXPjOX38YQIvu",
    decode_responses=True
)

class Product(HashModel): #database model for the product details 
    name :str
    price : float
    quantity_available: int

    class Meta: #defined databse
        database= redis

@app.get pr 
deff all():