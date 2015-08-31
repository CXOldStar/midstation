# -*- coding: utf-8 -*-
__author__ = 'qitian'
from threading import Thread
from random import randint
from midstation.user.models import Order, Button, Service, User
import time
from datetime import datetime


def get_received_messages(sleep=5):
    '''
    module message for testing
    :return:
    '''
    while(True):
        node_id = '111111'
        button = Button.query.filter_by(node_id=node_id).first()
        if button:
            order = Order()
            create_time = datetime.strptime('2015-08-31 11:30:00', '%Y-%m-%d %H:%M:%S')
            order_exit = Order.query.filter_by(button_id=button.id, create_time=create_time).first()
            if not order_exit:
                print 'Save Order'
                order.save(button, create_time=create_time)
                print 'Sent Message to WeChat'
            else:
                print 'Order exit'
        time.sleep(randint(2, 20))
        print '%s' % time.strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    get_received_messages()