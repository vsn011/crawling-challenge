from sqlite3 import Timestamp
import scrapy
import json
import requests
import datetime
from immowelt_spinne.items import ImmoweltSpinneItem

from immowelt_spinne.spiders.dict2class import Dict2Class



#move variables to config file 

class ImmoSpider(scrapy.Spider):
    name = 'immo'
    allowed_domains = ['api.immowelt.com']
    start_urls = ['https://api.immowelt.com/']

    URL="https://api.immowelt.com/estatesearch/EstateSearch/v1/Search"

    access_token = ""
    access_token_timeout = ""
    access_token_expires_in=""
    count=0

    headers =  {
                'accept': '*/*', 
                'content-type': 'application/x-www-form-urlencoded; charset=utf-8', 
                'authorization': 'Basic aW1tb3dlbHRfbW9iaWxlX2FwcF9pb3NfMjo5UXVHa20xM1k0WEZPZHFzZW05eGh4RVVKejR2UWdEWA==', 
                }

    headersnew = {
                "accept": "application/json", 
                "content-type": "application/json", 
                "authorization": ""}


    paramsnew = {
        "construction":{},
        "general":{
        "category":[],
        "distributionType":"ZUR_MIETE",
        "equipment":[],
        "estateType":["WOHNUNG", "LAND_FORSTWIRTSCHAFT", "WOHNGEMEINSCHAFT", "GARAGE_STELLPLATZ", "GASTRONOMIE_HOTEL", "HALLEN_INDUSTRIEFLAECHE", "HAUS", "BUERO_PRAXISFLAECHE", "GRUNDSTUECK", "SONSTIGES", "LADENFLAECHE", "WOHNEN_AUF_ZEIT", "GEWERBE_GRUNDSTUECK", "RENDITEOBJEKT"]
            },
        "location":{
            "geo":{
                "locationId":[516424, 518004, 518044, 517940]
             }
         },
        "offset":"0",
        "pagesize":"500",
        "pricing":{},
        "sort":"SortByCreateDate"
    }


    body_req = {"grant_type": "client_credentials"}


    def start_requests(self):
        # if (
        #     self.access_token
        #     and self.access_token_timeout is not None
        #     and pytz.utc.localize(datetime.datetime.utcnow()) < self.access_token_timeout
        #     ):
        #     return self._access_token
        # else:
        return  [scrapy.FormRequest("https://api.immowelt.com/auth/oauth/token",
                                headers=self.headers,
                                method="POST",
                                formdata={"grant_type": "client_credentials"},callback=self.after_login)]


    def after_login(self, response):
        #check if response is null - will be null if token exist
        self.access_token = json.loads(response.body).get("access_token")
        self.access_token_expires_in = json.loads(response.body).get("expires_in")
        # self.access_token_timeout = pytz.utc.localize(
        #      datetime.datetime.utcnow()
        # ) + datetime.timedelta(minutes=10)

        
        self.headersnew["pagesize"] = "1000"
        self.headersnew["offset"] = "0"
        headclone = self.headersnew.copy()
        headclone["pagesize"] = "1000"

        self.headersnew["authorization"] = "Bearer {0}".format(self.access_token)

        while (int(headclone["offset"]) <= self.count):
            return scrapy.Request(self.URL,
                                    headers=self.headersnew,
                                    method="POST",
                                    body=json.dumps(self.paramsnew), dont_filter=True)



    def parse(self, response):
       
        data = json.loads(response.body)
       
        item = data.get('items')
        res = ImmoweltSpinneItem()
        for i in item:
            res["onlineId"] = i.get('onlineId')
            res["globalObjectKey"] = i.get('globalObjectKey')
            res["areas"] = i.get('areas')
            res["address"] = i.get('address')
            res["name"] = i.get('name')
            res["creationDate"] = i.get('creationDate')
            res["broker"] = i.get('broker')
            res["rooms"] = i.get('rooms')
            res["price"] = i.get('price')
            res["estateType"] = i.get('estateType')
            res["distributionType"] = i.get('distributionType')
            res["images"] = i.get('images')
            res["equipment"] = i.get('equipment')
            yield res

       
        
        
    


    # def access_token(self):
    #     """
    #     Returns the current access token if it's not timed out. Otherwise, generates a new one.
    #     """
    #     if (
    #         self._access_token
    #         and self._access_token_timeout is not None
    #         and pytz.utc.localize(datetime.datetime.utcnow())
    #         < self._access_token_timeout
    #     ):
    #         return self._access_token
