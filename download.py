#!/usr/bin/env python
#encoding=utf-8

'''
function:it can traversal a website and find the injectable points.
author:jaffer
time:2014-05-15
¹¹¼Ü£ºÅÀ³æÏµÍ³£¬url·ÖÎöÏµÍ³£¬sql×¢ÈëÅÐ¶ÏÏµÍ³£¬±£´æurlÏµÍ³
²âÊÔÖÐµÄbug£ºx-powered-byµÈ·µ»ØµÄÄÚÈÝ²»Ò»¶¨¶¼ÓÐ£¬Èç¹ûÃ»ÓÐµÄ»°£¬³ÌÐò±¨´í¡£Õâ¸öÐèÒª´¦Àí¡£
ÐèÒª¸Ä½øµÄµØ·½£º1¡¢³ÌÐòËÙ¶È£¬¶àÏß³Ì£¿2¡¢Á´½ÓÈç¹û¶ÏÁË£¬¸ÃÈçºÎ±£³ÖÒ»¶ÎÊ±¼äÖØÁ¬£¿3¡¢´úÀíÅÀ³æ£¿
'''
import pdb
import re
import httplib2
import urllib2
import urllib
import os
from sys import argv
from os import makedirs,unlink,sep
from os.path import dirname,exists,isdir,splitext
from string import replace,find,lower
from htmllib import HTMLParser
from urllib import urlretrieve
from urllib import urlopen
from urlparse import urlparse,urljoin
from formatter import DumbWriter,AbstractFormatter
from cStringIO import StringIO
import sys 
import threadpool
import time


pdb.set_trace()

reload(sys) 
sys.setdefaultencoding('utf8')


'''
µÚÒ»¸ö²ÎÊýÊÇurl£¬
µÚ¶þ¸ö²ÎÊýÊÇ´æ·ÅÄ¿Â¼
'''
#downloadÒýÇæ
class download(object):
	def __init__(self,count,path):
		self.count = count
		self.path = path
		#self.threadnum = threadnum

	def getDownloadLink(self,url):
		h = httplib2.Http()
		headers = {
			"Accept-Encoding": "gzip, deflate, sdch",
			"Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
			"Cache-Control": "max-age=0",
			"Connection": "keep-alive",
			"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
			"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0",
			}
		res,con = h.request(url,'GET',headers=headers)
		df = con.find('data_url')
		if df != -1:
			ds = con.find('"',df+11,-1)
			if con[ds-3:ds] == 'apk':
				downurl = con[df+10:ds]
				self.getApk(downurl)
			else:
				dt = con.find('data_url',ds,-1)
				if dt != -1:
					dfo = con.find('"',dt+11,-1)
					if con[dfo-3:dfo] == 'apk':
						downurl = con[dt+10:dfo]
						self.getApk(downurl)

				

	def getApk(self,download_url):
		print download_url+'**********\n'
		apkName = download_url.split('/')[-1]
		print apkName+'--------\n'
		urlretrieve(download_url,self.path+'\\'+apkName)

	def gothread(self):
		#½¨Á¢½ø³Ì³Ø
		#pool = threadpool.ThreadPool(self.threadnum)
		base = '7644000'
		#Á½¸ölistºÏ²¢£¬Ö±½ÓÏà¼Ó¾Í¿ÉÒÔ
		for i in range(self.count):
			url = 'http://shouji.baidu.com/software/item?docid=%s' % str(int(base) + i)
			#pool.add_task(self.getDownloadLink,url)
			self.getDownloadLink(url)
			#time.sleep(1.2)
		#join and destroy all threads
		#pool.destroy()

def usage():
	test = '''
	this program will download apk from http://shouji.baidu.com.
	if you want to download 100 apps,the result maybe less than that.so you can appoint more at first.
	I am not use multithread,because it is something wrong I donot know.just wired.:)
	author:jaffer
	time:4-18-2015
	'''
	print test

def main():
	usage()
	count = raw_input('how many apk do you want to download?\n')
	#threadnum = raw_input('the thread number you want to run:\n')
	path = 'download_path'
	if not os.path.exists(path):
		os.mkdir(path)
	down = download(int(count),path)
	down.gothread()


if __name__ == '__main__':
	main()
	print '\nover \n'
	raw_input()



