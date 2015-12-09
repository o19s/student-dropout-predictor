from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError

es = Elasticsearch()

def createIndex():

    settings = {
        "settings": {
            "number_of_shards": 1
        },
        "mappings": {
            "student": {
                "properties": {
                    "BYINCOME": {
                        "type": "integer"
                    },
                    "BYSIBHOM": {
                        "type": "integer"
                    }
                }
            }
        }
    }
    es.indices.delete('els', ignore=[400,404])
    es.indices.create('els', body = settings)




def indexElsCsv(csvPath):

    from csv import DictReader

    dr = DictReader(open(argv[1]))
    idx = 0
    for idx, row in enumerate(dr):
        if idx % 10000 == 0:
            print "Indexed %s" % idx
        student = {'STU_ID': row['STU_ID'],
                   'BYSIBHOM': int(row['BYSIBHOM']),
                   'BYMOTHED': int(row['BYMOTHED']),
                   'BYFATHED': row['BYFATHED'],
                   'BYMATHSE': row['BYMATHSE'],
                   'BYENGLSE': row['BYENGLSE'],
                   'BYINCOME': int(row['BYINCOME']),
                   'F1DOSTAT': row['F1DOSTAT']}
        es.index('els', doc_type='student', id=row['STU_ID'], body=student)
    print idx

if __name__ == "__main__":
    try:
        createIndex()
        from sys import argv
        indexElsCsv(argv[1])
    except TransportError as e:
        print e.info
