#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
A simple Shadowsocks ss:// URI generator.
Written by Drickle Sotherman <drickle99@hotmail.com>
Supports SIP002 scheme.
CLI usage:
ss-urigen.py <path/to/jsonfile> # Generate from a json directly
ss-urigen.py # Will ask you everything 
'''
import json
import base64
from urllib import parse
from getpass import getpass
datastore = []
filelist = []
class server:
    def __init__(self):
        self.SIP002 = False
        self.server = ''
        self.port = ''
        self.password = ''
        self.method = 'chacha20-ietf-poly1305'
        self.plugin = ''
        self.opts = ''

def parse_json ():
    '''
    `parse_json(filelist:list)`
    Will be called by `main()` after scanned parameters and added to filelist
    Parse represented JSON file one by one, and add to `global datastore` .
    '''
    global filelist
    for file in filelist:
        print(file)
        try :
            parsed_json = json.load(open(file))
        except FileNotFoundError:
            print(f"Error - File not found: {file}. Ignoring.")
            continue
        except json.JSONDecodeError:
            print(f'Error - Unable to parse JSON file {file}. Ignoring.')
            continue
        global datastore
        current = server()
        try:
            current.server = parsed_json['server']
            current.port = str(parsed_json['server_port'])
            current.password = parsed_json['password']
            current.method = parsed_json['method']
            if parsed_json.get('plugin') != '':  # Determines if it is a SIP002 scheme
                current.SIP002 = True
                current.plugin = parsed_json['plugin']
                try:
                    current.opts = parsed_json['plugin_opts']
                except:
                    pass
            datastore.append(current)
        except:
            print(f"Error - Unable to parse JSON file {file}. Exiting.")
            exit(1)
    return

def generate_uri():
    for item in datastore:
        if item.SIP002 :
            encrypt = (
                item.method + ':' +
                item.password
            )
            notencrypt = (
                '@' + item.server +
                ':' + item.port +
                '/?plugin=' + item.plugin+ 
                parse.quote(';' + item.opts)
            )
        else :
            encrypt = (
                item.method + ':' +
                item.password + '@' +
                item.server + ':' +
                item.port
            )
            notencrypt = ''
        uri = 'ss://' + base64.b64encode(encrypt.encode('utf-8')).decode('utf-8').replace('=','') + notencrypt
        print(uri)
    exit(0)

def ask():
    tempserver = server()
    tempserver.server = input('Server address: ')
    tempserver.port = input('Port: ')
    tempserver.password = getpass(prompt='Password: ')
    method = input('Encryption (chacha20-ietf-poly1305): ')
    if method == '':
        tempserver.method = 'chacha20-ietf-poly1305'
    else:
        tempserver.method = method
    ans = input("Plugin attached (y/N)? ")
    if ans in ('Y','y'):
        tempserver.SIP002 = True
        tempserver.plugin = input('Plugin: ')
        tempserver.opts = input('Plugin params: ')
    datastore.append(tempserver)
    print('')

    generate_uri()

def main() :
    global filelist
    import sys
    if len(sys.argv) <= 1:
        try:
            ask()
        except KeyboardInterrupt:
            print('User aborted. Exiting.')
            exit(1)
    else:
        args = sys.argv[1:]
        for arg in args:
            filelist.append(arg)
        parse_json()
        generate_uri()

if __name__ == '__main__':
    main()