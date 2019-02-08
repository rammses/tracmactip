#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Name Parse training file
- Parses info from a dash limited string
- Sample string T3-BK-DK1-VC1"
-               |  |  |   |
-               |  |  |   ---- Virtula Chasis No
-               |  |  -------- Data Cabinet no
-               |  ----------- Floor
-                ------------- Geographic location
"""
__author__ = "Mesut Bayrak 'Rammses' "
__copyright__ = "Copyright 2016, ISTANBUL"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Mesut Bayrak"
__email__ = "mesut@mikronet.net"
__status__ = "Beta "

sample = "T3-BK-DK1-VC1"


def parse_name(text, self):
    """ Name Parser
    - Parses info from a dash limited string
    - Sample string T3-BK-DK1-VC1"
    -               |  |  |   |
    -               |  |  |   ---- Virtula Chasis No
    -               |  |  -------- Data Cabinet no
    -               |  ----------- Floor
    -                ------------- Geographic location
    """
    text1 = text.split('-')
    s_geo = text1[0]
    s_floor = text1[1]
    s_datacabinet = text1[2]
    s_vc = text1[3]
    return s_geo, s_floor, s_datacabinet, s_vc


showme = parse_name(sample, "")

print(showme)
