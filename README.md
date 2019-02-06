# tracmactip
Use case : 
- Junos only !
- no addressing/numbering on ethernet jacks 
- need to identify which switch and port
- You need to have a mobile ethernet client, any laptop/raspberry/arduino will do

What you need to do for this to work:

you;
- need to enter the mac address to config file 
- have to create a csv file as mentioned below
- need to create a netconf user on every juniper switch you own 
- for security reasons i made this using keypair auth which is explained below if you do know what you do you can use username password auth but i don't reccomend it


tracks a special mac address in JUNOS based switches addressed in csv based database using keypair auth wit pyez, pushes the info to an indicator at tipboard server

## PYez ve Tipboard ile mac tracking


Server ubuntu 16.04 

## Dependency installations for PYez modules

		#sudo apt install  python3-pip python3-dev libxml2-dev libxslt-dev libssl-dev libffi-dev

##Updating the PIP3 repositories
		#pip3 install --upgrade pip

## Installation of PYez

		#pip3 install junos-eznc

## Creating a keypair and a Netconf user to establish connection using PYez 
## Server side steps 
do not use passwords in keypair

		# ssh-keygen -t rsa
		Generating public/private rsa key pair.
		Enter file in which to save the key (/root/.ssh/id_rsa): tipboard_nopass.key
		Enter passphrase (empty for no passphrase):
		Enter same passphrase again:
		Your identification has been saved in tipboard_nopass.key.
		Your public key has been saved in tipboard_nopass.key.pub.
		The key fingerprint is:
		SHA256:39dwxZTgeRK4T+p6T5eKL3hgDv1tTtb8ZB81T7bGT8o root@ubuntu
		The key's randomart image is:
		+---[RSA 2048]----+
		|            .o. o|
		|           .. o+ |
		|            .+ .o|
		|           . .o .|
		|        S   + ..=|
		|       . = o .+**|
		|        + * o+.X*|
		|         o *==+==|
		|         .+.*=E +|
		+----[SHA256]-----+


1. this command creates 2 files, one has a pub extension you need upload this file to /var/tmp foler
2. The private key file must be used as identity file while creating a connection to junos switch 

put the public key file using scp to switch


		# scp tipboard_nopass.key.pub root@192.168.17.200:/var/tmp/tipboard_nopass.key.pub
		Password:
		tipboard_nopass.key.pub
## Switch side steps
### Creating a Superuser enabled user with key only authentication 

-----------
		{master:0}[edit]
		root@SWH_PS_WS_CA0201# set system login user tipboard class super-user authentication load-key-file /var/tmp/tipboard_
		                                                                                                                      ^
		'/var/tmp/tipboard_' is ambiguous.
		Possible completions:
		  <load-key-file>      File (URL) containing one or more ssh keys
		  /var/tmp/tipboard_nopass.key.pub  Size: 393, Last changed: Feb 01 04:14:21
		  /var/tmp/tipboard_public  Size: 448, Last changed: Feb 01 04:08:35
		{master:0}[edit]
		root@SWH_PS_WS_CA0201# set system login user tipboard class super-user authentication load-key-file /var/tmp/tipboard_nopass.key.pub
		#commit
-----------

### Enable netconf with port change def=830

		root@SWH_PS_WS_CA0201# set system services netconf ssh
		{master:0}[edit]
		root@SWH_PS_WS_CA0201# show | compare
		[edit system services]
		+    netconf {
		+        ssh;
		+    }
		{master:0}[edit]
		root@SWH_PS_WS_CA0201# commit
		configuration check succeeds
		commit complete

Change port as 2223 

		#set system services netconf ssh port 2223


## Testing

If you receive what we call dev.facts as shown below everything is fine. You've established an PYez connection to junos switch
	
	root@ubuntu:~# ssh -i ./tipboard_nopass.key tipboard@192.168.17.200 -p 2223 -s netconf
	<!-- No zombies were killed during the creation of this user interface -->
	<!-- user tipboard, class j-super-user -->
	<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
	  <capabilities>
	    <capability>urn:ietf:params:netconf:base:1.0</capability>
	    <capability>urn:ietf:params:netconf:capability:candidate:1.0</capability>
	    <capability>urn:ietf:params:netconf:capability:confirmed-commit:1.0</capability>
	    <capability>urn:ietf:params:netconf:capability:validate:1.0</capability>
	    <capability>urn:ietf:params:netconf:capability:url:1.0?scheme=http,ftp,file</capability>
	    <capability>urn:ietf:params:xml:ns:netconf:base:1.0</capability>
	    <capability>urn:ietf:params:xml:ns:netconf:capability:candidate:1.0</capability>
	    <capability>urn:ietf:params:xml:ns:netconf:capability:confirmed-commit:1.0</capability>
	    <capability>urn:ietf:params:xml:ns:netconf:capability:validate:1.0</capability>
	    <capability>urn:ietf:params:xml:ns:netconf:capability:url:1.0?protocol=http,ftp,file</capability>
	    <capability>http://xml.juniper.net/netconf/junos/1.0</capability>
	    <capability>http://xml.juniper.net/dmi/system/1.0</capability>
	  </capabilities>
	  <session-id>6914</session-id>
	</hello>
	]]>]]>


To test default ssh port request terminal using -t netconf or you get stuck in terminal screen and you have to kick newly created user from terminal.

	{master:0}
	root@SWH_PS_WS_CA0201> show system users
	fpc0:
	--------------------------------------------------------------------------
	Failed conversion of ``26:50'' using format ``%k:%M''
	date: illegal time format
	usage: date [-jnRu] [-d dst] [-r seconds] [-t west] [-v[+|-]val[ymwdHMS]] ...
	            [-f fmt date | [[[[[cc]yy]mm]dd]HH]MM[.ss]] [+format]
	<uptime-information>
	<date-time junos:seconds="1548995600">4:33AM</date-time>
	<up-time junos:seconds="97620">1 day,  3:07</up-time>
	<active-user-count junos:format="3 users">3</active-user-count>
	<load-average-1>0.53</load-average-1>
	<load-average-5>0.38</load-average-5>
	<load-average-15>0.35</load-average-15>
	<user-table>
	<user-entry>
	<user>mikronet</user>
	<tty>u0</tty>
	<from>-</from>
	<login-time junos:seconds="1548984800">Thu01AM</login-time>
	<idle-time junos:seconds="1548984800">26:50</idle-time>
	<command>-cl</command>
	</user-entry>
	<user-entry>
	<user>root</user>
	<tty>pts/0</tty>
	<from>192.168.17.92</from>
	<login-time junos:seconds="1548992000">3:33AM</login-time>
	<idle-time junos:seconds="0">-</idle-time>
	<command>cli</command>
	</user-entry>
	<user-entry>
	<user>tipboard</user>
	<tty>pts/1</tty>
	<from>192.168.17.91</from>
	<login-time junos:seconds="1548995540">4:32AM</login-time>
	<idle-time junos:seconds="0">-</idle-time>
	<command>mgd</command>
	</user-entry>
	</user-table>
	</uptime-information>

	{master:0}



## Simple get_facts testing output

use the get_facts.py file at concept_work folder to check minimal access to switch 

	 # python3 get_facts.py
	 'HOME': '/var/home/tipboard',
	 'RE0': {'last_reboot_reason': '0x1:power cycle/failure',
	         'mastership_state': 'master',
	         'model': 'RE-EX2300-48P',
	         'status': 'OK',
	         'up_time': '1 day, 3 hours, 25 minutes, 58 seconds'},
	 'RE1': None,
	 'RE_hw_mi': False,
	 'current_re': ['master',
	                'node',
	                'fwdd',
	                'member',
	                'pfem',
	                're0',
	                'fpc0',
	                'localre'],
	 'domain': None,
	 'fqdn': None,
	 'hostname': 'SWH_PS_WS_CA0201',
	 'hostname_info': {'fpc0': 'SWH_PS_WS_CA0201'},
	 'ifd_style': 'SWITCH',
	 'junos_info': {'fpc0': {'object': junos.version_info(major=(15, 1), type=X, minor=(53, 'D', 590), build=1),
	                         'text': '15.1X53-D590.1'}},
	 'master': 'RE0',
	 'model': 'EX2300-48P',
	 'model_info': {'fpc0': 'EX2300-48P'},
	 'personality': 'SWITCH',
	 're_info': {'default': {'0': {'last_reboot_reason': '0x1:power cycle/failure',
	                               'mastership_state': 'master',
	                               'model': 'RE-EX2300-48P',
	                               'status': 'OK'},
	                         'default': {'last_reboot_reason': '0x1:power '
	                                                           'cycle/failure',
	                                     'mastership_state': 'master',
	                                     'model': 'RE-EX2300-48P',
	                                     'status': 'OK'}}},
	 're_master': {'default': '0'},
	 'serialnumber': 'JW0218050498',
	 'srx_cluster': None,
	 'srx_cluster_id': None,
	 'srx_cluster_redundancy_group': None,
	 'switch_style': 'VLAN_L2NG',
	 'vc_capable': True,
	 'vc_fabric': False,
	 'vc_master': '0',
	 'vc_mode': 'Enabled',
	 'version': '15.1X53-D590.1',
	 'version_RE0': None,
	 'version_RE1': None,
	 'version_info': junos.version_info(major=(15, 1), type=X, minor=(53, 'D', 590), build=1),
	 'virtual': False}

## Usage Of trackmactip.py

Usage

    #python3 trackmactip.py ./switch_database.csv ./trackmactip.yaml

### The switch_database.csv file explained
Yet another boring csv file, you have to add every device and their private key location with the order show below.

    #"switch_ip_address","switch_netconf_port","netconf_username","private_key_file_location"
    "192.168.17.200","2223","tipboard","./tipboard_nopass.key"
    "192.168.17.200","830","readonly","./readnly_users_nopassword_private.key"

### The config.yaml file explained

It is actually very human readable
if you want to track additional ip addresses just add them and increase the number. Just remember tile will display the information based FIFO

So if you plug mac1 first then mac2 second you'll be seeing mac2 on tipboard tile.
Tile and API key section is going to be explained in tipboard server setup.   

    Logging:
      logfile : '/var/log/trackmactip.log'
      verbose_logging: False
    
    Tracked_Mac:
      mac-address1: "00:01:02:03:04:05"
      mac-address2: "0a:0b:0c:0d:0e:0f"
    
    Tipboard:
      tipboardServer: "192.168.17.91"
      tipboardPort: "192.168.17.91"
      tipboardAPIkey: "e2c3275d0e1a4bc0da360dd225d74a43"
      tipboardTileData: "tile=text key=id_1"





### Notes

## PIP may create problems 
Rehash and continue as shown below

    root@ubuntu:~#
    root@ubuntu:~# pip3
    Traceback (most recent call last):
      File "/usr/bin/pip3", line 9, in <module>
        from pip import main
    ImportError: cannot import name 'main'
    root@ubuntu:~# hash -d pip
    -bash: hash: pip: not found
    root@ubuntu:~# hash -d pip3 <--
    root@ubuntu:~# pip3 install junos-eznc
    Collecting junos-eznc
      Using cached https://files.pythonhosted.org/packages/00/b5/3d6d2d572789421b71d2bd7e3bae843db504cad59415bf817c7b9075aad6/junos_eznc-2.2.0-py2.py3-none-any.whl
    Collecting pyserial (from junos-eznc)


## Some of paramiko's crypto functions are deprecated 
This is a known bug you can ignore them. Sample outputs are shown below

	/usr/local/lib/python3.5/dist-packages/paramiko/kex_ecdh_nist.py:39: CryptographyDeprecationWarning: encode_point has been deprecated on EllipticCurvePublicNumbers and will be removed in a future version. Please use EllipticCurvePublicKey.public_bytes to obtain both compressed and uncompressed point encoding.
	  m.add_string(self.Q_C.public_numbers().encode_point())
	/usr/local/lib/python3.5/dist-packages/paramiko/kex_ecdh_nist.py:96: CryptographyDeprecationWarning: Support for unsafe construction of public numbers from encoded data will be removed in a future version. Please use EllipticCurvePublicKey.from_encoded_point
	  self.curve, Q_S_bytes
	/usr/local/lib/python3.5/dist-packages/paramiko/kex_ecdh_nist.py:111: CryptographyDeprecationWarning: encode_point has been deprecated on EllipticCurvePublicNumbers and will be removed in a future version. Please use EllipticCurvePublicKey.public_bytes to obtain both compressed and uncompressed point encoding.
	  hm.add_string(self.Q_C.public_numbers().encode_point())
	{'2RE': False, 'HOME': '/var/home/tipboard', 'RE0': {'mastership_state': 'master', 'status': 'OK', 'up_time': '1 day, 3 hours, 23 minutes, 39 seconds', 'model': 'RE-EX2300-48P', 'last_reboot_reason': '0x1:power cycle/failure'}, 'RE1': None, 'RE_hw_mi': False, 'current_re': ['master', 'node', 'fwdd', 'member', 'pfem', 're0', 'fpc0', 'localre'], 'domain': None, 'fqdn': None, 'hostname': 'SWH_PS_WS_CA0201', 'hostname_info': {'fpc0': 'SWH_PS_WS_CA0201'}, 'ifd_style': 'SWITCH', 'junos_info': {'fpc0': {'text': '15.1X53-D590.1', 'object': junos.version_info(major=(15, 1), type=X, minor=(53, 'D', 590), build=1)}}, 'master': 'RE0', 'model': 'EX2300-48P', 'model_info': {'fpc0': 'EX2300-48P'}, 'personality': 'SWITCH', 're_info': {'default': {'0': {'mastership_state': 'master', 'status': 'OK', 'last_reboot_reason': '0x1:power cycle/failure', 'model': 'RE-EX2300-48P'}, 'default': {'mastership_state': 'master', 'status': 'OK', 'last_reboot_reason': '0x1:power cycle/failure', 'model': 'RE-EX2300-48P'}}}, 're_master': {'default': '0'}, 'serialnumber': 'JW0218050498', 'srx_cluster': None, 'srx_cluster_id': None, 'srx_cluster_redundancy_group': None, 'switch_style': 'VLAN_L2NG', 'vc_capable': True, 'vc_fabric': False, 'vc_master': '0', 'vc_mode': 'Enabled', 'version': '15.1X53-D590.1', 'version_RE0': None, 'version_RE1': None, 'version_info': junos.version_info(major=(15, 1), type=X, minor=(53, 'D', 590), build=1), 'virtual': False}
	root@ubuntu:~#
	root@ubuntu:~# vi get_facts.py
	root@ubuntu:~# python3 get_facts.py
	/usr/local/lib/python3.5/dist-packages/paramiko/kex_ecdh_nist.py:39: CryptographyDeprecationWarning: encode_point has been deprecated on EllipticCurvePublicNumbers and will be removed in a future version. Please use EllipticCurvePublicKey.public_bytes to obtain both compressed and uncompressed point encoding.
	  m.add_string(self.Q_C.public_numbers().encode_point())
	/usr/local/lib/python3.5/dist-packages/paramiko/kex_ecdh_nist.py:96: CryptographyDeprecationWarning: Support for unsafe construction of public numbers from encoded data will be removed in a future version. Please use EllipticCurvePublicKey.from_encoded_point
	  self.curve, Q_S_bytes
	/usr/local/lib/python3.5/dist-packages/paramiko/kex_ecdh_nist.py:111: CryptographyDeprecationWarning: encode_point has been deprecated on EllipticCurvePublicNumbers and will be removed in a future version. Please use EllipticCurvePublicKey.public_bytes to obtain both compressed and uncompressed point encoding.
	  hm.add_string(self.Q_C.public_numbers().encode_point())

