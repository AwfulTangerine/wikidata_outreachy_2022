# Import modules
import requests
import urllib.request
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import pywikibot


# 0. Load Pywikibot & Wikidata site
site = pywikibot.Site('wikidata:wikidata', user='Jiehui Ma')
repo = site.data_repository()


# 1. Automatically fetch Bibcode urls from ADS website
def article_topic_extractor(qid):
    article_item = pywikibot.ItemPage(repo, qid)
    return article_item['labels']['en']

def get_bibcode_url(qid):
    '''
    Directly get the url from Wikidata article page without manually copy-pasting.
    If the 'ADS Bibcode' identifier already in article item page, generate the url directly.
    If not: 
    1) Redirect to ADS official website; 
    2) Search ADS Bibcode by article title,
    3) Generate url based on the fetched Bibcode,
    4) Add the identifier into the article item page.
    '''
    article_item = pywikibot.ItemPage(repo, qid)
    claims = article_item.get(u'claims')
    if 'P819' in claims['claims']:
        bibcode_in_wikidata = claims['claims']['P819'][0].target
        url = "https://ui.adsabs.harvard.edu/abs/" + bibcode_in_wikidata + "/exportcitation"
    else:
        print("No ADS bibcode identifiers stored on the item page.")
        print("Directly fetch bibcode on ADS official website:")
        # Use NASA's ADS API to search bibcode by article's title,
        # developed based on ADS official documentation. See: https://github.com/adsabs/adsabs-dev-api/blob/master/examples/search_and_export.ipynb 
        token = "GWyxadCns4nOvfDDthxDP4NloEXkTuWzamSMqPo8"
        query = article_topic_extractor(qid)
        encoded_query = urlencode({'q': query, 'fl': 'bibcode'})
        try:
            results = requests.get("https://api.adsabs.harvard.edu/v1/search/query?{}".format(encoded_query), headers={'Authorization': 'Bearer ' + token})
            fetched_bibcode = list(results.json()['response']['docs'][0].values())[0]
        except:
            print("No articles found in ADS database.")
        # Add 'ADS bibcode' identifier
        bibcode_claim = pywikibot.Claim(repo, u'P819')
        bibcode_claim.setTarget(fetched_bibcode)
        article_item.addClaim(bibcode_claim, summary=u'Added ADS Bibcode identifier')  
        url = "https://ui.adsabs.harvard.edu/abs/" + fetched_bibcode + "/exportcitation"
    return url


# 2. Designed the function to clean author information in bibcode
def get_bibtex_author(qid):
    '''
    Returns a big list with each author name stored a small list inside.
    '''
    # Fetch bibtex string from the url, using BeautifulSoup library
    loaded_url = urllib.request.urlopen(get_bibcode_url(qid))
    soup = BeautifulSoup(loaded_url, 'html.parser')
    bibtex_raw = soup.find("textarea", {"class":"export-textarea form-control"}).text
    # Clean the raw bibtex string to dig author info
    str1 = bibtex_raw.split("author = ")[1]
    str2 = str1.split("title")[0]
    str3 = str2[:-11][2:]
    return list(x.split("}, ") for x in str3.split(" and {"))


# 3. Match bibtex author information (cleaned before) with Wikidata authors
# 3.1 Get author's serial number as the matching index
def serial(author):
    serial_num = author.qualifiers.get('P1545')[0].target
    return(int(serial_num))

# 3.2 The function for adding 'author first names' & 'author family names' qualifiers
def add_qualifiers(author, pid, target):
    if pid not in author.qualifiers:
        qualifier = pywikibot.Claim(repo, pid)
        qualifier.setTarget(target)
        author.addQualifier(qualifier, summary=u'Added author last names qualifiers.')
    else:
        print("Qualifier already existed.")
    return 1

# 3.3 The main matcher function
def author_name_matcher(qid):
    article_item = pywikibot.ItemPage(repo, qid)
    claims = article_item.get(u'claims')
    bibtex_author = get_bibtex_author(qid)
    if 'P50' in claims['claims']:
        author_as_item = claims['claims']['P50']
    else:
        author_as_item = []
    if 'P2093' in claims['claims']:   
        author_as_string = claims['claims']['P2093']
    else:
        author_as_string = []
    author_combined = author_as_item + author_as_string
    for author in author_combined:
        try:
            p50_value = author.getTarget()
            p50_item_dict = p50_value.get()
            author_name = p50_item_dict['labels']['en']
            print(f"For author {serial(author)}, Wikidata stated as: {author_name}")
        except:
            author_name_string = author.getTarget()
            print(f"For author {serial(author)}, Wikidata stated as: {author_name_string}")
        for i in range(0,10):
            if (i == (serial(author)-1)):
                print("BiBTeX stated as: " + str(bibtex_author[i])[1:-1].replace("'",""))
                bibtex_first_name = str(bibtex_author[i][1])
                bibtex_last_name = str(bibtex_author[i][0].replace("'",""))
                add_qualifiers(author, 'P9687', bibtex_first_name)
                add_qualifiers(author, 'P9688', bibtex_last_name)
        else:
            continue
    return 1
    
# Try article "Q60560235":
author_name_matcher("Q60560235")
