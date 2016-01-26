# _*_ coding:utf-8 _*_
'''
	This file is part of Google Decision Support System.
	Google Decision Support System is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.
	Google Decision Support System is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.
	You should have received a copy of the GNU General Public License
	along with Google Decision Support System.  If not, see <http://www.gnu.org/licenses/>.

	@author DangerBlack
	@version 1.0

'''
import time
#from pygoogle import pygoogle 
from pylab import *
#import json
#import urllib
import requests
from unicodedata import normalize

def requestQuery(query):
	header = {'user-agent': 'contnent-Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0'}
	res = requests.get('https://www.google.it/search?q='+query+'&gws_rd=cr,ssl&ei=odOnVsHMBcKke7jerogD',
		headers=header
	)
	#print(res.encoding);
	text=res.text.encode('utf-8')
	idx=text.find('<div id="resultStats">')+len('<div id="resultStats">')
	fidx=text.find('<nobr>',idx)
	textfound=text[idx:fidx]
	print(textfound)
	field=textfound.split(' ')
	if(len(field)>2):
		results=field[1]
	else:
		results=field[0]
	results=str.replace(results,'.','')
	print(results)
	#print(results)
	return int(results)
	
'''
def showsome(searchfor):
  query = urllib.urlencode({'q': searchfor})
  url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s&rsz=large' % query
  search_response = urllib.urlopen(url)
  search_results = search_response.read()
  results = json.loads(search_results)
  data = results['responseData']
  res=data['cursor']['estimatedResultCount']
  return res


def getNumberOfResult(query):
	g = pygoogle(query) 
	g.pages = 5 
	return g.get_result_count();
'''

def plotAPie(titles,labels,values):
	figure(1, figsize=(6,6))
	ax = axes([0.1, 0.1, 0.8, 0.8])
	#explode=(0, 0.05, 0, 0)
	explode=[]
	for q in labels:
		explode.append(0)
	pie(values, explode=explode, labels=labels,
					autopct='%1.1f%%', shadow=True, startangle=90)
	title(titles)
	
	savefig(titles+labels[0]+'.png', bbox_inches='tight')
	clf()
	#show()

def searchComplete(title,lables):
	values = []
	for option in labels:
		query=str.replace((title+option),' ','+')
		query="\""+query+"\""
		res=requestQuery(query)
		print(title+option+" "+str(res))
		values.append(res)
		time.sleep(5)
	plotAPie(title,labels,values)

def readFileOfQuery(filename='query.txt'):
	in_file = open(filename,"r")
	listQuery = in_file.read()
	in_file.close()
	query=[]
	count=-1
	for line in listQuery.split('\n'):
		print(line)
		if(line!=''):
			if(not line[0]=='-'):
				query.append([line+" ",[]])
				count=count+1
			else:
				query[count][1].append(line[1:])
	
	for q in query:
		titles=q[0]
		labels=q[1]
	return query

		
#titles="I like girls with "
#labels = ['blonde hair', 'black hair', 'red hair', 'brown hair']
#values =[ 78,15,22,36]
#plotAPie(titles,labels,values) #usage raw plotter
#searchComplete(title,labels) #usage raw searcher
#readFileOfQuery() #usage raw query reader


'''THE QUERY FILE MUST BE SAVED IN A FILE NAMED AS query.txt
in this file you had to put

text of some query
-first ending
-second ending
-third ending
-fourht ending

you must have four query add random word if you want make them unused
'''

query=readFileOfQuery()
for q in query:
	titles=q[0]
	labels=q[1]
	res=searchComplete(titles,labels)
		
