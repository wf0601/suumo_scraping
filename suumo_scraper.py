import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
import pandas as pd
from typing import Dict, List

@dataclass
class SuumoScraper:
    url: str
    
    @property
    def _get_page_content(self):
      page = requests.get(self.url)
      soup = BeautifulSoup(page.content,"html.parser")
      return soup
    
    def get_all_details_in_page(self):
      elements = self._get_all_property
      df_all = pd.DataFrame()
      for ele in elements:
        one_building = self._get_all_flats_in_building(ele)
        df_all = pd.concat([df_all,one_building])
      return df_all   

    @property
    def _get_all_property(self):
      return self._get_page_content.find(id="js-bukkenList").find_all("div", class_="cassetteitem")
    
    @staticmethod
    def _get_property_name(ele):
      try:
        property_name = ele.find("div","cassetteitem_content-title").text
      except:
        property_name = ''
      return property_name
    @staticmethod
    def _get_property_block(ele):
      try:
        property_block = ele.find("li","cassetteitem_detail-col1").text
      except:
        property_block = ''
      return property_block
    @staticmethod
    def _get_construction_details(ele):
      try:
        details = ele.find("li",class_="cassetteitem_detail-col3").text.strip().split('\n')   
        construction_details = ','.join(details)
      except:
        construction_details = ''
      return construction_details
    @staticmethod
    def _get_stations_nearby(ele) -> List:
      try:
        stations = ele.find_all("div",class_ = "cassetteitem_detail-text") 
        stations_info = [station.text.strip() for station in stations]
      except:
        stations_info = []
      return stations_info

    def _get_all_flats_in_building(self,ele) -> pd.DataFrame:
      flats = ele.find_all("tr","js-cassette_link") 
      df_one_building = pd.DataFrame()
      for flat in flats:    
        flat_dict = {'property_name':self._get_property_name(ele),
                     'flat_address':self._get_property_block(ele),
                     'flat_detail':self._get_construction_details(ele),
                     'station_nearby':self._get_stations_nearby(ele)}
        floor = flat.find_all('td')[2].text.strip()
        rent = flat.find("span",class_ = 'cassetteitem_price cassetteitem_price--rent').text.split('万円')[0]
        size = flat.find("span",class_ = 'cassetteitem_menseki').text
        flat_dict['size']=size
        flat_dict['rent']=rent
        flat_dict['floor'] = floor
        one_flat = pd.DataFrame({k: [v] for k, v in flat_dict.items()})
        df_one_building = pd.concat([df_one_building,one_flat])
      return df_one_building 
        




# def scrape(url):
#   df = pd.DataFrame()
#   page = requests.get(url)
#   soup = BeautifulSoup(page.content, "html.parser")
#   results = soup.find(id="js-bukkenList")
#   elements = results.find_all("div", class_="cassetteitem")
#   for ele in elements:
#     mansion_name = ele.find("div","cassetteitem_content-title").text
#     mansion_address = ele.find("li","cassetteitem_detail-col1").text
#     mansion_detail = ele.find("li",class_="cassetteitem_detail-col3").text.strip().split('\n')
#     stations = ele.find_all("div",class_ = "cassetteitem_detail-text")
#     station_detail = []
#     for station in stations:
#       station_detail.append(station.text.strip())
#     flats = ele.find_all("tr","js-cassette_link")
#     for flat in flats:
#       flat_dict = {'flat_name':mansion_name,'flat_address':mansion_address,'flat_detail':mansion_detail,'station':station_detail}
#       floor = flat.find_all('td')[2].text.strip()
#       rent = flat.find("span",class_ = 'cassetteitem_price cassetteitem_price--rent').text.split('万円')[0]
#       size = flat.find("span",class_ = 'cassetteitem_menseki').text
#       flat_dict['size']=size
#       flat_dict['rent']=rent
#       flat_dict['floor'] = floor
#       one_row = pd.DataFrame({k: [v] for k, v in flat_dict.items()})
#       df = pd.concat([df,one_row])
#   return df    