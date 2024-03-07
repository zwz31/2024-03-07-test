#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding:utf-8

import os
import paramiko
import binascii
import requests
import win32crypt

addr = '172.19.200.164:80'
user = 'root'
pwd = '123456'

def LoginRDP(ip_port, username, passwd):
    pwdHash = win32crypt.CryptProtectData(passwd, u'psw', None, None, None, 0)
    pwdHash_ok = binascii.hexlify(pwdHash)
    pwdHash_ok = binascii.hexlify(pwdHash)
    rdpFileStr = u'''
screen mode id:i:1 
desktopwidth:i:1280 
desktopheight:i:750 
session bpp:i:24 
winposstr:s:2,3,188,8,1062,721 
full address:s:%(ip)s
compression:i:1 
keyboardhook:i:2 
audiomode:i:0 
redirectdrives:i:0 
redirectprinters:i:0 
redirectcomports:i:0 
redirectsmartcards:i:0 
displayconnectionbar:i:1 
autoreconnection enabled:i:1 
username:s:%(username)s
domain:s:MyDomain 
alternate shell:s: 
shell working directory:s: 
password 51:%(pwdHash_ok)s
disable wallpaper:i:1 
disable full window drag:i:1 
disable menu anims:i:1 
disable themes:i:0 
disable cursor setting:i:0 
bitmapcachepersistenable:i:1
    ''' % dict(ip=ip_port, username=username, pwdHash_ok=pwdHash_ok)
    rdpFileName = "%s.rdp"% username
    with open(rdpFileName, 'w') as f:
        f.write(rdpFileStr)
    os.system(".\\%s" % rdpFileName)


def LoginSSH(ip_port, username, passwd):
    ssh = paramiko.SSHClient()
    ip_split = ip_port.split(":")
    if len(ip_split) > 2 and '[' in ip_split:
        ip = ''.join(ip_split[:-1])
    else:
        ip = ip_split[0]
    port = int(ip_split[-1])
    ssh.connect(hostname=ip, port=port, username=username, passwd=passwd)


def LoginHTTP(ip_port, username, passwd):
    url = "http://" + ip_port
    if "443" in ip_port:
        url = "https://" + ip_port
    requests.post(url, data={"username": username, "passwd": passwd})


if __name__ == '__main__':
    if addr.endswith("3389"):
        LoginRDP(addr, user, pwd)
    elif addr.endswith("22"):
        LoginSSH(addr, user, pwd)
    elif addr.endswith("80") or addr.endswith("443"):
        LoginHTTP(addr, user, pwd)
    else:
        try:
            LoginRDP(addr, user, pwd)
        except:
            try:
                LoginSSH(addr, user, pwd)
            except:
                LoginHTTP(addr, user, pwd)
