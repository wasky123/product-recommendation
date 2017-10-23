__author__ = 'Administrator'
import simplejson
import csv

def parse(filename):
    f = open(filename)
    entry = {}
    for l in f:
        l = l.strip()
        colonPos = l.find(':')
        if colonPos == -1:
            yield entry
            entry = {}
            continue
        eName = l[:colonPos]
        rest = l[colonPos+2:]
        entry[eName] = rest
    yield entry
with open("Automotive_new.csv","wb") as csvfile: # "wb" will maintain the output without blank rows
    writer = csv.writer(csvfile)
    for e in parse("Automotive.txt"):
        if e.has_key("review/userId")==False:
            continue
        if e.has_key("review/userId")== True:
            if e["review/userId"]=="":
                continue
        # if e.has_key("product/productId")==False:
        #     continue
        # if e.has_key("review/score")==False:
        #     continue
        # if e.has_key("review/time") == False:
        #     continue
        # if e["review/userId"]== "unknown":
        #    continue
        if e.has_key("product/title")==False:
            continue
        if e.has_key("product/title")== True:
            if e["product/title"]=="":
                continue

        # writer.writerow([e["review/userId"],e["product/productId"],e["review/score"],e["review/time"]])
        writer.writerow([e["product/productId"],e["product/title"]])


'''
line = f.readline()
while line:
    print line,
    line = f.readline()
'''