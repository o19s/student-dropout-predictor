from elasticsearch import Elasticsearch

es = Elasticsearch()


from sys import argv
from csv import DictReader

dr = DictReader(open(argv[1]))
idx = 0
for idx, row in enumerate(dr):
    if idx % 10000 == 0:
        print "Indexed %s" % idx
    student = {'STU_ID': row['STU_ID'],
               'BYSIBHOM': row['BYSIBHOM'],
               'F1DOSTAT': row['F1DOSTAT']}
    es.index('els', doc_type='student', id=row['STU_ID'], body=student)
print idx
