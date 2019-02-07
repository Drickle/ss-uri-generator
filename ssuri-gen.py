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
datastore = {
    'server':'',
    'port':'',
    'password':'',
    'method':'',
    'plugin':'',
    'plugin_opts':''
}

def parse_json (jsonfile):
    try :
        parsed_json = json.load(open(jsonfile))
    except:
        print("Error - Unable to load your JSON file. Exiting.")
        exit(1)

    global datastore
    try:
        datastore['server'] = parsed_json['server']
        datastore['port'] = parsed_json['local_port']
        datastore['password'] = parsed_json['password']
        datastore['method'] = parsed_json['method']
        if parsed_json.get('plugin') != '': # Determines if it is a SIP002 scheme
            datastore['plugin'] = parsed_json['plugin']
            datastore['plugin_opts'] = parsed_json['plugin_opts']
        return
    except:
        print("Error - Unable to parse your JSON file. Exiting.")
        exit(1)

def generate_uri(data:dict):
    if data.get('plugin','') != '':
        encrypt = (
            data['method'] + ':' +
            data['password']
        )
        notencrypt = (
            '@' + data['server'] +
            ':' + data['port'] +
            '/?plugin=' + data['plugin'] + 
            parse.quote(';' + data['plugin_opts'])
        )
    else :
        encrypt = (
            data['method'] + ':' +
            data['password'] + '@' +
            data['server'] + ':' +
            data['port']
        )
        notencrypt = ''
    uri = 'ss://' + base64.b64encode(encrypt.encode('utf-8')).decode('utf-8').replace('=','') + notencrypt
    print(uri)
    print('')
    exit(0)

def ask():
    global datastore
    datastore['server'] = input('Server address: ')
    datastore['port'] = input('Port: ')
    datastore['password'] = getpass(prompt='Password: ')
    method = input('Encryption (chacha20-ietf-poly1305): ')
    if method == '':
        datastore['method'] = 'chacha20-ietf-poly1305'
    else:
        datastore['method'] = method
    ans = input("Plugin attachged (y/N)? ")
    if ans in ('Y','y'):
        datastore['plugin'] = input('Plugin: ')
        datastore['plugin_opts'] = input('Plugin params: ')
    print('')
    generate_uri(datastore)
    print('')

def main() :
    import sys
    try:
        file = sys.argv[1]
        parse_json(file)
        generate_uri(datastore)
    except IndexError: # file not given
        ask()
    
if __name__ == '__main__':
    main()