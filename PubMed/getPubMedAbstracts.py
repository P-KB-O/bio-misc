import os
import json
import csv
from time import sleep

import requests


"""
here is a brief tutorial about E-utilities

detail information: https://www.ncbi.nlm.nih.gov/books/NBK25499/

EInfo:
    url: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi?retmode=json
    Required: None
    desc: get db information

ESearch:
    url: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=asthma&usehistory=y&retmode=json
    Required: db, term
    desc: get a list of UIDs matching a text query, here we just query for a relative date range,
          https://pubmed.ncbi.nlm.nih.gov/help/#date-search-range

EFetch:
    url: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&query_key=1&WebEnv=MCID_62bc4ff0cb77e24f914f20aa&retmode=json&rettype=abstract
    Required: db, query_key, WebEnv
    desc: get pubmed abstracts

"""


output = os.path.join('data/pudmed', 'abstracts.csv')


query = '"last 10 years"'

# common settings between esearch and efetch
base_url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
db = 'db=pubmed'

# esearch specific settings
search_eutil = 'esearch.fcgi?'
# search_term = '&term=' + query
search_date = '&mindate=1800/01/01&maxdate=2021/12/31'
search_usehistory = '&usehistory=y'
search_rettype = '&retmode=json'

# search_url = base_url+search_eutil+db+search_term+search_usehistory+search_rettype
search_url = base_url+search_eutil+db+search_date+search_usehistory+search_rettype
print('{}\n esearch stage: \n\turl:{}'.format('-'*200, search_url))

ret = requests.get(search_url)
search_data = json.loads(ret.content.decode('utf-8'))

total_abstract_count = search_data['esearchresult']['count']
fetch_querykey = "&query_key=" + search_data['esearchresult']['querykey']
fetch_webenv = "&WebEnv=" + search_data['esearchresult']['webenv']

print('\tparse the return:')

formater = '{:>20s} {:>20s} {:>50s}'
header = ['total abstract count', 'query key', 'webenv']

print(formater.format(*header))
print(formater.format(total_abstract_count, fetch_querykey, fetch_webenv))

# other efetch settings
fetch_eutil = 'efetch.fcgi?'
retmax = 20
retstart = 0
fetch_retmode = "&retmode=text"
fetch_rettype = "&rettype=abstract"

print('{}\n efetch stage: '.format('-'*200))

run = True
item_counter = 0
loop_counter = 1

with open(output, "a") as fw:
    writer = csv.writer(fw)
    writer.writerow(['Journal', 'Title', 'Authors', 'Author_Information', 'Abstract', 'DOI', 'Misc'])

while retstart < int(total_abstract_count):
    print("\tthis is efetch run number " + str(loop_counter))
    loop_counter += 1

    fetch_retstart = "&retstart=" + str(retstart)
    fetch_retmax = "&retmax=" + str(retmax)
    fetch_url = base_url + fetch_eutil + db + fetch_querykey + fetch_webenv + fetch_retstart + fetch_retmax + fetch_retmode + fetch_rettype
    print('\t{}'.format(fetch_url))

    ret = requests.get(fetch_url)
    fetch_data = ret.content.decode('utf-8')
    abstracts = fetch_data.split("\n\n\n")

    item_counter = item_counter + len(abstracts)
    print("\ta total of {} abstracts have been downloaded.\n".format(item_counter))
    retstart = retstart + retmax

    sleep(1)
    with open(output, "a") as fw:
        writer = csv.writer(fw)
        for abstract in abstracts:
            split_abstract = abstract.split("\n\n")
            if len(split_abstract) > 5:  #
                writer.writerow(split_abstract)

