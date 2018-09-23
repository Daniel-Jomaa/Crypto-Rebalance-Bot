data_dict = {
	'Assets': {

	},
	#price, symbol/trading_pair, asset_count, %diff
	'Portfolio': {
			'Value': 0,
	},
	#value, percent increase
	'Time': 0,

	'Error': 0
}
#data_dict['Assets']['NANO'] = {}
#data_dict['Assets']['NANO']['Price'] = 7
#print(data_dict);


from binance.client import Client
api_key = "IkluBIx1nSsFnrc5HXhXi10baRQJFVUsnuoTPwZwDwxEvwqdqluo3ZmRsQC0aiAE";
api_secret = "qbzt0w5TvcgJCPYDJIe2KZ2v4tbdiw8YeYZMJttjK6Ieo3OQDgvGOJ170QvdG5Fc";
client = Client(api_key, api_secret)
info = client.get_symbol_info("ETHBTC")
client.get_symbol_info("ETHBTC")['filters'][1]['minQty']
print(the_thing)

# info = client.get_account()
# print(type(info))
# my_dict = dict()
# my_dict["hi"] = 6;
# print ("hi" in my_dict)
# print("bye" in my_dict)
#
# def func():
# 	try:
# 		print(coin[fjkdskjf])
# 	except:
# 		try:
# 			print(coin[fjkdskjf])
# 		except:
# 			print("Inner is good")
# 	print("This still work")
# func()
# print("Outer is good")
#
# print(str(3.))
