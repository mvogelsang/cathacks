import subprocess
import os
import sqlite3
import datetime
import time
import googlefinance
import requests
import twitter
import sys

# note, for convenience of writing many separate query functions
# the connection is defined globally
dbConn = sqlite3.connect("./stockinfo.db", detect_types=sqlite3.PARSE_DECLTYPES);
# dbConn.row_factory = sqlite3.Row
dbCursor = dbConn.cursor()
# a66709521106364d780bac5e6ac6f66f4b184206IH3msJM7XveroPUUFLLnn5WIa

# initialize twitter stuff
api = twitter.Api(consumer_key='Bb4x7mFZP2cDRo3eUJrH0n1hB',
                      consumer_secret='48Ku9TpZmP0Q4PFPhshXsO8Q21yQaPzdKQqvpYfq0lAWER7k2F',
                      access_token_key='398399301-yt52zOcroegxNTy6stklO6toYxgIRuarHdFfnmxR',
                      access_token_secret='CypwTsgsQ0eY462uzHQdguCYFTz9jQ1PF1x5NytmlapTC')

with open('negativeWords.txt', 'r') as f:
    negativeWords = f.readlines()


def sendText(msg, number):
    chunks = split2len(msg, 250)
    for chunk in chunks:
        response = requests.post('https://textbelt.com/text', {
          'phone': str(number),
          'message': chunk,
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
        dbCursor.execute( "update stockdata set currentPrice = ? where ticker = ?", (p['LastTradePrice'], p['StockSymbol']) )
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
            dbCursor.execute( "update stockdata set trackprice = ? where ticker = ?", (a[2], a[0]) )
            dbConn.commit()

        print 'sending alerts...'
        print msg
        print ''

        sendText(msg, 8594947422)

    # check twitter for bad things :(
    users = ['mjtv42', 'cnn']
    print 'searching'
    for user in users:
        statuses = api.GetUserTimeline(screen_name=user, count=50)
        for t in statuses:
            statusText = (t.text)
            foundNeg = False
            founStock = False

            for word in negativeWords:
                if (word) in statusText:
                    foundNeg = True

            for stock in tickers:
                if ("$" + stock) in statusText:
                    founStock = True

            if(founStock and foundNeg):
                print 'FOUND NEGATIVITY'
                print statusText
                sendText(statusText, 8594947422)

    dbConn.close()




if __name__ == "__main__":
    main()
