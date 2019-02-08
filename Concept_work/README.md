# Concept work for pyez Junos
Don't forget to have key files within this folder
please change variables first
## About check_concept.py
- Gets mac database and displays it on shell 

Depends heavily on junos version and pyez version if your environment is different than
- Junos 15.1X53-D590.1
- Pyez 2.2

always check xml output on switch via 

    show ethernet-switching table detail | display xml
if the output is not shown as

    <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1X53/junos">
        <l2ng-l2ald-rtb-macdb>
            <l2ng-l2ald-mac-entry-vlan junos:style="extensive">
                <l2ng-l2-mac-address>00:09:0f:fe:46:c6</l2ng-l2-mac-address>
                <mac-count-global>10</mac-count-global>
                <learnt-mac-count>10</learnt-mac-count>
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
            <l2ng-l2ald-mac-entry-vlan junos:style="extensive">
                <l2ng-l2-mac-address>00:09:df:e2:e8:98</l2ng-l2-mac-address>
                <mac-count-global>10</mac-count-global>
                <learnt-mac-count>10</learnt-mac-count>
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
Change the yml code according to your output 

## About get_facts.py
The most simple communications check file. Use it for authentication check