
from elasticsearch import Elasticsearch

es = Elasticsearch()


from sys import argv

query = {
    "query": {
        "bool": {
            "must": [
                #{"match": {
                #    "BYSIBHOM": argv[1]
                #}},
                {
                 "match": {
                    "BYINCOME": argv[1]
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
print "Total: %s " % res['hits']['total']
total = res['hits']['total']

for bucket in res['aggregations']['dropouts']['buckets']:
    if bucket['key'] == '1':
        docCount = int(bucket['doc_count'])
        percentage = ((docCount / float(total)) * 100.0)
        print "Dropout %s" % percentage
    if bucket['key'] == '0':
        docCount = int(bucket['doc_count'])
        percentage = ((docCount / float(total)) * 100.0)
        print "Graduated %s" % percentage
