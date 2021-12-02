from IPython.core.display import display, HTML
from bs4 import BeautifulSoup as bs
import requests as rq
import pygal
import os
import webbrowser
import pandas as pd
import matplotlib.pyplot as plt
import tempfile
import webbrowser
from itertools import cycle, islice


#Fetch HTML
url = 'https://ranking-empresas.eleconomista.es/'

#Extract HTMl tree
page = rq.get(url).text
soup = bs(page,features="lxml")

#Find companies and quantiy
table = soup.find('table')
top_10_companies = []

for row in table.find_all('tr')[1:11]:
    company_name = row.find('a').text
    fact = row.find_all('td')[3].text
    fact = fact.replace(".","")
    #print(fact)
    #print(company_name)
    top_10_companies.append((company_name,int(fact)))

def fst(x):
	return x[0]
def snd(x):
	return x[1]

df = pd.DataFrame({'turnovers' : map(snd,top_10_companies)}, 
	index=map(fst,top_10_companies))

ax = df.plot(kind='bar',stacked=True,figsize = (10, 5),color=['blue'])
ax.set_xticklabels(ax.get_xticklabels(), rotation=15, ha="right",fontsize=7)
plt.tight_layout()

#plt.show()
plt.savefig("plot.png")

html = '<html> <img src="plot.png" title="My plot" /> </html>'

with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
    url = 'file://' + f.name
    f.write(html)
webbrowser.open(url)

