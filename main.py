import subprocess
import os
import sqlite3
import datetime
import time
import googlefinance
import requests


# # note, for convenience of writing many separate query functions
# # the connection is defined globally
# dbConn = sqlite3.connect("./LouData.db", detect_types=sqlite3.PARSE_DECLTYPES);
# dbConn.row_factory = sqlite3.Row
# dbCursor = dbConn.cursor()
# a66709521106364d780bac5e6ac6f66f4b184206IH3msJM7XveroPUUFLLnn5WIa

def getStockList():
    # get get stock array
    with open("./stocks.dat", "rb") as input_file:
        stocks = input_file.readlines()
    return stocks

def getRecentPrices():
    with open("./benchmarks.dat", "rb") as input_file:
        prices = input_file.readlines()
    return prices

def sendText(msg, number):
    response = requests.post('https://textbelt.com/text', {
      'phone': str(number),
      'message': msg,
      'key': '3ad6e579a523e9e9ecb180fdf6eb5cdfdf45984c19kuhuiZaE1kSWAnvDbyUmexL',
    })

    print response.content

def main():
    # stocks = getStockList()
    # recentPrices = getRecentPrices()
    sendText('waddup hoe', 8594947422)






if __name__ == "__main__":
    main()
