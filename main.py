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

def split2len(s, n):
    def _f(s, n):
        while s:
            yield s[:n]
            s = s[n:]
    return list(_f(s, n))

def main():
    # get stock tickers
    dbCursor.execute('select ticker from stockdata;')
    temp = dbCursor.fetchall()
    tickers = list(sum(temp, ()))

    # get most recent prices
    priceInfo = googlefinance.getQuotes(tickers)

    # update recent prices
    for p in priceInfo:
        dbCursor.execute("update stockdata set currentPrice = ? where ticker = ?", (p['LastTradePrice'], p['StockSymbol']) )
    dbConn.commit()

    # get all of the stock information
    dbCursor.execute("select * from stockdata where abs(trackprice - currentprice)*1.0/(trackprice*1.0) > .15")
    alertStocks = dbCursor.fetchall()

    # Verify that results were found
    dbCursor.execute("select count(*) from stockdata where abs(trackprice - currentprice)*1.0/(trackprice*1.0) > .15")
    count = dbCursor.fetchall()
    if(count[0][0] > 0):

        # build the message
        msg = 'STOCK ALERTS:\n'
        for a in alertStocks:
            msg = msg + ' ' + str(a[0]) + ' ' + str(a[2]) + '\n'

        print 'sending alerts...'
        print msg
        print ''

        # split into sendable chunks
        chunks = split2len(msg, 250)
        print chunks

        # send the chunks
        for chunk in chunks:
            sendText(chunk, 8594947422)


    # this is some test stuff
    # sendText('waddup', 8594947422)
    # subprocess.call(["csvsql", "--db", "sqlite:///./stockinfo.db", "--insert", "./stockdata.init"])



if __name__ == "__main__":
    main()
