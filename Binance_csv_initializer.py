from binance_helper import initialize_csv

if __name__ == "__main__":
    csv_name = 'Project-Enchilada-Data.csv'
    coin_list = ['ICX', 'NANO', 'TRAC', 'XLM', 'ZRX', 'BNB', 'ADA', 'SUB']
    initialize_csv(csv_name, coin_list)
