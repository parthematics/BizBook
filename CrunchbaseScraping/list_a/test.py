import requests
from bs4 import BeautifulSoup
import re
import os

files = [f for f in os.listdir('.') if os.path.isfile(f)]
files = [f for f in files if f[-4:] == ".htm"]
files.sort()

print(files)

for file in files:

    f = open(file, "r")

    content = BeautifulSoup(f.read())

    atags = content.find_all('a')
    length = len(atags)
    links = []
    for i in range(0, length):
        links.append(atags[i]['href'])


        companies = [x for x in links if x[:14] == "/organization/"]

        compilation = open("links.txt", "a")
        for company in companies:
            compilation.write("https://www.crunchbase.com" + company + "\n")
