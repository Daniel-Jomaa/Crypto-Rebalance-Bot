#all libraries can be downloaded using: pip install python-binance, pip install dropbox, pip install pandas, pip install apscheduler
#IMPORTING LIBRARIES
from binance_helper import *

#checking if a file exists
import os.path
#to run every hour
from apscheduler.schedulers.blocking import BlockingScheduler




#printing prices (in the form of a list of dicts ('symbol', 'price'))

#print(prices)

def program_runner():
    data_dict = {
        'Assets': {

        },
        #price, symbol/trading_pair, asset_count, %diff
        'Portfolio': {
                'Value': 0,
        },
        #value, percent increase
        'Time': 0,
    }
    #connecting to Binance
    api_key = "IkluBIx1nSsFnrc5HXhXi10baRQJFVUsnuoTPwZwDwxEvwqdqluo3ZmRsQC0aiAE";
    api_secret = "qbzt0w5TvcgJCPYDJIe2KZ2v4tbdiw8YeYZMJttjK6Ieo3OQDgvGOJ170QvdG5Fc";
    client = Client(api_key, api_secret)
    #csv name
    csv_name = 'Project-Enchilada-Datav2.csv'
    #List of coins to be trading
    coin_list = ['ICX', 'LTC', 'NANO', 'NEO']
    coin_list.sort()
    #retrieves the coin balances
    balances_of_coins = checking_balances(client)
    #initializes data_dict
    initialize_data_dict(data_dict, balances_of_coins)
    #price gathering
    prices = client.get_all_tickers()
    #making the dict to hold all the data
    #data_dict = {'Error': 'None'}
    #purchase the inital coin_stat
    #update prices of each coin in portfolio
    update_Price(data_dict, prices)
    #update quantity of each coin in portfolio
    update_Quantity(data_dict, coin_list, client)
    #purchase if coins are not purchased
    if purchase_coins(data_dict, coin_list, client):
        update_Price(data_dict, coin_list, prices)
        update_Quantity(data_dict, coin_list, client)
    #updates total portfolio value
    total_value(data_dict)
    #creates the percent difference in the reqiuired percent and the actual percentage
    update_Pdiff(data_dict, coin_list)
    #reorganize into equal %
    update_TradeVal(data_dict)
    #shave off the top into btc
    sell_assets_over(data_dict, coin_list, client)
    #prop up deficits, buy from btc
    buy_assets_under(data_dict, coin_list, client)
    #verify BNB is sufficient
    verify_BNB(data_dict, prices, coin_list, client)
    #updates time in UTC
    time = update_Time(data_dict)
    #save to a csv
    if (not os.path.isfile(csv_name)):
        initialize_csv(csv_name, coin_list)
    dict_to_csv(data_dict, csv_name)
    print("Just ran at " + time)
    print(data_dict)


# EXCEL FILE
# time, price, quantity, surplus/deficit from equal percentage, total portfolio value, percent increase


#Final note: We need to run this in a daemon for nonstop
if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(program_runner, 'interval', minutes=1)
    scheduler.start()
