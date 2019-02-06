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
import csv
import os
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from pprint import pprint

import yaml
from jnpr.junos.factory.factory_loader import FactoryLoader

def get_config_data(config_filename,self):
    # TODO: config dosyasını okuyup değişkenleri config_data indexine sıralı ata
    with open(config_filename, 'r') as ymlfile:
        config_data = yaml.load(ymlfile)
    return config_data


def get_switch_data(formatted_filename,self):
    with open(formatted_filename, 'r') as f:
        next(f, None) # Skip first line (if any)
        reader = csv.reader(f)
        switch_data = list(reader)
    return switch_data

if len(sys.argv) < 3:
    print('You did not enter the required parameters!')
    print('Usage python3 trackmactip.py ./switch_database.csv ./trackmactip.yaml')
else:

    switch_db_file = sys.argv[1]
    config_file = sys.argv[2]

    config=get_config_data(config_file,"")
    #print(config['Tracked_Mac'])
    #print("---------")

    devices=get_switch_data(switch_db_file,"")
    print(devices[0][0])
    print("---------")

    hostname = devices[0][0]
    print(hostname)
    connection_port = devices[0][1]
    print(connection_port)
    username = devices[0][2]
    print(username)
    private_key_file = devices[0][3]
    print(private_key_file)
    # sw db den okuyup değişkenlere yazıp düzgün print ettik
    print(len(devices))
    # device tuple boyutunu da aldık döngüde kullanmak için
    # TODO: Aşağıdaki engine kodunu döngüde kullanılabilecek bir fonksiona cevir.

# dev = Device(host=hostname, user=username, ssh_private_key_file=private_key_file,port=connection_port)


# yml = '''
# EthernetSwitchingTable:
#   rpc: get-ethernet-switching-table-information
#   item: l2ng-l2ald-mac-entry-vlan/l2ng-mac-entry
#   key:
#      - l2ng-l2-mac-address
#      - l2ng-l2-mac-logical-interface
#      - l2ng-l2-vlan-id
#   view: EtherSwView

# EtherSwView:
#   fields:
#     mac: l2ng-l2-mac-address
#     port_id: l2ng-l2-mac-logical-interface
#     id: l2ng-l2-vlan-id
# '''

# globals().update(FactoryLoader().load(yaml.load(yml)))

# dev.open()


# table = EthernetSwitchingTable(dev)
# table.get()
# print('tablo icerigi :',table)
# dev.close()


# for i in table:
#   print('mac:', i.mac)
#   print('port id:', i.port_id)
#   print('vlan id:', i.id)
#   print()

'''
yaml tablosu icin ornek xml ciktisi
root@SWH_PS_WS_CA0201> show ethernet-switching table detail | display xml
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1X53/junos">
    <l2ng-l2ald-rtb-macdb>
        <l2ng-l2ald-mac-entry-vlan junos:style="extensive">
            <l2ng-l2-mac-address>00:09:0f:fe:46:c6</l2ng-l2-mac-address>
            <mac-count-global>13</mac-count-global>
            <learnt-mac-count>13</learnt-mac-count>
            <l2ng-l2-mac-routing-instance>default-switch</l2ng-l2-mac-routing-instance>
            <l2ng-l2-vlan-id>1</l2ng-l2-vlan-id>
            <l2ng-l2-mac-vlan-name>default</l2ng-l2-mac-vlan-name>
            <l2ng-l2-mac-logical-interface>ge-0/0/40.0</l2ng-l2-mac-logical-interface>
            <l2ng-l2-mac-ifl-generation>473</l2ng-l2-mac-ifl-generation>
            <l2ng-l2-mac-entry-flags>in_hash,in_ifd,in_ifl,in_vlan,in_rtt,kernel,in_ifbd</l2ng-l2-mac-entry-flags>
            <l2ng-l2-mac-epoch>1</l2ng-l2-mac-epoch>
            <l2ng-l2-mac-sequence-number>0</l2ng-l2-mac-sequence-number>
            <l2ng-l2-mac-learn-mask>0x00000001</l2ng-l2-mac-learn-mask>
        </l2ng-l2ald-mac-entry-vlan>
'''
