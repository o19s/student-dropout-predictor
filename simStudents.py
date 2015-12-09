from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError

es = Elasticsearch()


from sys import argv

mostSimilar = 250

incomeCategories = [None, "None", "$1000 or less", "$1001-$5000", "$5001-10000", "$10001-$15000", "$15001-$20000", "$20001-25000",
                    "$25001-$35000", "$35001-$50000", "$50001-$75000", "$75001-$100000", "$100001-$200000", "> $200000"]

query = {
    "query": {
        "function_score": {
            "functions": [
                {"gauss": {
                    "BYINCOME": {
                        "origin": int(argv[1]),
                        "scale": 1,
                        "decay": 0.9
                    }
                }},
                {"gauss": {
                    "BYSIBHOM": {
                        "origin": int(argv[2]),
                        "scale": 1,
                        "decay": 0.9
                    }
                }}
            ]
        }
    },
    "aggs" : {
        "dropoutsTopN": {
            "sampler": {
                "shard_size": mostSimilar
            },
            "aggs": {
                "dropouts" : {
                    "terms" : { "field" : "F1DOSTAT" }
                },
                "income": {
                    "terms": {"field": "BYINCOME"}
                },
                "siblings": {
                    "terms": {"field": "BYSIBHOM"}
                },
                "mathSelfEfficacy": {
                    "terms": {
                        "field": "BYMATHSE",
                        "order": {"_term": "desc"}
                    }
                }
            }
        },
    },
    'size': 5
}

try:
    res = es.search(index='els', doc_type='student', body=query)
except TransportError as e:
    print e.info
for idx, hit in enumerate(res['hits']['hits']):
    print "%s,%s,%s" % (idx,hit['_score'], hit['_source'])
#print "Total: %s " % res['hits']['total']
total = res['hits']['total']

print ""
print "DROPOUTS FOR %s MOST SIMILAR TO INCOME %s SIBLINGS %s" % (mostSimilar, incomeCategories[int(argv[1])], argv[2])

for bucket in res['aggregations']['dropoutsTopN']['dropouts']['buckets']:
    if bucket['key'] == '1':
        docCount = int(bucket['doc_count'])
        percentage = ((docCount / float(mostSimilar)) * 100.0)
        print "Dropout %s" % percentage
    if bucket['key'] == '0':
        docCount = int(bucket['doc_count'])
        percentage = ((docCount / float(mostSimilar)) * 100.0)
        print "Graduated %s" % percentage

print ""
print "INCOME OF %s MOST SIMILAR STUDENTS" % mostSimilar

for bucket in res['aggregations']['dropoutsTopN']['income']['buckets']:
    print "%s,%s" % (incomeCategories[int(bucket['key'])], bucket['doc_count'])

print ""
print "NUM SIBLINGS OF %s MOST SIMILAR STUDENTS" % mostSimilar

for bucket in res['aggregations']['dropoutsTopN']['siblings']['buckets']:
    print "%s,%s" % (bucket['key'], bucket['doc_count'])

print ""
print "MATH SELF EFFICACY PROFILE"
for bucket in res['aggregations']['dropoutsTopN']['mathSelfEfficacy']['buckets']:
    print "%s,%s" % (bucket['key'], bucket['doc_count'])
