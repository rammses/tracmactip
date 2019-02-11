#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Facts retriever
- Gets device facts form junos device using keypair authentication method
"""
__author__ = "Mesut Bayrak 'Rammses' "
__copyright__ = "Copyright 2016, ISTANBUL"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Mesut Bayrak"
__email__ = "mesut@mikronet.net"
__status__ = "Beta "

import sys
import os
import datetime
import threading
import requests
import csv
import yaml
import time
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.factory.factory_loader import FactoryLoader


def name_details(text):
    """ Name Parser
    - Parses info from a dash limited string
    - Sample string T3-BK-DK1-VC1"
    -               |  |  |   |
    -               |  |  |   ---- Virtula Chasis No
    -               |  |  -------- Data Cabinet no
    -               |  ----------- Floor
    -                ------------- Geographic location
    """
    try:
        text1 = text.split('-')
        s_geo = text1[0]
        s_floor = text1[1]
        s_datacabinet = text1[2]
        s_vc = text1[3]
    except:
        s_geo = "Can't Parse"
        s_floor = "Can't Parse"
        s_datacabinet = "Can't Parse"
        s_vc = "Can't Parse"

    return s_geo, s_floor, s_datacabinet, s_vc,


def post_info(t_title, t_description, t_big_value_switch, t_big_value_port, t_upper_left_value, t_lower_left_value,
              t_upper_right_value, t_lower_right_value, server, api_key):
    t_title = 'Raspberry 1 location'
    # t_description='01:02:03:04:05:06'
    # t_big_value_switch=' T3-BK-DK1-VC1'
    # t_big_value_port='ge-0/0/20'
    t_upper_left_label = 'Cabinet / Kabin'
    # t_upper_left_value='DK3'
    t_lower_left_label = 'Floor / Kat :'
    # t_lower_left_value='BK'
    t_upper_right_label = 'Time changed :'
    # t_upper_right_value='333:00:03'
    t_lower_right_label = 'Device ip : '
    # t_lower_right_value='test'
    data = {
        'tile': 'big_value',
        'key': 'raspberry',
        'data': '{"title": "' + t_title + '",'
        '"description": "' + t_description + '",'
        '"big-value": "' + t_big_value_switch + ' \\r' + t_big_value_port + '",'
        '"upper-left-label": "' + t_upper_left_label + '",'
        '"upper-left-value": "' + t_upper_left_value + '",'
        '"lower-left-label": "' + t_lower_left_label + '",'
        '"lower-left-value": "' + t_lower_left_value + '",'
        '"upper-right-label": "' + t_upper_right_label + '",'
        '"upper-right-value": "' + t_upper_right_value + '",'
        '"lower-right-label": "' + t_lower_right_label + '",'
        '"lower-right-value": "' + t_lower_right_value + '"}'
    }
    if Log_Stat == True:
        print('data to post tipboard :',data)
    requests.post('http://' + server + '/api/v0.1/' + api_key + '/push', data=data)
    # r.status_code, r.reason
    # print(r.text)
    # print(r.status_code, r.reason)



def get_config_data(config_filename, self):
    with open(config_filename, 'r') as ymlfile:
        config_data = yaml.load(ymlfile)
    return config_data


def get_switch_data(formatted_filename, self):
    with open(formatted_filename, 'r') as f:
        next(f, None)  # Skip first line (if any)
        reader = csv.reader(f)
        switch_data = list(reader)
    return switch_data


def search_for_mac_and_tip(s_mac, s_ip, s_port, s_current_time,s_file, s_user,ss_server,ss_api):
    dev = Device(host=s_ip, user=s_user, ssh_private_key_file=s_file, port=s_port)
    s_location =""
    s_name=""
    s_FLOOR=""
    s_DC=""
    s_VC=""
    s_Message=""
    yml = '''
    EthernetSwitchingTable:
      rpc: get-ethernet-switching-table-information
      item: l2ng-l2ald-mac-entry-vlan/l2ng-mac-entry
      key:
         - l2ng-l2-mac-address
         - l2ng-l2-mac-logical-interface
         - l2ng-l2-vlan-id
      view: EtherSwView

    EtherSwView:
      fields:
        mac: l2ng-l2-mac-address
        port_id: l2ng-l2-mac-logical-interface
        id: l2ng-l2-vlan-id
    '''

    globals().update(FactoryLoader().load(yaml.load(yml)))
    dev.open()
    table = EthernetSwitchingTable(dev)
    table.get()

    for i in table:
        if i.mac == s_mac:
            s_port = i.port_id
            s_name = dev.facts['hostname']
            s_details = name_details(dev.facts['hostname'])
            s_location = s_details[0]
            s_FLOOR = s_details[1]
            s_DC = s_details[2]
            s_VC = s_details[3]
            s_Message = "found"
    dev.close()

    if Log_Stat == True:
        print('Data to be posted :',(s_mac, s_name, s_port, s_VC, s_DC,s_FLOOR, s_current_time,s_ip,ss_server, ss_api))
    post_info(s_mac, s_name, s_port, s_VC, s_DC,s_FLOOR,s_current_time,s_ip,ss_server, ss_api)



if len(sys.argv) < 3:
    print('You did not enter the required parameters!')
    print('Usage python3 trackmactip.py ./switch_database.csv ./trackmactip.yaml')
else:
    #command line paramaters
    switch_db_file = sys.argv[1]
    config_file = sys.argv[2]
    #Reading config and db files
    config = get_config_data(config_file, "")
    devices = get_switch_data(switch_db_file, "")
    mac_address = config['Tracked_Mac']['mac-address']
    #Reading Logging status
    Log_Stat = config['Logging']['verbose_logging']

    private_key_file = devices[0][3]
    server_address = config['Tipboard']['tipboardServer']+':'+config['Tipboard']['tipboardPort']
    api_key = config['Tipboard']['tipboardAPIkey']

    if Log_Stat == True:
        print('Mac to look for :',config['Tracked_Mac']['mac-address'])
        print('First entrt in CSV :', devices[0][0])
        hostname = devices[0][0]
        print('IP Address :',hostname)
        connection_port = devices[0][1]
        print('Port :',connection_port)
        username = devices[0][2]
        print('Username :',username)
        print('Private Key dosyası :',private_key_file)
        print('DB deki Girdi adedi : ',len(devices))
    sleep_time=int(config['Engine']['checkInterval'])
    p=1
    while True:
        thread_list = []
        for k in range(len(devices)):
            hostname = devices[k][0]
            connection_port = devices[k][1]
            username = devices[k][2]
            private_key_file = devices[k][3]
            current_time=str(datetime.datetime.now())

            thread = threading.Thread(target=search_for_mac_and_tip, args=(mac_address, hostname, connection_port, current_time,private_key_file, username,server_address,api_key))
            thread_list.append(thread)
            thread.start()
        if Log_Stat == True:
            p += 1
            print('loop ', p )
        time.sleep(sleep_time)
