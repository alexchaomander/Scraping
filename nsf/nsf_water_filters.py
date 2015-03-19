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

trade_name_attr = {
	'align': 'left',
    'valign': 'top',
    'width': '200'
}

replacement_element_attr = {
	'align': 'center',
	'valign': 'top',
	'width': '95'
}

service_cycle_attr = {
	'align': 'center',
	'valign': 'top',
	'width': '50'
}

flow_rate_attr = {
	'align': 'center',
	'valign': 'top',
	'width': '75'
}

claim_attr = {
	'align': 'left',
	'valign': 'top',
	'width': '225'
}

company_attr = {
	'size': '+2'
}

facility_attr = {
	'size': '+1'
}

products = {}
products['Trade Name'] = []
products['Replacement Element'] = []
products['Service Cycle'] = []
products['Flow Rate'] = []
products['Claim'] = []
products['Company'] = []
products['Facilities'] = []
products['Certification'] = []
product_count_list = []
facility_count_list = []

for i in range(len(allFiles)):

	with open(allFiles[i], 'r') as f:

		html = f.read()

		soup = BeautifulSoup(html)

		trade_links = get_data(soup, 'td', trade_name_attr)
		replacement_element_links = get_data(soup, 'td', replacement_element_attr)
		service_cycle_links = get_data(soup, 'td', service_cycle_attr)
		flow_rate_links = get_data(soup, 'td', flow_rate_attr)
		claim_links = get_data(soup, 'td', claim_attr)
		company_links = get_data(soup, 'font', company_attr)
		facility_links = get_data(soup, 'font', facility_attr)
		facility_count_list.append(len(facility_links))

		company_count = 0

		for link in trade_links:
			text = link.get_text()
			if text not in products.keys():
				products['Trade Name'].append(text)
				company_count += 1

		product_count_list.append(company_count)
		for link in replacement_element_links:
			text = link.get_text()
			if text not in products.keys():
				products['Replacement Element'].append(text)

		for link in service_cycle_links:
			text = link.get_text()
			if text not in products.keys():
				if text != "(gallons)":
					if text == "" or text == " ":
						products['Service Cycle'].append('N/A')
					else:
						products['Service Cycle'].append(text)

		for link in flow_rate_links:
			text = link.get_text()
			if text not in products.keys():
				if text != "(gpm)":
					if text == "" or text == " ":
						products['Flow Rate'].append('N/A')
					else:
						products['Flow Rate'].append(text)

		for link in claim_links:
			text = link.get_text()
			if text not in products.keys():
				if text == "" or text == " ":
					products['Claim'].append('N/A')
				else:
					products['Claim'].append(text)

		for link in company_links:
			text = link.get_text()
			for _ in range(company_count):
				if text not in products.keys():
					products['Company'].append(text)

		for link in facility_links:

			text = link.get_text()
			if i < len(facility_count_list):
				for _ in range(facility_count_list[i]):
					products['Facilities'].append(text)

		for _ in range(company_count):
			products['Certification'].append('NSF/ANSI 42')

  		bar.next()
bar.finish()

print " "

# print "Doing facilities:"
# facilities_bar = Bar('Processing', max=len(allFiles))
# for i in range(len(allFiles)):

# 	with open(allFiles[i], 'r') as f:

# 		html = f.read()

# 		soup = BeautifulSoup(html)

# 		facility_list = html.split('</table><br>')

# 		for facility in facility_list:
# 			#print facility
# 			soup = BeautifulSoup(facility)
# 			trade_links = get_data(soup, 'td', trade_name_attr)
# 			facility_links = get_data(soup, 'font', facility_attr)

# 			facility_count = 0
# 			for link in trade_links:
# 				text = link.get_text()
# 				if text not in products.keys():
# 					facility_count += 1

# 			for link in facility_links:
# 				for _ in range(facility_count):
# 					text = link.get_text()
# 					products['Facilities'].append(text)
#   		facilities_bar.next()
# facilities_bar.finish()

print "Trade Name: " + str(len(products['Trade Name']))
print "Replacement Element: " + str(len(products['Replacement Element']))
print "Service Cycle: " + str(len(products['Service Cycle']))
print "Flow Rate: " + str(len(products['Flow Rate']))
print "Claim: " + str(len(products['Claim']))
print "Company: " + str(len(products['Company']))
print "Facility: " + str(len(products['Facilities']))
print "Certification: " + str(len(products['Certification']))

print ""
#print products['Claim']
########## WRITING TO CSV ##############

print "Writing to csv: "
writingBar = Bar('Processing', max=len(products['Claim']))

f = csv.writer(open("../data/water_filters.csv", "w"))
f.writerow(["Trade Name", "Replacement Element", "Service Cycle", "Flow Rate", "Claim", "Company", "Facility", "Certification"])    # Write column headers as the first line
for i in range(len(products['Claim'])):
	if i < len(products['Trade Name']):
		trade = products['Trade Name'][i].encode('utf-8')
	else:
		trade = 'N/A'
	if i < len(products['Replacement Element']):
		replacement = products['Replacement Element'][i].encode('utf-8')
	else:
		replacement = 'N/A'
	if i < len(products['Service Cycle']):
		service = products['Service Cycle'][i].encode('utf-8')
	else:
		service = 'N/A'
	if i < len(products['Flow Rate']):
		flow = products['Flow Rate'][i].encode('utf-8')
	else:
		flow = 'N/A'
	if i < len(products['Claim']):
		claim = products['Claim'][i].encode('utf-8')
	else:
		claim = 'N/A'
	if i < len(products['Company']):
		company = products['Company'][i].encode('utf-8')
	else:
		company = 'N/A'
	if i < len(products['Facilities']):
		facilities = products['Facilities'][i].encode('utf-8')
	else:
		facilities = 'N/A'
	if i < len(products['Certification']):
		certification = products['Certification'][i].encode('utf-8')
	else:
		certification = 'N/A'
	f.writerow([trade,replacement,service, flow, claim,company,facilities, certification])
	writingBar.next()
writingBar.finish()