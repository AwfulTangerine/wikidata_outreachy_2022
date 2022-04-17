# Import modules
import pywikibot
import mwparserfromhell


# 0. Connect to Wikidata repository with my account
site = pywikibot.Site('wikidata:wikidata', user='Jiehui Ma')
repo = site.data_repository()    


# 1. Add text to outreachy homepage
def add_text(text):
    page = pywikibot.Page(site, 'User:Jiehui_Ma/Outreachy_1')
    print(page.text)
    page.save(summary='Test', appendtext='\n' + text)
    return 1
# Try adding 'Hello'
add_text('Hello')


# 2. Print all information from an item page
def print_all_text(qid):
    item = pywikibot.ItemPage(repo, qid)
    print(item.text)
    return 1
# Try printing sandbox
print_all_text('Q4115189')


# 3. Print author information on article item page:
def get_item_cache(qid):
    item = pywikibot.ItemPage(repo, qid)
    cache = item.get()
    return cache

def get_property_label(pid):
    property_page = pywikibot.PropertyPage(repo, pid)
    property_page.get()
    return property_page.labels['en']

def get_qualifiers(claim, pid):
    qualifier_label = get_property_label(pid)
    qualifier_value = claim.qualifiers.get(pid)[0].target
    print(f'{qualifier_label}: {qualifier_value}')
    return 1

def get_name_info(item, pid):
    return item.claims[pid][0].getTarget().labels['en']

def print_all_authors(article_qid):
    article_item = get_item_cache(article_qid)
    print(article_item['labels']['en'])
    # Fetch the author(P50) information
    if 'P50' not in article_item['claims']:
        print('No author stored as items.')
    else:
        for claim in article_item['claims']['P50']:
            # Get author name info & qualifiers
            p50_value = claim.getTarget()
            p50_item_dict = p50_value.get()
            print(f"{get_property_label('P50')}: {p50_item_dict['labels']['en']}")
            get_qualifiers(claim, 'P1545')
            get_qualifiers(claim, 'P1932')
            # Automatically follow links to author's own item page
            author_qid = p50_value.getID()
            item_author = pywikibot.ItemPage(repo, author_qid)
            if item_author.get():
                print('Redirected to item page, fetching author name components...')
            try:
                print(f"{get_property_label('P735')}: {get_name_info(item_author, 'P735')}")
            except:
                print('Given name item page is not in Wikidata.')
            try:
                print(f"{get_property_label('P734')}: {get_name_info(item_author, 'P734')}")
            except:
                print('Family name item page is not in Wikidata.')
    # Fetch the author name string(P2093) information
    if 'P2093' not in article_item['claims']:
        print('No author stored as strings.')
    else:
        for claim in article_item['claims']['P2093']:
            # Get author name string & qualifiers
            p2093_value = claim.getTarget()
            print(f"{get_property_label('P2093')}: {p2093_value}")
            get_qualifiers(claim, 'P1545')
    print("-------------------")
    return 1
# Try printing the author info in several articles
article_qid_list = ['Q60560235','Q69152190','Q104538340','Q59897278']
for article_qid in article_qid_list:
    print_all_authors(article_qid)



"""
逻辑：
1. 获取property （P50） 的 item value （Q值）
2. 根据Q值 redirect 到 item link
"""