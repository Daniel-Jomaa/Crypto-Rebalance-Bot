#Helper file to binance_main.py
import pandas as pd
#for current time
import time
#for accessing API (signing in)
from binance.client import Client

def checking_balances(client):
    balances = client.get_account()['balances']
    balances_of_coins = dict()
    #finds all the nonzero balances in the account
    for item in balances:
        if (item['free'] > 0.0001):
            balances_of_coins[item['asset']] = float(item['free'])
    return balances_of_coins

def initialize_data_dict(dict_name, balances_of_coins):
    for key,value in balances_of_coins:
        dict_name['Assets'][key] = {}

#makes the inital coin purchases
def purchase_coins(dict_name, coin_list, client):
    is_redistributed = False
    validate = 0
    for coin in dict_name['Assets']:
        validate = validate + ((dict_name['Assets'][coin]['Price']) * (dict_name['Assets'][coin]['Quantity']))
    lower_threshold = 0.000009
    if validate < lower_threshold:
        is_redistributed = True
        BTC_available = float(client.get_asset_balance('BTC')['free'])
        qty_to_buy = dict()
        for key, value in dict_name['Assets'].items():
            qty_to_buy[key] = BTC_available / len(coin_list) / dict_name['Assets'][key]['Price']
            order = client.order_limit_buy(symbol = key + "BTC", quantity = float_trunc_2(qty_to_buy[key]), price = str(dict_name['Assets'][key]['Price']), recvWindow=5000)
            print("Buying " + key + " at " + str(dict_name['Assets'][key]['Price']) + ". The API says: " + str(order) + "API type is: " + str(type(order)) + "Bought this much: " + str(float_trunc_2(qty_to_buy[key])))
    return is_redistributed

#finds the coins index in the list from get_all_tickers()
def find_coin_index(prices, trading_pair):
    counter = 0
    for coin in prices:
        if coin['symbol'] == trading_pair:
            return counter
        counter += 1
    return None

#loop through and find all of the prices for the coins that we have
#it does this by using the find_coin_index function and returning the index in
#which the trading pair is indexed at.
def update_Price(dict_name, prices):
    for key,value in dict_name['Assets']:
        coin_pair = key + "BTC"
        coin_index = find_coin_index(prices, coin_pair)
        #add to dict if everything is ok
        else:
            coin_price = prices[coin_index]['price']
            dict_name['Assets'][coin]['Price'] = float(coin_price)

#gather asset quantities
def update_Quantity(dict_name, client):
    for key,value in dict_name['Assets']:
        coin_quantity = client.get_asset_balance(key)['free']
        dict_name['Assets'][key]['Quantity'] = float(coin_quantity)

#populate 'asset': {portfolio: {'value': value}}
#calc total values for whole portfolio and adds them to the json
def total_value(dict_name):
    total_price = 0
    for coin in dict_name['Assets']:
        total_price += dict_name['Assets'][coin]['Price']
    dict_name['Portfolio']['Value'] = total_price

#populate 'asset':{'coin':{'Pdiff': diff }}
#percent difference and add it to the json
def update_Pdiff(dict_name):
    for coin in dict_name['Assets']:
        dict_name['Assets'][coin]['Pdiff'] = (dict_name['Assets'][coin]['Price'] * dict_name['Assets'][coin]['Quantity']) - (dict_name['Portfolio']['Value'] / len(dict_name['Assets']))

#populate the 'asset':{'coin':{'TradeVal:val'}}
#the TradeVal is the number of assets that need to be sold to equilize the
#portfolio
def update_TradeVal(dict_name):
    for coin in dict_name['Assets']:
        dict_name['Assets'][coin]['TradeVal'] = (dict_name['Assets'][coin]['Pdiff'] * dict_name['Portfolio']['Value']) / dict_name['Assets'][coin]['Price']

#if any of the assets are over the equal number
def sell_assets_over(dict_name, client):

    #minimum account qty
    for key,value in dict_name['Assets']:
        if dict_name['Assets'][key]['TradeVal'] > 0:
            MIN_BTC = 0.001
            if coin_quantity * dict_name['Assets'][key]['Price'] > MIN_BTC:
                min_quantity = client.get_symbol_info(key + "BTC")['filters'][1]['minQty']
                coin_quantity = float_trunc(dict_name['Assets']['TradeVal'], min_quantity)
                if coin_quantity < 


                # try:
                # order = client.order_limit_sell(symbol=coin + "BTC",
                #                              quantity=coin_quantity, price = str(dict_name['Assets'][key]['Price']), recvWindow = 5000)
                # except:
                #     try:
                #         coin_quantity = float_trunc(dict_name['Assets']['TradeVal'], 1)
                #         order = client.order_limit_sell(symbol=coin + "BTC",
                #                                      quantity=coin_quantity, price = str(dict_name['Assets'][key]['Price']), recvWindow = 5000)
                #     except:
                #         coin_quantity = float_trunc(dict_name['Assets']['TradeVal'], 0)
                #         order = client.order_limit_sell(symbol=coin + "BTC",
                #                                      quantity=coin_quantity, price = str(dict_name['Assets'][key]['Price']), recvWindow = 5000)
                 print("Selling " + key + ". The API says: " + str(order) + "API type is: " + str(type(order)) + "Sold this much: " + str(float_trunc(dict_name['Assets']['TradeVal']), 2))

#uses the BTC that was purchased to sell into the assets that are underperforming
def buy_assets_under(dict_name, client):
    for key,value in dict_name['Assets']:
        if dict_name['Assets'][key]['TradeVal'] < 0:
            MIN_BTC = 0.001
            coin_quantity = float_trunc(-1 * dict_name['Assets'][key]['TradeVal'], 2)
            if coin_quantity * dict_name['Assets'][key]['Price'] > MIN_BTC:
                try:
                    order = client.order_limit_buy(symbol=key + "BTC",
                                                quantity=coin_quantity, price=str(dict_name['Assets'][key]['Price']), recvWindow=5000)
                except:
                    try:
                        coin_quantity = float_trunc(-1 * dict_name['Assets'][key]['TradeVal'], 1)
                        order = client.order_limit_buy(symbol=key + "BTC",
                                                    quantity=coin_quantity, price=str(dict_name['Assets'][key]['Price']), recvWindow=5000)
                    except:
                        coin_quantity = float_trunc(-1 * dict_name['Assets'][key]['TradeVal'], 0)
                        order = client.order_limit_buy(symbol=key + "BTC",
                                                    quantity=coin_quantity, price=str(dict_name['Assets'][key]['Price']), recvWindow=5000)

                print("Buying " + key + " at " + str(dict_name['Assets'][coin]['Price']) + ". The API says: " + str(order) + "API type is: " + str(type(order)) + "Bought this much: " + str(float_trunc_2(dict_name['Assets'][key]['TradeVal'])))

#FIXME
# def gather_BNB_taxes(dict_name, coin_list, BNB_needed, BNB_price, client):
#
#     BTC_from_each = (BNB_needed * BNB_price) / len(coin_list)
#     for coin in coin_list:
#         qty_from_each = BTC_from_each / dict_name['Assets'][coin]['Price']
#         order = client.order_limit_sell(symbol = coin + "BTC", quantity = float_trunc_2(qty_from_each), price=str(dict_name['Assets'][coin]['Price']), recvWindow=5000 )
#         print("Selling " + coin + ". The API says: " + str(order) + "API type is: " + str(type(order)) + "Sold this much: " + str(float_trunc_2(qty_from_each)))
#
#     update_Quantity(dict_name, coin_list)
#     order = client.order_limit_buy(symbol = "BNBBTC", quantity = float_trunc_2(BNB_needed), price=str(dict_name['Assets'][coin]['Price']), recvWindow=5000)
#     print("Buying " + coin + ". The API says: " + str(order) + "API type is: " + str(type(order)) + "Bought this much: " + str(float_trunc_2(BNB_needed)))
#
# #checks to see if the BNB count is adequate, if it is not, then it will buy more
# #using BTC equally from our existing supply of Assets
# #FIXME
# def verify_BNB(dict_name, prices, coin_list, client):
#
#     refill_BNB_percent = 0.01 # 1%
#     min_BNB_percent = .003 # 0.3%
#
#     BNB_quantity = float(client.get_asset_balance("BNB")['free'])
#     BNB_index = find_coin_index(prices, "BNBBTC")
#     BNB_price = float(prices[BNB_index]['price'])
#
#     if dict_name['Portfolio']['Value'] * min_BNB_percent > BNB_quantity * BNB_price:
#         BNB_quantity_needed = (refill_BNB_percent * dict_name['Portfolio']['Value']/BNB_price) - BNB_quantity
#         gather_BNB_taxes(dict_name, coin_list, BNB_quantity_needed, BNB_price, client)

#returns the string time in (YYMMDDhhmmss) in UTC time
def update_Time(dict_name):
    curr_time = time.gmtime()
    #add year
    year = str(curr_time[0])
    #add month
    month = str(curr_time[1])
    month = month.zfill(2)
    #add day
    day = str(curr_time[2])
    day = day.zfill(2)
    #add hour
    hour = str(curr_time[3])
    hour = hour.zfill(2)
    #add minute
    minute = str(curr_time[4])
    minute = minute.zfill(2)
    #add second
    second = str(curr_time[5])
    second = second.zfill(2)
    dict_name['Time'] = year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second
    return (dict_name['Time'])



#parses the dict into the csv according to andrew's *shitty* panda knowledge
def dict_to_csv(dict_name, csv_name):
    the_cols = ['Time', 'Error', 'Value']
    the_data = [dict_name['Time'], dict_name['Error'],
                dict_name['Portfolio']['Value']]
    for coin in sorted(dict_name['Assets']):
        for coin_stat in sorted(dict_name['Assets'][coin]):
            the_cols.append(coin + "-" + coin_stat)
            the_data.append(dict_name['Assets'][coin][coin_stat])
    series = pd.Series(the_data, index=the_cols)

    df = pd.DataFrame(columns = the_cols)
    df = df.append(series, ignore_index=True)
    with open(csv_name, 'a') as f:
        df.to_csv(f, header=False)

#one time run to initialize the CSV file
def initialize_csv(csv_name, coin_list):
    the_cols = ['Time', 'Value']
    coin_qualities = ['Pdiff', 'Price', 'Quantity', 'TradeVal']
    for coin in coin_list:
        for coin_stat in coin_qualities:
            the_cols.append(coin + "-" + coin_stat)
            series = pd.Series(index=the_cols)
    df = pd.DataFrame(columns = the_cols)
    df = df.append(series, ignore_index=True)
    with open(csv_name, 'a') as file:
        df.to_csv(file, header=True)

#truncates floats to two decimals
def float_trunc(float_num, min_quantity):
    number_decimals = 0;
    while (min_quantity < 1):
        number_decimals += 1
        min_quantity * 10;
    string = str(float_num)
    decimal_index = string.find('.')
    if decimal_index == -1:
        return int(float_num)
    return float(string[0:decimal_index + number_of_decimals + 1])
