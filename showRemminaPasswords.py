#!/usr/bin/python
import base64
import os
import re
import sys

try:
    from Crypto.Cipher import DES3
except Exception as e:
    print(e)
    print('pip3 install --upgrade pycrypto')
    sys.exit(1)

HOME = os.path.expanduser("~")
CHARSET = 'utf-8'

REMMINA_FOLDER = '/home/andrea/.local/share/remmina' 
if REMMINA_FOLDER[-1] != '/':
    REMMINA_FOLDER = REMMINA_FOLDER+'/'

REMMINA_PREF   = '/home/andrea/.config/remmina/remmina.pref' 
REGEXP_ACCOUNTS = r'([^.]+)\.remmina(.swp)?'

def show_remmina_accounts():
    diz = {}
    res = []
    fs = open(REMMINA_PREF)
    fso = fs.readlines()
    fs.close()

    for i in fso:
        if re.findall(r'secret=', i):
            r_secret = i[len(r'secret='):][:-1]            
        
    for f in os.listdir(REMMINA_FOLDER):
        if re.findall(REGEXP_ACCOUNTS, f): 
            fo = open( REMMINA_FOLDER+f, 'r')
            for i in fo.readlines():
                if re.findall(r'^group=', i):
                    r_group = i.split('=')[1][:-1]
                if re.findall(r'^password=', i):
                    r_password = i[len(r'password='):][:-1]
                if re.findall(r'^name=', i):
                    r_name = i.split('=')[1][:-1]
                if re.findall(r'^username=', i):
                    r_username = i.split('=')[1][:-1]
            
            password = base64.b64decode(r_password)
            secret = base64.b64decode(r_secret)
            
            diz[r_name] = DES3.new(secret[:24], DES3.MODE_CBC, secret[24:]).decrypt(password)
            if sys.version_info.major == 3:
                pval = diz[r_name].decode(CHARSET)
            else:
                pval = diz[r_name]
            r = (r_group, r_name, r_username, pval, diz[r_name])
            res.append(r)
            #print('{} {} {} [raw:{}]'.format(*r))
            print('{} {} {} {} '.format(*r))
            fo.close()
    return res
    
if __name__ == '__main__':
    show_remmina_accounts()