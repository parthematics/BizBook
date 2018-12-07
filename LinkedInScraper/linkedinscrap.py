import sys
import re
import time
import xlsxwriter
import json
import argparse
import requests
import subprocess
import urllib
import math
from thready import threaded
reload(sys)
sys.setdefaultencoding('utf-8')

""" Setup Argument Parameters """
parser = argparse.ArgumentParser(description='LinkedIn')
parser.add_argument('-u', '--keywords', help='Keywords to search')
parser.add_argument('-o', '--output', help='Output file (do not include extentions)')
args = parser.parse_args()

def get_search():
    url = "https://www.linkedin.com/voyager/api/search/cluster?count=40&guides=List(v-%%3EPEOPLE,facetGeoRegion-%%3Ear%%3A0)&keywords=%s&origin=FACETED_SEARCH&q=guided&start=0" % search
    headers = {'Csrf-Token':'ajax:7736867257193100830'}
    cookies['JSESSIONID'] = 'ajax:7736867257193100830'
    cookies['X-RestLi-Protocol-Version'] = '2.0.0'
    r = requests.get(url, cookies=cookies, headers=headers)
    content = json.loads(r.text)
    data_total = content['paging']['total']

    # Calculate pages off final results at 40 results/page
    pages = data_total / 40
    if data_total % 40 == 0:
        pages = pages - 1
    if pages == 0:
        pages = 1

    print "[Info] %i Results Found" % data_total
    if data_total > 1000:
        pages = 24
        print "LinkedIn only allows 1000 results. Refine keywords to capture all data"
    print "[Info] Fetching %i Pages" % pages
    print

    # Set record position for XLSX
    recordpos = 1

    for p in range(pages):
        # Request results for each page using the start offset
        url = "https://www.linkedin.com/voyager/api/search/cluster?count=40&guides=List()&keywords=%s&origin=GLOBAL_SEARCH_HEADER&q=guided&searchId=1489295486936&start=%i" % (search, p*40)
        url = "https://www.linkedin.com/voyager/api/search/cluster?count=40&guides=List(v-%%3EPEOPLE,facetGeoRegion-%%3Ear%%3A0)&keywords=%s&origin=FACETED_SEARCH&q=guided&start=%i" % (search, p*40)
        r = requests.get(url, cookies=cookies, headers=headers)
        content = r.text.encode('UTF-8')
        content = json.loads(content)
        print "[Info] Fetching page %i with %i results" % (p+1,len(content['elements'][0]['elements']))
        for c in content['elements'][0]['elements']:
            try:
                if c['hitInfo']['com.linkedin.voyager.search.SearchProfile']['headless'] == False:
                    try:
                        data_industry = c['hitInfo']['com.linkedin.voyager.search.SearchProfile']['industry']
                    except:
                        data_industry = ""
                    data_firstname = c['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['firstName']
                    data_lastname = c['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['lastName']
                    data_slug = "https://www.linkedin.com/in/%s" % c['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['publicIdentifier']
                    data_occupation = c['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['occupation']
                    data_location = c['hitInfo']['com.linkedin.voyager.search.SearchProfile']['location']
                    try:
                        data_picture = "https://media.licdn.com/mpr/mpr/shrinknp_400_400%s" % c['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['picture']['com.linkedin.voyager.common.MediaProcessorImage']['id']
                    except:
                        #print "[Notice] No picture found for %s %s, %s" % (data_firstname, data_lastname, data_occupation)
                        data_picture = ""

                    # Write data to XLSX file
                    worksheet1.write('A%i' % recordpos, data_firstname)
                    worksheet1.write('B%i' % recordpos, data_lastname)
                    worksheet1.write('C%i' % recordpos, data_occupation)
                    worksheet1.write('D%i' % recordpos, data_location)
                    worksheet1.write('E%i' % recordpos, data_industry)
                    worksheet1.write('F%i' % recordpos, data_slug)
                    worksheet1.write('G%i' % recordpos, data_picture)
                    worksheet2.write('A%i' % recordpos, '=IMAGE(dataset!G%i)' % recordpos)
                    worksheet2.write('B%i' % recordpos, '=dataset!A%i&" "&dataset!B%i&"\n"&dataset!C%i&"\n"&dataset!D%i&"\n"&dataset!E%i' % (recordpos,recordpos,recordpos,recordpos,recordpos))
                    worksheet2.write('C%i' % recordpos, '=HYPERLINK(dataset!F%i)' % recordpos)
                    worksheet2.set_row(recordpos-1,125)
                    recordpos = recordpos + 1
                else:
                    print "[Notice] Headless profile found. Skipping"
            except:
                print "[Notice] Skipping"
                continue
        print

def authenticate():
    try:
        session = subprocess.Popen(['python', 'login.py'], stdout=subprocess.PIPE).communicate()[0].replace("\n","")
        if len(session) == 0:
            sys.exit("[Error] Unable to login to LinkedIn.com")
        print "[Info] Obtained new session: %s" % session
        cookies = dict(li_at=session)
    except Exception, e:
        sys.exit("[Fatal] Could not authenticate to linkedin. %s" % e)
    return cookies

if __name__ == '__main__':
    title = """tool to scrape linkedin"""
    print title.decode('UTF-8')
    search = args.keywords if args.keywords!=None else raw_input("Enter search Keywords\n")
    outfile = args.output if args.output!=None else raw_input("Enter filename for output \n")
    print

    # URL Encode for the querystring
    search = urllib.quote_plus(search)
    cookies = authenticate()

    # Initiate XLSX File
    workbook = xlsxwriter.Workbook('results/%s.xlsx' % outfile)
    worksheet1 = workbook.add_worksheet('dataset')
    worksheet2 = workbook.add_worksheet('report')
    worksheet2.set_column(0,0, 25)
    worksheet2.set_column(1,2, 75)

    # Initialize Scraping
    get_search()

    # Close XLSD File
    workbook.close()
