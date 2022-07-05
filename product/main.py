from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()
#Middleware is software that enables one or more kinds of communication or connectivity 
# between two or more applications or application components in a distributed network. 
# By making it easier to connect applications that weren't designed to connect with one another - 
# and providing functionality to connect them in intelligent ways
#  - middleware streamlines application development and speeds time to market.

app.add_middleware(
    #services running at different ports, browser doesnt allow to request 
    #different ports so CORS means that problem
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="redis-17995.c273.us-east-1-2.ec2.cloud.redislabs.com",
    port=17995,
    password="UGxm99ceFQv1iKcIJ91Y5RHae7wcaZ6W",
    decode_responses=True
)


class Product(HashModel): #database model for the product details 
    name: str
    price: float
    quantity: int
 
    class Meta:  #defined databse
        database = redis


@app.get('/products') #get request to products  pulls the data and shows when user visit that url
def all():
    return [format(pk) for pk in Product.all_pks()] #function that returns all the primary keys


def format(pk: str): #primary keys is passed 
    product = Product.get(pk) #fetched items from that primary key of Product model from the database

    return {
        'id': product.pk, #returned the value of respective attributes 
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }


@app.post('/products') #post method to create Product instances
def create(product: Product):  #passed Product class itself as parameter so post will allow to create its attributes 
    return product.save()

#delete functionality 
@app.get('/products/{pk}')
def get(pk: str):#it fetches the items from primary key of database table  in order to delete the items  
    return Product.get(pk)


@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)