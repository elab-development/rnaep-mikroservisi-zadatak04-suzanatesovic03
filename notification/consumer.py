import time
from database import redis

key_completed = 'order_completed'
key_refund = 'refund_order'
group = 'notification-group'

try:
    redis.xgroup_create(key_completed, group, mkstream=True)
except:
    print('Group already exists for order_completed!')

try:
    redis.xgroup_create(key_refund, group, mkstream=True)
except:
    print('Group already exists for refund_order!')

while True:
    try:
        results = redis.xreadgroup(group, group, {key_completed: '>', key_refund: '>'}, count=1, block=5000)

        if results:
            for result in results:
                stream_name = result[0]
                obj = result[1][0][1]

                if stream_name == key_completed:
                    print(f"Obaveštenje: Porudžbina {obj.get('pk', '?')} je uspešno kreirana i plaćena!")
                elif stream_name == key_refund:
                    print(f"Obaveštenje: Porudžbina {obj.get('pk', '?')} je refundirana!")

    except Exception as e:
        print(f"Consumer error: {e}")
    
    time.sleep(1)