from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests, time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

# This should be a different database
redis = get_redis_connection(
    host="redis-17995.c273.us-east-1-2.ec2.cloud.redislabs.com",
    port=17995,
    password="UGxm99ceFQv1iKcIJ91Y5RHae7wcaZ6W",
    decode_responses=True
)


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  #options: pending , completed ,shipped, refunded

    class Meta:
        database = redis


@app.get('/orders/{pk}')
def get(pk: str):
    order= Order.get(pk)
    redis.xadd('refund_order', order.dict(), '*')
    
    return order


#here we will be dealing with the problem of microservice , we will 
#have to request the product details directly with our product app/microservice
#this asunc function will run seperately not with the main app so it gets the data from request
#id , quantity from id we will get all the product information
@app.post('/orders')
async def create(request: Request, background_tasks: BackgroundTasks):  # id, quantity
    body = await request.json()#getting data thats in request

    req = requests.get('http://localhost:8000/products/%s' % body['id'])#the id is string so from the body id the %s will be replaced with the string id fetched from body
    product = req.json() 

#now we will be creating the order from customer of that Order class we made up
    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=0.2 * product['price'],
        total=1.2 * product['price'],
        quantity=body['quantity'],
        status='pending'
    )
   
    background_tasks.add_task(order_completed, order)
    order.save()
    return order


def order_completed(order: Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()
    redis.xadd('order_completed', order.dict(), '*')
    #send order dictionary
    #now when order is completed we have to deduct the item number from our inventotry 
    #we will use redis stream to send events . it is a messaging event pass
    #key is order_completed and order is passed as dictionary and the star represents the id of the messeage 
    #we are sending