
from elasticsearch import Elasticsearch

es = Elasticsearch()


from sys import argv

query = {
    "query": {
        "match": {
            "BYSIBHOM": argv[1]
        }
    },
    'size': 100
}

res = es.search(index='els', doc_type='student', body=query)
print res['hits']['hits'][0]['_source']
print len(res['hits']['hits'])
for hit in res['hits']['hits']:
    print hit['_source']
