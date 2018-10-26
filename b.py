import requests
from bs4 import BeautifulSoup
import csv

with open('investors-10-22-2018.csv', 'r') as f:
    reader = csv.reader(f)
    entry_list = list(reader)

investor_to_crunchbasepage = dict()
for item in entry_list:
    investor_to_crunchbasepage[item[0]] = item[1]

#print(investor_to_crunchbasepage)

#for investor in investor_to_crunchbasepage:
page_link = 'https://www.crunchbase.com/organization/500-startups'
page_response = requests.get(page_link, timeout=5)
page_content = BeautifulSoup(page_response.content, "html.parser")
textContent = []

for i in range(0, 2):
    paragraphs = page_content.find_all("p")[i].text
    textContent.append(paragraphs)

print(textContent)
