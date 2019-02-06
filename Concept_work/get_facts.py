#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Facts retriever
- Gets device facts form junos device using keypair authentication method
"""
__author__      = "Mesut Bayrak 'Rammses' "
__copyright__   = "Copyright 2016, ISTANBUL"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Mesut Bayrak"
__email__ = "mesut@mikronet.net"
__status__ = "Beta "

import sys
from getpass import getpass
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from pprint import pprint


hostname = '192.168.17.200'
username = 'tipboard'
private_key_file = "./tipboard_nopass.key"
connection_port = 2223

dev = Device(host=hostname, user=username, ssh_private_key_file=private_key_file,port=connection_port)

try:
    dev.open()
except ConnectError as err:
    print ("Cannot connect to device: {0}".format(err))
    sys.exit(1)
except Exception as err:
    print (err)
    sys.exit(1)



pprint (dev.facts)
dev.close()
