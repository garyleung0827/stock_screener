import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
import math
import numpy as np
import datetime as DT
from datetime import date


date_entry = input('Enter a date in YYYY-MM-DD format: ')
MarketCapLower= float(input('Enter the Lower Market Cap in Billion: ')) * 1000000000
year, month, day = map(int, date_entry.split('-'))
if not MarketCapLower:
	MarketCapLower = 0
end_date = DT.date(year, month, day)
#for time interval is more than 180 days
start_date = end_date - DT.timedelta(days=210)
#today2= end_date + DT.timedelta(days=265)
today = date.today()

while end_date < today:
        print(end_date)

        #create a list of stock for the stock within the Market Cap of my interest
        df = pd.read_csv("Stock List/" + str(end_date) + ".csv")
        df_filtered = df[df['Market Cap'] >= MarketCapLower]
        quote = df_filtered[~df_filtered.Symbol.str.contains("\^")].Symbol.to_list()
        quote = [item.replace("/", "-") for item in quote]
        #quote = ["ABR"]
        #print(quote)

        exportList = pd.DataFrame(columns=['Stock'])
        exportList2 = pd.DataFrame(columns=['Stock'])
        exportList3 = pd.DataFrame(columns=['Stock'])
        exportList4 = pd.DataFrame(columns=['Stock'])

        for i in quote:
                print("stock is : " + i)
                df = yf.download(i, start= start_date, end= end_date, interval = "1wk", auto_adjust = True)
                df = df.dropna().copy()


                if len(df) >= 31:
                        df['SMA_10'] = round(df['Close'].rolling(window=10).mean(), 2)
                        df['SMA_30'] = round(df['Close'].rolling(window=30).mean(), 2)
                        df.Close = df.Close.round(2)
                        sma_10 = df.SMA_10[-1]
                        sma_30 = df.SMA_30[-1]
                        close_now = df.Close[-1]

                        #current Close is greater than SMA_10
                        condition_1 = close_now > sma_10
                        print(condition_1)

                        #current Close is greater than SMA_30
                        condition_2 = close_now > sma_30
                        print(condition_2)

                        #current High is a half year High
                        condition_3 = df.High[-1] >= df.High.tail(26).max()
                        print(condition_3)
               
                        if (condition_1):
                                exportList = exportList.append({'Stock': i}, ignore_index=True)
                        if (condition_2):
                                exportList2 = exportList2.append({'Stock': i}, ignore_index=True)
                        if (condition_3):
                                exportList3 = exportList3.append({'Stock': i}, ignore_index=True)
                        if (condition_1 and condition_2 and condition_3):
                                exportList4 = exportList4.append({'Stock': i}, ignore_index=True)
                              
        exportList.to_csv ('result/at least about 10 ma/at least about 10 ma_' + str(end_date) + '.csv', index = False, header=True)
        exportList2.to_csv ('result/at least about 30 ma/at least about 30 ma_' + str(end_date) + '.csv', index = False, header=True)
        exportList3.to_csv ('result/Half year new height/Half year new height_' + str(end_date) + '.csv', index = False, header=True)
        exportList4.to_csv ('result/Basic condition/update_' + str(end_date) + '.csv', index = False, header=True)

        #add a break if a single day is wannted
        #break
        end_date += DT.timedelta(days=7)
