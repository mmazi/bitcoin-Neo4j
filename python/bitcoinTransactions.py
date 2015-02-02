#!/usr/bin/env python

import simplejson as json
import httplib
import urllib2

from httplib import HTTPConnection, HTTPS_PORT
import ssl
from decimal import *
file = open("poc_transaction.txt", "w")
fileIn = open("poc_transactionsIn.txt", "w")
fileOut = open("poc_transactionsOut.txt", "w")
fileTransList = open("poc_transactionList.txt","w")
fileBlockTrans = open("poc_relsBlocksTransactions.txt","w")
fileTransOut = open("poc_relsTransactionsOut.txt","w")
fileTransInRels = open("poc_relsTransactionsIn.txt","w")
filePaymentOutAddr = open("poc_relsPaymentsToAddress.txt","w")
filePaymentInAddr = open("poc_relsRedeemedFromAddress.txt","w")
fileAddressList = open ("poc_addressList.txt","w")
fileBlockList = open("poc_blockdata.txt", "w")

file.write(":ID,Transaction_ID,Hash,Time,V_In,V_Out,:LABEL" + "\n")
fileIn.write(":ID,Transaction_ID,Transaction_Hash,Address,Spent,Value,:LABEL" + "\n")
fileOut.write(":ID,Transaction_ID,Transaction_Hash,Type,:LABEL" + "\n")
fileBlockTrans.write(":START_ID,:END_ID,:TYPE" + "\n")
fileTransOut.write(":START_ID,:END_ID,Spent,Value,:TYPE" + "\n")
fileTransInRels.write(":START_ID,:END_ID,Spent,Value,:TYPE" + "\n")
filePaymentOutAddr.write(":START_ID,:END_ID,Spent,Value,:TYPE" + "\n")
filePaymentInAddr.write(":START_ID,:END_ID,Spent,Value,:TYPE" + "\n")
fileAddressList.write(":ID,AddressID,:LABEL" + "\n")
fileBlockList.write(":ID,BlockID,Hash,Received_Time,Previous_Block_Hash,Transaction_Count,Height,:LABEL"  + "\n")


tout = 1
tin = 1
f = open('blockList.txt', 'r')
temp = f.read().splitlines()
for line in temp:
	words = line.split("|")
	s = words[1]
	
	url = "https://blockchain.info/rawblock/" + str(s)
	print url
	usock = urllib2.urlopen(url)
	data = usock.read()
	result = json.loads(data)

	hash = result['hash']
	block_index = result['block_index']
	height = result['height']
	size = result['size']
	main_chain = result['main_chain']
	prev_block = result['prev_block']
	try: 
		received_time = result['received_time']
	except KeyError:
		received_time = 'NA'
	n_tx = result['n_tx']
	fileBlockList.write(str(hash) + ',' + str(block_index) + ',' +str(hash) + ',' + str(received_time) + ',' + str(prev_block) + ',' + str(n_tx) + ',' + str(height) + ",BlockChain" + "\n");

	parent =  result["tx"]
	for item in parent:
		tx_index = str(item["tx_index"])
		tx_hash = str(item["hash"])
		file.write(str('trans' + str(item["tx_index"])) + ',' + str(item["tx_index"]) + ',' +str(item["hash"]) + ',' + str(item["time"]) + ',' + str(item["vin_sz"]) + ',' + str(item["vout_sz"]) + ",Transaction"+ "\n");
		fileBlockTrans.write(str(hash) + ',' + str('trans' + str(item["tx_index"])) + ',' + 'PART_OF_BLOCK' + "\n")
		if 'inputs' in item :
			for nn in item["inputs"]:
#				print nn["sequence"]
				if 'prev_out' in nn :
#					print nn["prev_out"]["addr"]
#					print nn["prev_out"]["spent"]
#					print nn["prev_out"]["value"]
					try: 
						strAddr = str(nn["prev_out"]["addr"])
					except KeyError:
						strAddr = 'NA'

					fileIn.write('transin_' + str(tin) + ',' + tx_index + ',' + str(tx_hash) + ',' + strAddr + ',' +str(nn["prev_out"]["spent"]) + ',' + str( Decimal(nn["prev_out"]["value"]) / Decimal(100000000.0))  + ",IncomingPayment" + "\n");
					fileTransInRels.write('transin_' + str(tin) + ',' + 'trans' + str(tx_index) + ',' + str(nn["prev_out"]["spent"]) + ','+ str( Decimal(nn["prev_out"]["value"]) / Decimal(100000000.0)) + ',' + 'INCOMING_PAYMENT' + "\n")
					filePaymentInAddr.write(strAddr + ',' + 'transin_' + str(tin) + ',' + str(nn["prev_out"]["spent"]) + ','+ str( Decimal(nn["prev_out"]["value"])/ Decimal(100000000.0)) + ','+ 'REDEEMED' + "\n")
					fileTransList.write('transin_' + str(tin) + ',' + tx_hash + "\n")
					fileAddressList.write(strAddr + ',' + strAddr + ',Address' + "\n")
					tin = tin + 1
					
		if 'out' in item :
			for xx in item["out"]:
#							print xx["tx_index"]
#							print xx["type"]
#							print xx["addr"]
#							print xx["spent"]
#							print xx["value"]
				try: 
					rec = str(xx["addr"])
					fileOut.write('out_' + str(tout) + ',' + str(xx["tx_index"]) + ',' + str(tx_hash) + ',' + str(xx["type"])  + ",OutgoingPayment"+ "\n");
					fileTransOut.write('trans' + str(xx["tx_index"]) + ',' + 'out_' + str(tout) + ',' + str(xx["spent"]) + ','+ str( Decimal(xx["value"]) / Decimal(100000000.0)) + ',' + 'SENT_COINS' + "\n")
					filePaymentOutAddr.write('out_' + str(tout) + ',' + rec + ',' + str(xx["spent"]) + ','+ str( Decimal(xx["value"]) / Decimal(100000000.0)) + ','+ 'WAS_SENT_TO' + "\n")
					fileAddressList.write(str(rec) + ',' + str(rec) + ',Address' + "\n")
					tout = tout+1
				except KeyError:
					rec = 'Unavailable'


	usock.close()
file.close()
fileIn.close()
fileOut.close()
fileTransList.close()
fileBlockTrans.close()
fileTransInRels.close()
filePaymentOutAddr.close()
filePaymentInAddr.close()
fileAddressList.close()
fileBlockList.close()
f.close();
print "Done"



