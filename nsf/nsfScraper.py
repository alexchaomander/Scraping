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

company_attr = {
	'size': '+2'
}

facility_attr = {
	'size': '+1'
}

products = {}
products['Trade Designation'] = []
products['Product Function'] = []
products['Max Use'] = []
products['Company'] = []
products['Facilities'] = []
product_count_list = []
facility_count_list = []

for i in range(1):

	with open(allFiles[7], 'r') as f:

		html = f.read()

		soup = BeautifulSoup(html)

		print html.split('font size="+1"')


		trade_links = get_data(soup, 'td', trade_designation_attr)
		product_function_links = get_data(soup, 'td', product_function_attr)
		max_use_links = get_data(soup, 'td', max_use_attr)
		company_links = get_data(soup, 'font', company_attr)
		facility_links = get_data(soup, 'font', facility_attr)
		facility_count_list.append(len(facility_links))

		company_count = 0

		for link in trade_links:
			text = link.get_text()
			if text not in products.keys():
				products['Trade Designation'].append(text)
				company_count += 1

		product_count_list.append(company_count)
		for link in product_function_links:
			text = link.get_text()
			if text not in products.keys():
				products['Product Function'].append(text)

		for link in max_use_links:
			text = link.get_text()
			if text not in products.keys():
				products['Max Use'].append(text)

		for link in company_links:
			text = link.get_text()
			for _ in range(company_count):
				if text not in products.keys():
					products['Company'].append(text)

		for link in facility_links:
			text = link.get_text()
			for _ in range(facility_count_list[i]):
				products['Facilities'].append(text)
  		bar.next()
bar.finish()

print "Trade Designation: " + str(len(products['Trade Designation']))
print "Product Function: " + str(len(products['Product Function']))
print "Max Use: " + str(len(products['Max Use']))
print "Company: " + str(len(products['Company']))
print "Facility: " + str(len(products['Facilities']))
print " "
# print products['Trade Designation'][0:20]
# print " "
# print products['Product Function'][0:20]
# print " "
# print products['Max Use'][0:20]
# print " "
# print products['Company'][0:20]
# print " "
#print products['Facilities']
print facility_count_list, sum(facility_count_list), len(facility_count_list)

##SOME COMPANIES HAVE MULTIPLE FACILITIES

#print product_count_list, sum(product_count_list)

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