from main import redis, Product
import time

key = 'order_completed'
group = 'product-group'

try:
    redis.xgroup_create(key, group) #created a group with key and group name
except:
    print('Group already exists!')

while True:
    try:
        results = redis.xreadgroup(group, key, {key: '>'}, None)

        if results != []:
            for result in results:
                obj = result[1][0][1]
                try:
                    product = Product.get(obj['product_id'])
                    product.quantity = product.quantity - int(obj['quantity'])
                    product.save()
                except:
                    redis.xadd('refund_order', obj, '*')
                    #if the product was deleted wwhile waiting for 5 sec the 
                    #email will be send as refunded to customer 
                    #now when order is completed we have to deduct the item number from our inventotry 
                    #we will use redis stream to send events . it is a messaging event pass

    except Exception as e:
        print(str(e))
    time.sleep(1)