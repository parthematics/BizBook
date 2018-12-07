import requests
from bs4 import BeautifulSoup
import re
import os

files = [f for f in os.listdir('.') if os.path.isfile(f)]
files = [f for f in files if f[-4:] == ".htm"]
#files.sort()
total = set()
for file in files:

    f = open(file, "r")

    content = BeautifulSoup(f.read())

    atags = content.find_all('a')
    length = len(atags)
    links = []
    for i in range(0, length):
        links.append(atags[i]['href'])


        companies = [x for x in links if x[:14] == "/organization/"]


        for company in companies:
            total.add(company)


#compilation = open("links0.txt", "a")
total = list(total)
total.sort()

current_file_links = 0
file_number = -1

for company in total:
    if current_file_links == 0:
        file_number += 1
        compilation = open("links" + str(file_number) + ".txt", "a")
    compilation.write(company + "\n")
    current_file_links += 1
    current_file_links = current_file_links % 400
