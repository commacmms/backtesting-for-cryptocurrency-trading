# convert all concepts that were originally for binance for coinbase instwad
import cbpro

import csv
import os
import time
from datetime import date, datetime

public_client = cbpro.PublicClient()

def get_coins():
    with open('coins.txt', 'r') as f:
        coins = f.readlines()
        coins = [coin.strip('\n') for coin in coins]
    return coins

#def get_historical_data(coin, since, kline_interval):
def get_historical_data(coin, start, end, granularity):
    """
    Args example:
    coin = 'ETH-EUR'
    start = '01-01-2020'
    end = '07-08-2021'
    granularity = 60, 300, 900, 3600, 21600, 86400
    """
    if os.path.isfile(f'{coin}_{start}_to_{end}.csv'):
        print('Datafile already exists, loading file...')

    else:
        print(f'Fetching historical data for {coin}, this may take a few minutes...')

        start_time = time.perf_counter()
        #data = public_client.get_historical_klines(coin, kline_interval, since)
        f_start = datetime.strptime(start, '%d-%m-%Y')
        f_end = datetime.strptime(end, '%d-%m-%Y')
        data = public_client.get_product_historic_rates(coin, granularity=granularity, start=f_start.isoformat(), end=f_end.isoformat())
        data = [item[0:6] for item in data]

        # field names
        fields = ['time', 'low', 'high', 'open', 'close', 'volume']

        # save the data
        with open(f'{coin}_{start}_to_{end}.csv', 'w', newline='') as f:
            # using csv.writer method from CSV package
            write = csv.writer(f)
            write.writerow(fields)
            write.writerows(data)

        end_time = time.perf_counter()

        # calculate how long it took to produce the file
        time_elapsed = round(end_time - start_time)

        print(f'Historical data for {coin} saved as {coin}_{start}_to_{end}.csv. Time elapsed: {time_elapsed} seconds')
    return f'{coin}_{start}_to_{end}.csv'
