from celery import shared_task
import time
@shared_task
def add(x, y):
    print('Task is running...')
    time.sleep(10)
    print('Task is done')
    print('x:', x)
    print('y:', y)
    print('x + y:', x + y)
    return x + y