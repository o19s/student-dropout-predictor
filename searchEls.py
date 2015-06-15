
from elasticsearch import Elasticsearch

es = Elasticsearch()


from sys import argv

query = {
    "query": {
        "bool": {
            "should": [
                {"match": {
                    "BYSIBHOM": argv[1]
                }},
                {
                 "match": {
                     "BYINCOME": argv[2]
                  }
                }
            ]
        }
    },
    "aggs" : {
        "dropouts" : {
            "terms" : { "field" : "F1DOSTAT" }
        }
    },
    'size': 5
}

res = es.search(index='els', doc_type='student', body=query)
print res['hits']['hits'][0]['_source']
print len(res['hits']['hits'])
for hit in res['hits']['hits']:
    print hit['_source']
import json
print json.dumps(res, indent=True)
print "Total: %s " % res['hits']['total']
