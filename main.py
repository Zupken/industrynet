import lxml.html
import database
import requests
from selenium import webdriver


class Scraping:

    def __init__(self):
        self.default_url = 'https://industrynet.com/suppliers/?category=BA0640-BA0890-BE0004-BE0360-BO0240-BO1110-BR0457-BU0320-BU0350-BU0696-CA0280-CA0503-CA1690-CA1795-CA2100-CA2220-CA2240-CH0100-CO1617-CO1748-CO1755-CO2123-CO2939-CO3678-CY0127-DE0175-DI0610-DI0613-DO0243-DR0643-DR0650-FA0474-FA0475-FE0237-FI0503-FI1087-FL0092-FL0094-FO1390-FO1412-FO1437-GI0070-ST0540-ST0560-ST0562-ST0610-ST0614-ST0615-ST0620-ST0625-ST0635-ST0653-ST0665-ST0700-ST0730-ST0734-ST0770-ST0780-ST0840-ST0855-ST0930-ST0960&page='
        self.number = 1
        self.data = []

    def get_data(self):
        while True:
            url = self.default_url+str(self.number)
            self.source = requests.get(url)
            self.tree = lxml.html.fromstring(self.source.content)
            if self.number == 1:
                self.etree = self.tree.xpath('//td[@class="threecolshelltd2"]/table//td[@class="supplierresultstd2"]')
            elif self.number < 7:
                self.etree = self.tree.xpath('//td[@class="supplierresultspreftd1"]')
            else:
                self.etree = self.tree.xpath('//td[@class="supplierresultsfreetd1"]')
            for element in self.etree:
                self.name = element.xpath('./div[1]/a[@href]/text()')
                if self.name:
                    self.name = self.name[0]
                else:
                    self.name = 'N/A'
                self.city = element.xpath('./div[2]/text()')
                if self.city:
                    self.city = self.city[0]
                else:
                    self.city = 'N/A'
                self.info = element.xpath('./div[@class="smallfont supplierresultspremiumdesc"]/text()')
                if self.info:
                    self.info = self.info[0]
                else:
                    self.info = 'N/A'
                self.data.append([self.name, self.city, self.info])
            self.number += 1
            if self.number > 24:
                break
        x = database.Database(('name', 'city', 'info'))
        x.database(self.data)


Scraping = Scraping()
Scraping.get_data()
