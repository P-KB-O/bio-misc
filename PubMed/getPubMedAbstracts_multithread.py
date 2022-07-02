import os 
import json 
import csv 
import threading 
from time import sleep 
from collections import defaultdict 

# import eventlet
import requests 
from bs4 import BeautifulSoup 
 
# output = os.path.join('data/pudmed', 'abstracts.csv') 
output = 'data/pudmed' 
 
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
 
 
def get_abstract(retstarts, thd, retmax=60): 
    _file_path = output+'/abstract'+str(thd)+'.csv' 
    # other efetch settings 
    with open(_file_path, "a", newline='') as fw: 
        fw.seek(0) 
        fw.truncate() 
        writer = csv.writer(fw) 
        writer.writerow(['PMID', 'Title', 'Abstract']) 
    for retstart in retstarts: 
        print('thread_{} running, retstart={}\n'.format(thd, retstart)) 
        fetch_eutil = 'efetch.fcgi?' 
        retmax = retmax 
        retstart = retstart 
        fetch_retmode = "&retmode=xml" 
        fetch_rettype = "&rettype=abstract" 
 
        fetch_retstart = "&retstart=" + str(retstart) 
        fetch_retmax = "&retmax=" + str(retmax) 
        fetch_url = base_url + fetch_eutil + db + fetch_querykey + fetch_webenv + fetch_retstart + fetch_retmax + fetch_retmode + fetch_rettype 
 
        fetch_data = None
        # eventlet is not working for MacOS
        # with eventlet.Timeout(20, False):  # in case request outtime
        try:
            ret = requests.get(fetch_url)
            fetch_data = ret.content.decode('utf-8')
        except requests.exceptions.Timeout:
            pass

        if fetch_data is None:
            continue
 
        soup = BeautifulSoup(fetch_data, 'xml') 
        with open(_file_path, "a", newline='') as fw: 
            writer = csv.writer(fw) 
            i = 1 
            for articles in soup.find_all('PubmedArticle'): 
                try: 
                    pmid = articles.find('PMID').text.strip() 
                    title = articles.find('ArticleTitle').text.strip() 
                    abstract = articles.find('AbstractText').text.strip() 
                    if pmid is None or title is None or abstract is None: 
                        continue 
                    else: 
                        i += 1 
                        writer.writerow([pmid, title, abstract]) 
                except Exception: 
                    # print('some thing lack.') 
                    pass 
        sleep(1) 
 
retmax = 600 
retstart = 0 
page_nums = int(int(total_abstract_count) / retmax) 
thd_nums = 10 
 
pools = defaultdict(list) 
for j in range(page_nums): 
    pools[j % thd_nums].append(j*retmax) 
 
for i in range(thd_nums): 
    thd = threading.Thread(target=get_abstract, args=(pools[i], i, retmax)) 
    thd.start()
