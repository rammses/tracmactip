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
import pprint
import os
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from pprint import pprint

import yaml
from jnpr.junos.factory.factory_loader import FactoryLoader


def get_switch_data(formatted_filename, self):
    # reads switch connection info and creates a tuple for every line
    with open(formatted_filename, 'r') as f:
        reader = csv.reader(f)
        switch_data = list(reader)
    return switch_data


def burda_dur(mesaj):
    try:
        input(mesaj)
    except SyntaxError:
        pass


if len(sys.argv) < 3:
    print('Gerekli parametreleri girmediniz!')
    print('kullanım şekli python3 trackmactip.py switch_konfig_datasi.csv trackmactip.cfg')
    else:
    switch_data = get_switch_data('./switch_database.csv', "")
    pprint("Switch data :", switch_data)
    print("Switch data :", switch_data[1][0])

# hostname = '192.168.17.200'
# username = 'tipboard'
# private_key_file = "./tipboard_nopass.key"
# connection_port = 2223

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
