import csv
import os
from rdflib import Graph, URIRef
import shutil
import rdflib


result = './result/'
result2 ='./creators/'
shutil.rmtree(result2, ignore_errors=True)
os.makedirs(result2, exist_ok=True)



urls = ['mauritshuis',
        'museum-de-fundatie',
        'catharijneconvent',
        'stedelijk-museum-schiedam',
        'van-abbe-museum',
        'museum-belvedere',
        'rijksakademie',
        'moderne-kunst-museum-deventer']

for url in urls:
    gPath = f'./result/{url}.ttl'
    g = Graph()
    g.parse(gPath, format("ttl"))
    print(url + " Parsed successfully")

    getByIdentifiers = """
    SELECT DISTINCT ?a ?b
    WHERE {
        ?a <http://purl.org/dc/elements/1.1/creator> ?b .
    
    }"""

    qres = g.query(getByIdentifiers)

    with open(result2 + f'creatorForEnrichment_{url}.csv', 'w', encoding='utf-8') as f:
            for row in qres:
                sub = row.a.split("/n")
                obj = row.b.split("/n")
                writer = csv.writer(f, delimiter=',')
                writer.writerows(zip(sub, obj))