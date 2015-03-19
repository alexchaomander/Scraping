from bs4 import BeautifulSoup
from soupselect import select
from progress.bar import Bar
from soupselect import select
import csv
import os
import re
import sys

# Get all the files from the current directory
allFiles = os.listdir(".")
#bar = Bar('Processing', max=len(allFiles))

#Returns whether or not a string contains any numbers
def contain_numbers(s):
	return bool(re.match(".*\\d.*", s))

def get_data(currentSoup, tag, attributes):
	return currentSoup.find_all(tag, attributes)

def irrelevant_info(s):
	phoneNumber = "^[2-9]\d{2}-\d{3}-\d{4}$"
	cityStateZip = "[A-Za-z\s\-]+,\s?[A-Za-z]{2}\s(\d{5}|[A-Za-z0-9]{3}\s?[A-Za-z0-9]{3})"
	phoneNumber2 = "^[2-9]\d{2}-\d{3}-\w{4}$"
	address = "\d{1,5}\w.*"
	poBox = "P.O.\sBox\s\d*"
	suite = "Suite\s\d*"
	boulevard = ".* Boulevard"

	return bool(re.match(phoneNumber, s)) or bool(re.match(cityStateZip, s)) \
		or bool(re.match(phoneNumber2, s)) or bool(re.match(address, s)) \
		or bool(re.match(poBox, s)) or bool(re.match(suite, s)) or bool(re.match(boulevard, s))

products = []

model_number_attr = {
	'align': 'left',
    'valign': 'top',
    'width': '45%'
}

rated_capacity_attr = {
	'align': 'left',
	'valign': 'top',
	'width': '35%'
}

classification_attr = {
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

table_attr = {
	'width': '100%',
	'cellspacing':'0',
	'cellpadding':'0',
	'border':'0'
}

products = {}
products['Model Number'] = []
products['Rated Capacity'] = []
products['Classification'] = []
products['Company'] = []
products['Facilities'] = []
products['Certification'] = []
product_count_list = []
facility_count_list = []

for i in range(len(allFiles)):

	with open(allFiles[i], 'r') as f:

		html = f.read()

		soup = BeautifulSoup(html)

		#trade_links = soup.select("tr td")
		trade_links = soup.select('tr td')
		company_links = get_data(soup, 'font', company_attr)
		facility_links = get_data(soup, 'font', facility_attr)

		company_count = 0

		for link in trade_links:
			text = link.get_text()
			if contain_numbers(text):
				if not irrelevant_info(text):
					products['Model Number'].append(text)
					company_count += 1

		for link in company_links:
			text = link.get_text()
			for _ in range(company_count):
				if text not in products.keys():
					products['Company'].append(text)

		for link in facility_links:
			text = link.get_text()
			products['Facilities'].append(text)

		for _ in range(company_count):
			products['Certification'].append('NSF/ANSI 40')

  		#bar.next()
#bar.finish()

print ""

print "Model Number: " + str(len(products['Model Number']))
print "Company: " + str(len(products['Company']))
print "Facility: " + str(len(products['Facilities']))
print "Certification: " + str(len(products['Certification']))

# ########## WRITING TO CSV ##############

print "Writing to csv: "
writingBar = Bar('Processing', max=len(products['Model Number']))

f = csv.writer(open("../data/wasteWaterTreatmentSystems.csv", "w"))
f.writerow(["Model Number", "Company", "Facility", "Certification"])    # Write column headers as the first line
for i in range(len(products['Model Number'])):
	model = products['Model Number'][i].encode('utf-8')
	company = products['Company'][i].encode('utf-8')
	if i < len(products['Facilities']):
		facilities = products['Facilities'][i].encode('utf-8')
	else:
		facilities = 'N/A'
	certification = products['Certification'][i].encode('utf-8')
	f.writerow([model,company,facilities,certification])
	writingBar.next()
writingBar.finish()