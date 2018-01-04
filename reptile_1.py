#!/usr/bin/env python 

from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from urllib.error import HTTPError,URLError
import re
import datetime
import random

pages = set();
random.seed(datetime.datetime.now())
# 获取页面所有内链的列表
def getInternalLinks(bsObj ,inclueUrl) :
	includeUrl = urlparse(includeUrl).scheme +"://"+urlparse(includeUrl).netcol
	internalLinks = []
	# 找出所有以"/"开头的链接
	for link in bsObj.findAll('a',href = re.compile("^(/|.*"+includeUrl+")")) :
		if link.attrs['href'] is not None  and link.attrs['href'] not in internalLinks :
			# 检查字符串是否是以指定子字符串开头
			if link.attrs['href'].startswith("/") :
				internalLinks.append(includeUrl+link.attrs['href'])
			else :
				internalLinks.append(link.arrts['href'])
	return inrenalLinks 
# 获取页面所有外链的列表
def getExternalLinks(bsObj,excludeUrl) :
	externalLinks = []
	# 找出所有以"http"或"www"开头且不包含当前URL的链接
	for link in bsObj.findAll('a',href = re.compile("^(http|www)((?!"+excludeUrl+").)*$")) :
		if link.attrs['href'] is not None :
			if link.attrs['href'] not in externalLinks:
				#externalLinks.append(link.attrs['href']) :
				externalLinks.append(link.attrs['href'])
	return externalLinks 

def splitAddress(address) :
	addressParts = address.replace("http://","").split('/')
	return addressParts

def getRandomExternalLink(startingPage) :
	html = urlopen(startingPage)
	bsObj = BeautifulSoup(html,'lxml')  #  可能会出现SSLError异常
	externalLinks = getExternalLinks(bsObj,splitAddress(startingPage)[0])
	if len(externalLinks) == 0 :
		internalLinks = getInternalLinks(startingPage)
		print ('--------------------\n')
		return getRandomExternalLink(internalLinks[random.randint(0,len(internalLinks)-1)])
	else :
		return externalLinks[random.randint(0,len(externalLinks)-1)]

def followExternalOnly(startingSite) :
	externalLink = getRandomExternalLink("http://oreilly.com")  # 可能会出现SSLError异常
	#随机外链
	print ("Link is  "+externalLink)
	followExternalOnly(externalLink)

followExternalOnly("http://oreilly.com")


