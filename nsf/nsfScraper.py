from bs4 import BeautifulSoup
from progress.bar import Bar
from soupselect import select
import csv
import os
import re
import sys

# Get all the files from the current directory
allFiles = os.listdir(".")
bar = Bar('Processing', max=len(allFiles))

#Returns whether or not a string contains any numbers
def contain_numbers(s):
	return bool(re.match(".*\\d.*", s))

def get_data(currentSoup, tag, attributes):
	return currentSoup.find_all(tag, attributes)

products = []
colnames = []

trade_designation_attr = {
	'align': 'left',
    'valign': 'top',
    'width': '45%'
}

product_function_attr = {
	'align': 'left',
	'valign': 'top',
	'width': '35%'
}

max_use_attr = {
	'align': 'left',
	'valign': 'top',
	'width': '20%'
}

products = {}
products['Trade Designation'] = []
products['Product Function'] = []
products['Max Use'] = []
# For Trade Designation
for i in range(len(allFiles)):
	#print " " + allFiles[i]
	with open(allFiles[i], 'r') as f:
		#print "Before BeautifulSoup"
		soup = BeautifulSoup(f)
		#print "Calling BeautifulSoup"
		trade_links = get_data(soup, 'td', trade_designation_attr)
		product_function_links = get_data(soup, 'td', product_function_attr)
		max_use_links = get_data(soup, 'td', max_use_attr)
		#print "Finding all"
		for link in trade_links:
			text = link.get_text()
			if text not in products.keys():
				products['Trade Designation'].append(text)
		for link in product_function_links:
			text = link.get_text()
			if text not in products.keys():
				products['Product Function'].append(text)
		for link in max_use_links:
			text = link.get_text()
			if text not in products.keys():
				products['Max Use'].append(text)
  		bar.next()
bar.finish()

print "Trade Designation: " + str(len(products['Trade Designation']))
print "Product Function: " + str(len(products['Product Function']))
print "Max Use: " + str(len(products['Max Use']))

print products['Trade Designation'][0:20]
print " "
print products['Product Function'][0:20]
print " "
print products['Max Use'][0:20]


# soup = BeautifulSoup (open("43rd-congress.html"))

# final_link = soup.p.a
# final_link.decompose()

# f = csv.writer(open("43rd_Congress.csv", "w"))
# f.writerow(["Name", "Link"])    # Write column headers as the first line

# links = soup.find_all('a')
# for link in links:
#     names = link.contents[0]
#     fullLink = link.get('href')

#     f.writerow([names,fullLink]