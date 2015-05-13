import sys, os
import datetime
import cPickle
import operator


def SortnGroup(list_):
    #list_.sort(key=lambda x: x[3])
   
    #get unique entries using dict
    dList = {}
    for l in list_: dList[l[0]] = l[1:]

    sList = dList.items()
    #sort by queue_id
    #sList = sorted(dList.iteritems(), key=operator.itemgetter(1))
    sList = sorted(sList,key=lambda i: i[1][1])
    # then sort by run_id (may not be needed)
    sList = sorted(sList,key=lambda i: i[1][3])
    
    return sList


import MySQLdb
sys.path.append("/net/user/i3filter/SQLServers_n_Clients/npx4/")

try:
    import SQLClient_dbs4 as dbs4
    dbs4_ = dbs4.MySQL()
    
except Exception, err:
    raise Exception("Error: %s "%str(err))

dbInfo = dbs4_.fetchall("""select u.name, u.path, u.queue_id,u.size, r.run_id,u.md5sum from i3filter.urlpath u
                           join i3filter.run r on r.queue_id=u.queue_id
                           where r.dataset_id=1870 and u.dataset_id=1870
                           and u.transferstate="WAITING" """)
                           #order by r.run_id""")




burnSampleL2 = [b for b in dbInfo if not b[4]%10 and b[0].find("PFFilt")<0]
burnSamplePFFilt = [b for b in dbInfo if not b[4]%10 and b[0].find("PFFilt")>=0]
OtherL2 = [b for b in dbInfo if b[4]%10 and b[0].find("PFFilt")<0 and b[0].find("GCD")<0]
OtherPFFilt = [b for b in dbInfo if b[4]%10 and b[0].find("PFFilt")>=0]


Files2Copy = []
# you can change the copying priority by changing the order that each group is added to Files2Copy
# the group names are quite explicit
if len(burnSampleL2): Files2Copy.extend(SortnGroup(burnSampleL2))
if len(OtherL2): Files2Copy.extend(SortnGroup(OtherL2))
if len(burnSamplePFFilt): Files2Copy.extend(SortnGroup(burnSamplePFFilt))
if len(OtherPFFilt): Files2Copy.extend(SortnGroup(OtherPFFilt))

print len(Files2Copy)
#for f in Files2Copy: print f
