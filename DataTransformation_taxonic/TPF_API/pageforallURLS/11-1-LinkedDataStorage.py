import os
import shutil
import requests
import rdflib


urls = ['https://data.collectienederland.nl/fragments/mauritshuis',
       'https://data.collectienederland.nl/fragments/van-abbe-museum']

gPage = rdflib.Graph()
for url in urls:
    gPage.parse(url)
    pageLimit = """
    SELECT DISTINCT ?b
    WHERE {
        ?a <http://www.w3.org/ns/hydra/core#itemsPerPage> ?b .
    
    }"""
    qresforpage = gPage.query(pageLimit)
    for row in qresforpage:
        print("this is page number:",type(int(row.b)))

result = "./result_API/"

for url in urls:
    name = url.split("/")[-1]
    pageCount = 1
    # pageLimit = int(row.b)
    pageLimit = 5
    g_all = rdflib.Graph()
    folder = result + name + "/"
    shutil.rmtree(folder, ignore_errors=True)
    os.makedirs(folder, exist_ok=True)
    try:
        while pageCount < pageLimit:
            current_page_url = url + '?page=' + str(pageCount)
            print(f'Currently fetching page {current_page_url}')
            response = requests.get(current_page_url)
            if response.status_code != 200:
                break
            with open(folder + name + f'_page_{pageCount}.ttl', 'w', encoding='utf-8') as f:
                f.write(response.text)
            g2 = rdflib.Graph()
            g_all += g2.parse(folder + name+ f'_page_{pageCount}.ttl', format='ttl', encoding='utf-8')
            pageCount += 1
            # print(len(g_all))
    except Exception as e:
        print("There is not more pages. please check that last page in your folder.", str(e))


g3 = rdflib.Graph()
g3.parse("./result_API/mauritshuis/mauritshuis_page_1.ttl")
#
objectofdatabirth = """
SELECT DISTINCT ?a ?b
WHERE {
    ?a <http://schemas.delving.eu/nave/terms/creatorYearOfBirth> ?b .

}"""

qres = g3.query(objectofdatabirth)
# print("this is gresssssssssssssss:", qres)
for row in qres:
    print(f"{row.a} hasObjectBirth {row.b}")
