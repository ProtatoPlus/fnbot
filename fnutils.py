import requests

def getcurrentshop():
    dailshop = requests.get('https://fortnite-api.com/v2/shop/br/combined')
    shopjson = dailshop.json()
    basepathshop = shopjson['data']
    featpath = basepathshop['featured']
    featentries = featpath['entries']
    dailypath = basepathshop['daily']
    dailyentries = dailypath['entries']
    itemnames = []
    for i in dailyentries:
        idpath = i['items']
        for x in idpath:
            itemnames.append(x['name'])
    for i in featentries:
        idpath = i['items']
        for x in idpath:
            itemnames.append(x['name'])
    return(itemnames)

def getdaily():
    dailshop = requests.get('https://fortnite-api.com/v2/shop/br/combined')
    shopjson = dailshop.json()
    basepathshop = shopjson['data']
    dailypath = basepathshop['daily']
    dailyentries = dailypath['entries']
    itemnames = []
    for i in dailyentries:
        idpath = i['items']
        for x in idpath:
            itemnames.append(x['name'])
    return(itemnames)

def getcos(id):
    req = requests.get('')