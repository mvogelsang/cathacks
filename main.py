import subprocess
import os
import sqlite3
import datetime
import time
import googlefinance
import requests


# note, for convenience of writing many separate query functions
# the connection is defined globally
dbConn = sqlite3.connect("./stockinfo.db", detect_types=sqlite3.PARSE_DECLTYPES);
# dbConn.row_factory = sqlite3.Row
dbCursor = dbConn.cursor()
# a66709521106364d780bac5e6ac6f66f4b184206IH3msJM7XveroPUUFLLnn5WIa

def sendText(msg, number):
    response = requests.post('https://textbelt.com/text', {
      'phone': str(number),
      'message': msg,
      'key': '3ad6e579a523e9e9ecb180fdf6eb5cdfdf45984c19kuhuiZaE1kSWAnvDbyUmexL',
    })

    print response.content

def main():
    # get stock tickers
    dbCursor.execute('select ticker from stockdata;')
    temp = dbCursor.fetchall()
    tickers = list(sum(temp, ()))

    # get most recent prices
    priceInfo = googlefinance.getQuotes(tickers)

    # update recent prices
    for p in priceInfo:
        print p['LastTradePrice'] + ' ' + p['StockSymbol']
        dbCursor.execute("update stockdata set currentPrice = ? where ticker = ?", (p['LastTradePrice'], p['StockSymbol']) )
    dbConn.commit()

    # get all of the stock information
    dbCursor.execute("select * from stockdata")
    stored = dbCursor.fetchall()

    # this is some test stuff
    # sendText('waddup', 8594947422)
    # subprocess.call(["csvsql", "--db", "sqlite:///./stockinfo.db", "--insert", "./stockdata.init"])



if __name__ == "__main__":
    main()
