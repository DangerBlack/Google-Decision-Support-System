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
import matplotlib
matplotlib.use('Agg')
import time
#from pygoogle import pygoogle
from pylab import *
#import json
#import urllib
import requests
import io
from unicodedata import normalize
import base64
import urllib
import random as r
import logging

logging.basicConfig(filename='superbot_query.log',level=logging.INFO,format='%(asctime)s - %(levelname)s: %(message)s')

def requestQuery(query):
    header = {'user-agent': 'contnent-Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0'}
    try:
        res = requests.get('https://www.google.it/search?q='+query+'&gws_rd=cr,ssl&ei=odOnVsHMBcKke7jerogD',
            headers=header
        )

        #print(res.encoding);
        res.encoding='utf-8'
        text=res.text
        idx=text.find('<div id="result-stats">')+len('<div id="result-stats">')
        fidx=text.find('<nobr>',idx)
        textfound=text[idx:fidx]
        print(textfound)
        field=textfound.split(' ')
        if(len(field)>2):
            results=field[1]
        else:
            results=field[0]

        # Temp solution to make it work
        try:
            results = results.replace('.','')
        except:
            results = str.replace(results,'.','')

        print(results)
    except requests.exceptions.ConnectionError:
        results = 0
    #print(results)
    return int(results)

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

    imgdata = io.BytesIO()
    savefig(imgdata, bbox_inches='tight')
    imgdata.seek(0)
    clf()
    #img = imgdata.read()
    '''string = base64.b64encode(img)
    try:
        uri = 'data:image/png;base64,' + urllib.quote(string)
    except:
        uri = "error"'''
    #clf()
    return imgdata
    #show()

def splitQuery(string_query):
    query=[]
    for line in string_query.split('\n'):
        print(line)
        if(line!=''):
            if(not line[0]=='-'):
                query=([line+" ",[]])
            else:
                query[1].append(line[1:])

    return query

def printBigNumber(number):
    if(number>1000):
        number = str(number)[:-3]+"k"
    else:
        number = str(number)
    return number

def searchComplete(head, tails, loadingCallback):
    title = head.strip()+" "
    if len(tails) > 1 :
        labels = tails
        values = []
        for idx,option in enumerate(labels):
            query=str.replace((title+option.strip()),' ','+')
            query="\""+query+"\""
            res=requestQuery(query)
            print(title+option+" "+str(res))
            logging.info('Result: '+title+option+" "+str(res))
            values.append(res)
            labels[idx] = labels[idx] +" ("+printBigNumber(res)+")"
            loadingCallback()
            time.sleep(r.randint(1,5))
        return plotAPie(title,labels,values)
    else:
        return None

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

'''
if len(sys.argv) < 2:
    fd = sys.stdin
else:
    fd = open(sys.argv[1], "r")

query=readFileOfQuery(fd)
for q in query:

    res=searchComplete(titles,labels)
'''
