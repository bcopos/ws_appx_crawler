#!/usr/bin/env python

import time
import random
import subprocess
import os
import argparse

'''
	Downloads app using file of links from crawler

	Should probably use a db to keep track of downloaded apps and blah blah but oh well

	Author: Bogdan Copos (bcopos@ucdavis.edu)
'''

MAX_SLEEP_TIME = 60
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0"
ACCEPT_HEADER = "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"

def main(linksfile):
	links = read_file(linksfile)
	downloaded_file = linksfile + ".downloaded"

	downloaded_links = []
	if os.path.isfile(downloaded_file):
		downloaded_links = read_file(downloaded_file)
	
	for link in links:
		# if already downloaded, skip por favor
		if link in downloaded_links:
			continue
		
		# app hash (the thing before xap in the link, assuming it's a hash of the app)
		apphash = str(link.split('/')[-2:-1][0])
		apphash += ".appx"

		# translate link and download app using wget
		cmd = "wget" + " --header=\"" + ACCEPT_HEADER + "\"" + " --user-agent=\"" + USER_AGENT + "\"" + " -O " + apphash + " " + link
		p = subprocess.call(cmd, shell=True)
		if p != 0:
			print "wget failed on link " + str(link)
		
		# record download
		downloaded_links.append(link)
		f = open(downloaded_file, 'a')
		f.write(link+'\n')
		f.close()		

		time.sleep(random.randint(0, MAX_SLEEP_TIME)) 


def read_file(filename):
	f = open(filename, 'r')
	links = f.readlines()
	f.close()
	return links

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-i','--inputfile', type=str, required=True, help="file (with path) containing links from crawler)")
	args = parser.parse_args()
	
	main(args.inputfile)
