'''
Author: Prashant Kumar
Date: 5th September 2017
This class is for scraping fundoodata.com data for ecommerce data of 5 cities, Mumbai, Delhi, Pune, Chennai and Bangalore
'''
import urllib3
from bs4 import BeautifulSoup
import csv

class ScrapeFundoo:
    def __init__(self):
        self.http = urllib3.PoolManager()

    def getScrapeData(self, city_id, pageNo, rowCount):
        nameList = []
        tableDataList = []
        r = self.http.request('GET', 'https://www.fundoodata.com/advance_search_results.php?&new_industry_id%5b%5d=125&level_id=1&city_id='+city_id+'&criteria=1&search_type=&pageno='+pageNo+'&tot_rows='+rowCount+'&total_results='+rowCount+'&no_of_offices=0')
        soup = BeautifulSoup(r.data, 'lxml')
        divs = soup.select("div.search-result-left")
        names = soup.select("div.heading")
        for name in names:
            nameList.append((name.text).strip())
        for k in divs:
            td = k.select("table")
            for j in range(0, len(td)):
                tableData = ((td[j].text).replace("\n","").replace("\t","")).strip()
                tableDataList.append(tableData)
        return nameList, tableDataList

    def getCityData(self, city_name, city_id, pageNos, rowCount):
        nameList = ['Company Name']
        tableDataList = ['Company Information']
        for i in range(1, pageNos):
            names, tables = self.getScrapeData(str(city_id), pageNo=str(i),rowCount=rowCount)
            nameList.extend(names)
            tableDataList.extend(tables)
        rows = zip(nameList,tableDataList)
        with open(city_name+".csv", "w") as f:
            wr = csv.writer(f, dialect='excel')
            for row in rows:
                wr.writerow(row)

sF = ScrapeFundoo()
sF.getCityData(city_name="Bangalore", city_id="6", pageNos=9, rowCount="159")
sF.getCityData(city_name="Pune", city_id="7", pageNos=2, rowCount="37")
sF.getCityData(city_name="Mumbai", city_id="5", pageNos=11, rowCount="216")
sF.getCityData(city_name="Delhi", city_id="0", pageNos=20, rowCount="388")
sF.getCityData(city_name="Chennai", city_id="9", pageNos=3, rowCount="52")

