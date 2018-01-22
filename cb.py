#!/usr/bin/env python

import requests
import os
import ast
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
        self.send_to = ["+19093316457", "+19095250519", "+13103086949", "+18585317775"]
        #self.send_to = ["+19093316457"]
        self.from_ = "+19513863249"


        # coins to search
        #self.coins = ["ETH", "LTC"]
        self.coins = ["ETH"]

        # eth
        self.eth_low_thresh = 700
        self.eth_low = self.eth_low_thresh
        #self.eth_high = self.get_price_cb("sell", "ETH") 
        self.eth_high = 1400 
        self.eth_last_low = 1

        # ltc
        self.ltc_low_thresh = 225
        self.ltc_low = self.ltc_low_thresh
        #self.ltc_high = self.get_price_cb("sell", "LTC") 
        self.ltc_high = 350 
        self.ltc_last_low = 1

    def get_price_cb(self, price, coin):

        if price == "buy":
            url = "https://api.coinbase.com/v2/prices/" + coin + "-USD/buy"
        elif price == "sell":
            url = "https://api.coinbase.com/v2/prices/" + coin + "-USD/sell"

        response = requests.get(url)

        data = ast.literal_eval(response.text)

        value = data["data"]["amount"]

        return float(value)


    def update(self, buy_price, sell_price, coin):

        if coin == "LTC":

            if self.ltc_last_low != 0:
                if self.cycle_count > (self.ltc_last_low + 40):
                    self.ltc_low = self.ltc_low_thresh

            if buy_price < self.ltc_low:
                diff = buy_price - self.ltc_low
                change = ((diff) / self.ltc_low) * 100
                msg = ("LTC Buy Price: %.2f (%.2f @ %.2f%%)" % (buy_price, diff, change))

                if diff <= -1:
                    self.send_sms(msg)
                    self.ltc_low = buy_price

                self.ltc_last_low = self.cycle_count

            elif sell_price > self.ltc_high:
                diff = sell_price - self.ltc_high
                change = ((diff) / self.ltc_high) * 100
                msg = ("LTC Sell Price: %.2f (+ %.2f @ %.2f%%)" % (sell_price, diff, change))
                
                if diff >= 1:
                    self.send_sms(msg)
                    self.ltc_high = sell_price
                
        elif coin == "ETH":

            if self.eth_last_low != 0:
                if self.cycle_count > (self.eth_last_low + 40):
                    self.eth_low = self.eth_low_thresh

            if buy_price < self.eth_low:
                diff = buy_price - self.eth_low
                change = ((diff) / self.eth_low) * 100
                msg = ("ETH Buy Price: %.2f (%.2f @ %.2f%%)" % (buy_price, diff, change))

                if diff <= -1:
                    self.send_sms(msg)
                    self.eth_low = buy_price

                self.eth_last_low = self.cycle_count

            if sell_price > self.eth_high:
                diff = sell_price - self.eth_high
                change = ((diff) / self.eth_high) * 100
                msg = ("ETH Sell Price: %.2f (+ %.2f @ %.2f%%)" % (sell_price, diff, change))

                if diff >= 1:
                    self.send_sms(msg)
                    self.eth_high = sell_price


    def send_sms(self, msg):

        print(msg)
        for person in self.send_to:

            self.client.messages.create(to=person, from_=self.from_, body=msg)

def main():

    cmc = cmc_data()

    while True:

        for coin in cmc.coins:

            try:
                buy_price = cmc.get_price_cb("buy", coin)
                sell_price = cmc.get_price_cb("sell", coin)
                print("%s: Buy: %.2f Sell: %.2f" % (coin, buy_price, sell_price))
                cmc.update(buy_price, sell_price, coin)

            except:
                pass

        cmc.cycle_count += 1
        time.sleep(30)

        


if __name__ == "__main__":
    main()
