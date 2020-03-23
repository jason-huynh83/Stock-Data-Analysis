# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 15:07:27 2020

@author: User
"""
import pandas as pd
import bs4
import requests
from bs4 import BeautifulSoup
import mysql.connector

mydb = mysql.connector.connect (
        host = "localhost",
        user = "root",
        passwd = "password123",
        database = "stock"
        )

print (mydb)

my_stocks = ['XOM', 'BYND', 'UBER', 'AC.TO', 'AMD']

#scraping stock price
def stock_prices():
    print('PRICES')
    for url in range(0, len(my_stocks)):
        r=requests.get('https://finance.yahoo.com/quote/' + my_stocks[url])
        soup=bs4.BeautifulSoup(r.text, "lxml")
        price = soup.find('div',{'class':'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
        print("The current price of: " +my_stocks[url]+ ' is ' +str(price))
    return 

#scraping PE ratio
def pe_ratio():
    print('\n')
    print('PE RATIO')
    for url in range(0, len(my_stocks)):
        r=requests.get('https://finance.yahoo.com/quote/' + my_stocks[url])
        soup=bs4.BeautifulSoup(r.text, "lxml")
        pe_ratio = soup.find('td', {'data-test':'PE_RATIO-value'}).find('span').text
        print("The PE ratio of " +my_stocks[url]+ ' is ' +str(pe_ratio))
    return
 
#latest news article
def news():
    print("\nLatest news articles: ")
    for url in range(0, len(my_stocks)):
        print("News for " +my_stocks[url]+ ":")
        r=requests.get('https://finance.yahoo.com/quote/' + my_stocks[url])
        soup=bs4.BeautifulSoup(r.text, "lxml")
        news_table = soup.find('ul', {'class':'My(0) Ov(h) P(0) Wow(bw)'})
        list = ''
        i = 0
        for url1 in news_table.find_all('a'):
            list += url1.get('href')
            print('https://ca.finance.yahoo.com' + str(list))
            i += 1
            if i == 1:
                break
            
#Scarping relevant infomation from site (quarterly earnings) and importing into database MySQL
def company_earnings():
    for url in range(0, len(my_stocks)):
        r=requests.get('https://finance.yahoo.com/calendar/earnings?symbol=' +my_stocks[url])
        soup=bs4.BeautifulSoup(r.text, "lxml")
        table = soup.find('table', {'class':'W(100%)'})
        for bigtable in table.find_all('tr'):
                for symbol in bigtable.find_all('td', {'aria-label':'Symbol'}):
                    a = (symbol.text)
                for company in bigtable.find_all('td',{'aria-label':'Company'}):
                    b = (company.text)         
                for date in bigtable.find_all('td',{'aria-label':'Earnings Date'}):
                    c = (date.text)
                for estimate in bigtable.find_all('td', {'aria-label':'EPS Estimate'}):
                    d = (estimate.text)
                for reported_eps in bigtable.find_all('td', {'aria-label':'Reported EPS'}):
                    e = (reported_eps.text)
                for percent in bigtable.find_all('td',{'aria-label':'Surprise(%)'}):
                    f = (percent.text)
                    #print(a, b, c, d, e, f)
                    stock_table = mydb.cursor()
                    stock_table_values = """insert into stock_table(symbol, company, earnings_date, eps_estimate, reported_eps, surprise_percent) 
                                            values (%s, %s, %s, %s, %s, %s)"""
                    value = (a, b, c, d, e, f)
                    stock_table.execute(stock_table_values, value)
                    mydb.commit()
                    
    """#fetching all the data in the table               
    stock_table_values = "select * from stock_table""
    stock_table.execute(stock_table_values)
    for row in stock_table.fetchall():
        print(row)"""
        
    return table


stock_prices()
pe_ratio()
news()
company_earnings()
