'''
Author: Prashant Kumar
Date: 4th September 2017
This class is for scraping buildtraders.com data for cement, blocks, bricks, tmt, coarse aggregates, msand
This scraping project is for non-profit and is completely free
'''
import json
from http import client
from pymongo import MongoClient
class ScrapeDataBuildTraders:

    # constructor; initializes the http client and the mongodb client
    def __init__(self):
        self.conn = client.HTTPConnection("www.buildtraders.com")
        self.mongoClient = MongoClient("mongodb://localhost:27017")

    # generic method which invokes a GET call with parameter specified in the method
    def callGetApi(self, category, startValue, countValue):
        formedUrl = "/v1/categories/"+str(category)+"/skus?include=product%2Cdefault_retail_cost&=&filters=%3B%3Bsort_by%3Apopularity&start="+str(startValue)+"&count="+str(countValue)
        self.conn.request("GET", formedUrl)
        res = self.conn.getresponse()
        data = res.read().decode("utf-8")
        jsonData = json.loads(data)
        return jsonData['sku_page']['items']

    # method to fetch the json data for the cement
    def getCement(self):
        try:
            return self.callGetApi(category='13',startValue='', countValue='100')
        except:
            print("exception in getting response from the server")

    # method to fetch the json data for the tmt
    def getTmt(self):
        try:
            jsonData = []
            jsonData.extend(self.callGetApi(category='14',startValue="0", countValue='24'))
            jsonData.extend(self.callGetApi(category='14',startValue="24", countValue='24'))
            return jsonData
        except:
            print("exception in getting response from the server")

    # method to fetch the json data for the blocks
    def getBlocks(self):
        try:
            return self.callGetApi(category='17',startValue='', countValue='24')
        except:
            print("exception in getting response from the server")

    # method to fetch the json data for the bricks
    def getBricks(self):
        try:
            return self.callGetApi(category='16',startValue='', countValue='24')
        except:
            print("exception in getting response from the server")

    # method to fetch the json data for the coarse aggregates
    def getCoarseAggregates(self):
        try:
            return self.callGetApi(category='22',startValue='', countValue='24')
        except:
            print("exception in getting response from the server")

    # method to fetch the json data for the msand
    def getMsand(self):
        try:
            return self.callGetApi(category='19',startValue='', countValue='24')
        except:
            print("exception in getting response from the server")

    # method to insert an array of documents based on a collection name
    def insertDoc(self, docArray, collectionName):
        try:
            db = self.mongoClient['buildtraders']
            db[collectionName].delete_many({})
            db[collectionName].insert(docArray)
        except:
            print("problem while insertion of data in mongo")

# create an object of the BuildTraders class
Api = ScrapeDataBuildTraders()

Api.insertDoc(Api.getCement(), 'Cements')
Api.insertDoc(Api.getBlocks(), 'Blocks')
Api.insertDoc(Api.getBricks(), 'Bricks')
Api.insertDoc(Api.getTmt(), 'Tmt')
Api.insertDoc(Api.getCoarseAggregates(), 'CoarseAggregate')
Api.insertDoc(Api.getMsand(), 'Msand')