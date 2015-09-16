# -*- coding: utf-8 -*-
'''
日期：20150908
功能：打印所有基站最新的一条消息。可以通过修改gateway_mac来增加基站。
特点：利用map()实现并发。
'''
import requests
import json
import datetime
import sys
from functools import partial
import time
import pprint
import datetime
import time
import os
from midstation.configs.default import DefaultConfig as Config
from midstation.button.models import Message
from midstation.user.models import User, Button
import json
from wechat_sdk import WechatBasic
from midstation.user.models import Order, create_order
import requests


gateway_mac = ["000db93db79c", "000db93db700", "000db93db804", "000db93db7c0", "000db93db6f8", '000db93db784']
GATEWAY_ID = ["a2d790e1-1670-1217-0000-" + mac for mac in gateway_mac]

ORGANIZATION = "niot"
USERNAME = "niot.user"
PASSWORD = "Ni0t!0715"

NUM_MINUTES_BACK = 1


def detect_button_events(interval=5):
    """
    get messages sent from buttons
    :param interval:
    :return:
    """
    if GATEWAY_ID == '' or ORGANIZATION == '' or USERNAME == '' or PASSWORD == '':
        print ('Please fill out your username, password, and gateway ID in the script')
        return

    try:
        while True:
            data = get_received_messages(ORGANIZATION, GATEWAY_ID, USERNAME, PASSWORD, 2*60)
            if data:
                for event in data:
                    datas = event["events"]
                    for d in event['events']:
                        eventUUID = d['networkMessage']['routerMetadata']['eventUUID']
                        node_id = d['networkMessage']['nodeMetadata']['nodeId']
                        receipt_time = d['networkMessage']['routerMetadata']['receiptTime']

                        # change to datatime object
                        receipt_time = receipt_time[:8] + receipt_time[9:15]
                        receipt_time = datetime.datetime.strptime(receipt_time, '%Y%m%d%H%M%S')

                        # 判断是否已经处理过了
                        msg = Message.query.filter_by(eventUUID=eventUUID).first()
                        if not msg:
                            message = Message(eventUUID=eventUUID, node_id=node_id, receipt_time=receipt_time)
                            message.save()

                            # 发送微信消息
                            send_wechat(node_id)
                            # 创建订单
                            create_order(node_id)
                            # TODO:发送确认消息
                            send_command(USERNAME, PASSWORD, GATEWAY_ID, node_id, '0XFF')

            time.sleep(interval)

    except KeyboardInterrupt:
        os.exit()

# 发送微信消息
def send_wechat(node_id):
    button = Button.query.filter_by(node_id=node_id).first()
    if button:
        wechat_id = button.user.wechat_id
        template_id = button.service.wechat_template_id

    # wechat = WechatBasic(token='midstation', appid='wx6b84ff9cb6f9a54e', appsecret='4e09e5b35198bdbf35b90a65d5f76af4')
    wechat = WechatBasic(token=Config.WECHAT_TOKEN, appid=Config.WECHAT_APPID, appsecret=Config.WECHAT_APPSECRET)

    data = {}
    # res = wechat.send_template_message(user_id=wechat_id,
    #                              template_id=template_id, data=data)
    res = wechat.send_template_message(user_id='o5lpBuCdBW7HABytpcAbMy3QbBPs',
                                 template_id='grsshOaPw-0pCrkdZwjOS4Mr4AaQQVteEG-2R_RK6BY', data=data)
    if res['errcode']:
        raise Exception('Send wechat message failed')


# 发送成功消息
def send_command(username, password, target_gateway_id, target_node_id, payload_hex, needs_ack=False):
    """
    Sends a message to a node through a specified gateway
    The gateway and node ids must be strings
    Returns the command id, or None if the send was unsuccessful
    """
    command_url = 'https://ingest.link-labs.com/api/command/Gateway/' + target_gateway_id
    command_headers = {'content-type': 'application/json', 'Accept': 'application/json'}

    target_node_id_hex = '{0:x}'.format(target_node_id & int('1' * 36, 2))
    cmd_data = {'commandType': target_node_id_hex + ':' + ('Ack' if needs_ack else 'NoAck'),
                'payloadHex': payload_hex}
    auth = requests.auth.HTTPBasicAuth(username, password)
    response = requests.post(command_url, json.dumps(cmd_data), verify=False,
                             headers=command_headers, auth=auth)
    if response.status_code == requests.codes['created']:
        return json.loads(response.text)['commandId']
    else:
        raise RuntimeError(response.reason)



def get_received_messages(organization, gateway_id, username, password, num_minutes_back):
    urls = build_urls(organization, gateway_id, num_minutes_back)
    auth = requests.auth.HTTPBasicAuth(username, password)
    data = []

    req_get = partial(requests.get, verify=False, auth=auth)
    resp = map(req_get, urls)

    for i in resp:
        if i.status_code == requests.codes['ok']:
            data.append(json.loads(i.content.decode()))

    return data


def build_urls(organization, gateway_id, num_minutes_back):
    url_base = 'https://dataaccess.link-labs.com/data/dataFlow/' + organization + '/gateway/'
    curr_time = get_current_time()
    return [(url_base + ident + '/events/timeRange?refTime=' +\
        curr_time + '&minsBack=' + str(num_minutes_back)) for ident in gateway_id]


def get_current_time():
    return datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%S.%f')[:-3]

if __name__ == "__main__":
    pass
