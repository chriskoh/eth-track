#!/usr/bin/env python

import requests
import os
import time
from twilio.rest import Client
from operator import itemgetter
from bs4 import BeautifulSoup

class cmc_data:
    
    def __init__(self):

        # refresh counter
        self.cycle_count = 0

        # twilio
        self.client = Client("ACeb91b9ce6892d763cc73a4ffbc0d0cee", "ee4ef1a2791e57a92ab154bfb202cad7")
        self.send_to = ["+19093316457", "+19095250519"]
        #self.send_to = ["+19093316457"]
        self.from_ = "+19513863249"

        # eth
        self.eth = "id-ethereum"
        self.eth_low_thresh = 700
        self.eth_low = self.eth_low_thresh
        self.eth_high = 1 
        self.eth_last_low = 1

        # ltc
        self.ltc = "id-litecoin"
        self.ltc_low_thresh = 300
        self.ltc_low = self.ltc_low_thresh
        self.ltc_high = 1
        self.ltc_last_low = 1

        # cmc
        self.coins = ["id-ethereum", "id-litecoin"]
        self.cmc_url = "https://coinmarketcap.com"

    def get_price_cb(self):

        response =  requests.get("https://api.coinbase.com/v2/prices/ETH-USD/buy")

        data = response.text

        return data

    def get_price_cmc(self, coin_type):

        response = requests.get(self.cmc_url)
        data = response.text
        to_parse = BeautifulSoup(data, "lxml")

        soup = to_parse
        coin = soup.find('tr', id=coin_type)
        coin_price = coin.find('a', {"class":"price"})
        
        return float(coin_price['data-usd'])

    def update(self, price, coin):

        if coin == "id-litecoin":

            if self.ltc_last_low != 0:
                if self.cycle_count > (self.ltc_last_low + 40):
                    self.ltc_low = self.ltc_low_thresh

            if price < self.ltc_low:
                diff = price - self.ltc_low
                change = ((diff) / self.ltc_low) * 100
                msg = ("New low price (LTC): %.2f (%.2f @ %.2f%%)" % (price, diff, change))
                self.send_sms(msg)
                self.ltc_low = price
                self.ltc_last_low = self.cycle_count

            elif price > self.ltc_high:
                diff = price - self.ltc_high
                change = ((diff) / self.ltc_high) * 100
                msg = ("New high price (LTC): %.2f (+ %.2f @ %.2f%%)" % (price, diff, change))
                self.send_sms(msg)
                self.ltc_high = price
                
        elif coin == "id-ethereum":

            if self.eth_last_low != 0:
                if self.cycle_count > (self.eth_last_low + 40):
                    self.eth_low = self.eth_low_thresh

            if price < self.eth_low:
                diff = price - self.eth_low
                change = ((diff) / self.eth_low) * 100
                msg = ("New low price (ETH): %.2f (%.2f @ %.2f%%)" % (price, diff, change))
                self.send_sms(msg)
                self.eth_low = price
                self.eth_last_low = self.cycle_count

            elif price > self.eth_high:
                diff = price - self.eth_high
                change = ((diff) / self.eth_high) * 100
                msg = ("New high price (ETH): %.2f (+ %.2f @ %.2f%%)" % (price, diff, change))
                self.send_sms(msg)
                self.eth_high = price

    def send_sms(self, msg):

        print(msg)

        '''
        for person in self.send_to:

            self.client.messages.create(to=person, from_=self.from_, body=msg)
        '''

def main():

    cmc = cmc_data()

    print(cmc.get_price_cb())
    '''
    while True:

        for coin in cmc.coins:

            price = cmc.get_price_cmc(coin)
            print("%s: %.2f" % (coin,price))
            cmc.update(price, coin)

        cmc.cycle_count += 1
        time.sleep(30)
    '''

        


if __name__ == "__main__":
    main()
