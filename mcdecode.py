#!/usr/bin/env python3
import requests as req
import argparse
import re
import os
import json
from urllib.parse import urlparse

config_file = os.environ.get('HOME')+'/.mcdecode'
program_info = 'Decodes the encoded URL created by MimeCast Targetted Threat Protection - URL Protect feature. ' \
    'In order for URL to be decoded, a cookie from an enrolled browser needs to be specified via the command line ' \
    'or be stored in ~/.mcdecode'

parser = argparse.ArgumentParser(description=program_info)
parser.add_argument('--cookie', '-c', help='Cookie from an enrolled browser in the format of key=value')
parser.add_argument('--save', '-s', help='Save the specified cookie in ~/.mcdecode if URL is successfully decoded', action='store_true')
parser.add_argument('--url', '-u', help='Encoded URL', required=True)
parser.add_argument('--debug', help='Output debug information', action='store_true')

args = parser.parse_args()

# Check if valid looking cookie is specified as argument or be loaded from file
cookie_given = False
cookie_key = ''
cookie_value = ''

if args.cookie:
    if re.match('.*=.*', args.cookie) is None:
        print('ERROR: The specified cookie is not in the format: cookie=value')
        exit()
    else:
        tokens = args.cookie.split('=')

        if len(tokens) > 2:
            print('ERROR: More than one = character in the cookie. Specify cookie in the format: cookie=value')
            exit()

        cookie_key = tokens[0]
        cookie_value = tokens[1]
        cookie_given = True
else:
    if os.path.exists(config_file):
        line = ''

        file=open(config_file, 'r')
        if file.mode == 'r':
            line = file.readline()
        file.close()

        tokens = line.split('=')

        if len(tokens) > 2:
            print('ERROR: More than one = character in the cookie. Cookie file appears to be corrupt.')
            exit()

        cookie_key = tokens[0]
        cookie_value = tokens[1]
    else:
        print('ERROR: A valid cookie needs to be specified either via command line or cookie file.')
        exit()

if args.debug:
    print('DEBUG: Using cookie: ' + cookie_key + '=' + cookie_value)

# Make initial request
req1 = args.url
resp1 = req.get(req1, allow_redirects=False)

if 'Location' not in resp1.headers:
    print('ERROR: First response does not contain a "Location" header')
    exit()

if args.debug:
    print("DEBUG: First request status code: " + str(resp1.status_code))
    print("DEBUG: First request Location header: " + resp1.headers['Location'])

if resp1.status_code != 307:
    print('ERROR: First response status is ' + str(resp1.status_code) + '. Expecting 307.')
    exit()

# Make second request
cookies = {cookie_key: cookie_value}
req2 = resp1.headers['Location']
resp2 = req.get(req2, cookies=cookies, allow_redirects=False)

if 'Location' not in resp2.headers:
    print('ERROR: Second response does not contain a "Location" header')
    exit()

if args.debug:
    print("DEBUG: Second request status code: " + str(resp2.status_code))
    print("DEBUG: Second request Location header: " + resp2.headers['Location'])

if resp2.status_code != 307:
    print('ERROR: Second response status is ' + str(resp2.status_code) + '. Expecting 307.')
    exit()

url = resp2.headers['Location']

# Received device enrollment page
if re.match('^https://.+mimecast\.com/.+enrollment\?key=.*', url):
    print('ERROR: URL decode failed. Ensure a valid cookie is specified.')
    exit()

# Received email security training page, extract URL using API
if re.match('^https://.+mimecast\.com/.+\?key=.*', url):

    # Extract key
    key = url[url.index('key=') + len('key='):]

    if args.debug:
        print('DEBUG: Received email security training page, using API method')
        print('DEBUG: Extracted cacheKey: ' + key)

    # Prepare API input
    input = { 'data': [{'cacheKey':key, 'pageType':'user_challenge' }] }

    # Determine API URL and Make API call
    p = urlparse(url)
    base_url = p.scheme + '://' + p.netloc
    req3 = base_url + '/api/ttp/url/get-page-data'
    resp3 = req.post(req3, cookies=cookies, data=json.dumps(input))

    if args.debug:
         print('DEBUG: Making API call to: ' + req3)
         #print('DEBUG: Received response ' + resp3.text)

    output = json.loads(resp3.text)

    # Check response
    if output['meta']['status'] != 200:
        print('ERROR: API call unsuccessful.')
        exit()

    url = output['data'][0]['originalUrl']

print(url)

if args.save and cookie_given:
    if args.debug:
        print("DEBUG: Writing cookie to : " + config_file)

    file = open(config_file,'w')
    file.writelines(cookie_key + "=" + cookie_value)
    file.close()





