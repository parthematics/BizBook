import requests
from bs4 import BeautifulSoup
import re
import os
import csv

files = [f for f in os.listdir('./d') if os.path.isfile(f)]
files = [f for f in files if (f[-4:] == ".htm" or f[-5] == ".html")]
files.sort()

output = open('output.csv', mode='w')
output_writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
for file in files:

    f = open(file, "r")


    content = BeautifulSoup(f.read())


    compilation = open("results.csv", "a")

    links = content.find_all("a", href=re.compile("^/search/principal.investors/field/organizations/num_investors"))

    category_links = content.find_all("a", href=re.compile("^/search/organizations/field/organizations/categories/"))

    location_links = content.find_all("a", href=re.compile("^/search/organizations/field/organizations/location_group_identifiers/"))

    external_links = content.find_all("a", rel="nofollow noopener noreferrer")

    descriptions = content.find_all("p")




    categories = ""
    for link in category_links:
        categories += link.contents[0] + " "

    location = ""
    for link in location_links:
        location += link.contents[0] + " "

    external = ""
    for link in external_links:
        external += link['href'] + " "

    natural_language = ""
    for text in descriptions:
        if text.contents:
            natural_language += str(text.contents[0]) + " "

    output_writer.writerow([categories, location, external, natural_language])





#print(links)
#prefix = "/en/ais/details/ships/shipid"


#links = [a for a in links if href=lambda x: x and x.startswith(prefix))]

#print(divtags['href'])
#for item in divtags:
    #print(item['href'])
    #if "Number of Investors" in str(item):
        #print("FOUND")
    #length = len(atags)
    #links = company_tables
    #for i in range(0, length):
        #links.append(atags[i]['href'])


        #companies = [x for x in links if x[:14] == "/organization/"]

        #compilation = open("links.txt", "a")
        #for company in companies:
            #compilation.write("https://www.crunchbase.com" + company + "\n")
