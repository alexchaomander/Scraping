library(rvest)
url <- "http://info.nsf.org/Certified/DWTU/Listings.asp?hdAllPrds=AllProducts&submit5=%C2%A0%C2%A0%C2%A0%C2%A0All+Products"

webpage = html(url) %>%
  html_nodes("html")
fullpage = html_text(webpage)

company_split = html(url) %>%
  html_nodes("hr")
html_text(company_split)

#companies
row = html(url) %>%
  html_nodes("table font[size='+2']")
companies = html_text(row)

#facilities
row = html(url) %>%
  html_nodes("font[size='+1']")
facilities = html_text(row)

#products
row = html(url) %>%
  html_nodes("table td[width='200']")
products = html_text(row)
products = products[products != "N/A"]

#replacement elements
row = html(url) %>%
  html_nodes("table td[width='95']")
replacement_elements = html_text(row)
replacement_elements = replacement_elements[replacement_elements != "N/A"]

#service cycle
row = html(url) %>%
  html_nodes("table td[width='50']")
service_cycle = html_text(row)

#flow rate
row = html(url) %>%
  html_nodes("table td[width='75']")
flow_rate = html_text(row)
flow_rate = flow_rate[flow_rate != "Flow Rate"]
flow_rate = flow_rate[flow_rate != "(gpm)"]
flow_rate = flow_rate[flow_rate != "N/A"]
flow_rate = as.numeric(flow_rate[!is.na(as.numeric(flow_rate))])




library(XML)
url <- "http://info.nsf.org/Certified/DWTU/Listings.asp?hdAllPrds=AllProducts&submit5=%C2%A0%C2%A0%C2%A0%C2%A0All+Products"
pagetree = htmlTreeParse(url, useInternal = TRUE)
docText = unlist(xpathApply(pagetree, '//tr', xmlValue))

###

url = 'http://info.nsf.org/Certified/PwsComponents/Listings.asp?TradeName=&StandardExt=&MaterialType=&ProductType=&PlantState=&PlantCountry=&PlantRegion=&Standard=061'

row = html(url) %>%
  html_nodes("font[size='+2']")
companies= html_text(row)

row = html(url) %>%
  html_nodes("font[size='+1']")
facilities= html_text(row)

#products
row = html(url) %>%
  html_nodes("table tr td")
products = html_text(row)


#replacement elements
row = html(url) %>%
  html_nodes("table td[width='95']")
replacement_elements = html_text(row)


########## Getting companies and facilities #######

url = 'http://info.nsf.org/Certified/PwsComponents/Listings.asp?TradeName=&StandardExt=&MaterialType=&ProductType=&PlantState=&PlantCountry=&PlantRegion=&Standard=061'

row = html(url) %>%
  html_nodes("font[size='+2']")
companies= html_text(row)

row = html(url) %>%
  html_nodes("font[size='+1']")
facilities= html_text(row)

row = html(url) %>%
  html_nodes("div[align='center'] strong")
certification = html_text(row)

a = list(companies, facilities)
a = t(plyr::ldply(a, rbind))
a = as.data.frame(a)
colnames(a) = c("Companies","Facilities")

tables = readHTMLTable(url)
tables[1]



