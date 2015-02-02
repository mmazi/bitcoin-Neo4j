#!/usr/bin/env python

import simplejson as json
import httplib
import urllib2

from httplib import HTTPConnection, HTTPS_PORT
import ssl
from decimal import *
fileBlockList = open("poc_blockdata.txt", "w")

tout = 1
tin = 1
addrList = ["1G541ENwQBqG3WZgvYtVCojVgdHFpJ8RXs","16N3jvnF7UhRh74TMmtwxpLX6zPQKPbEbh","1NkjXACtWM358virDfhbE8rZsWWgrkVhsa","1FRtvFuwn736RmCfnroE3NmtWDR8jmjMZz"]
for s in addrList:
	
	url = "https://blockchain.info/address/" + str(s) + "?format=json"
	print url
	usock = urllib2.urlopen(url)
	data = usock.read()
	result = json.loads(data)

	address = result['address']
	numLoops = result['n_tx']/50
	
	for x in range(0, numLoops+1):
		loopValue = x * 50
		url3 = "https://blockchain.info/address/" + str(s) + "?format=json&offset=" + str(loopValue)
		print url3
		usock3 = urllib2.urlopen(url3)
		data3 = usock3.read()
		result3 = json.loads(data3)
		
		parent =  result3["txs"]
		for item in parent:
			block_height = str(item["block_height"])
#		print block_height
			url2 = "https://blockchain.info/block-height/" + str(block_height) + "?format=json"
			usock2 = urllib2.urlopen(url2)
			data2 = usock2.read()
			result2 = json.loads(data2)

			parent2 =  result2["blocks"]
			for item2 in parent2:
				block_index = str(item2["block_index"])
#			print block_index
				fileBlockList.write(str(block_height) + "|" + str(block_index) + "\n")
			usock2.close()
		usock.close()
	
fileBlockList.close()
print "Done"



