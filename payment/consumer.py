from main import redis, Order
import time

key = 'refund_order'
group = 'payment-group'

try:
    redis.xgroup_create(key, group)#created a group with key and group
except:
    print('Group already exists!')

while True:
    try:
        results = redis.xreadgroup(group, key, {key: '>'}, None)

        if results != []:
            print(results)
            for result in results:
                obj = result[1][0][1]
                order = Order.get(obj['pk'])
                order.status = 'refunded'
                order.save()
                #if the product was deleted wwhile waiting for 5 sec the 
                #email will be send as refunded to customer 
    except Exception as e:
        print(str(e))
    time.sleep(1)