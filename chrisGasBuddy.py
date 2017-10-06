import datetime
import csv
import urllib2
from bs4 import BeautifulSoup


#Gets contents of a page.
def get_http(url):
	response = urllib2.urlopen(url)
	return response.read()	


#Finds the raw price objects from Gas-Buddy.
def get_prices_from_web(html):
	soup = BeautifulSoup(html, 'html.parser')
	return soup.find_all(class_='price-display credit-price')
	

#Cycles through the returned prices and returns a list of the prices.
def show_prices(prices):
	complete_prices = []
	for price in prices:
		split1_price = str(price).split(">")
		split2_price = split1_price[1].split("<")
		complete_prices.append(split2_price[0])
	return complete_prices


#Winnebago logic.
def winnebago():
	html = get_http('https://www.gasbuddy.com/Station/66970')
	prices_list = get_prices_from_web(html)
	price_final = show_prices(prices_list)
	retail_gas = float(price_final[0])
	mft = .184
	propane_mft = .226
	retail_minus_mft = retail_gas - mft
	sales_tax = .05 * retail_minus_mft
	retail_taxfree = retail_minus_mft - sales_tax
	propane_price = retail_taxfree - 0.50
	raw_cost_of_propane = propane_price - propane_mft
	current_date = datetime.datetime.now().strftime("%m-%d-%y")
	filename = 'winnebago_price_' + current_date + '.csv'
	with open(filename, 'wb') as csvfile:
		filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
		filewriter.writerow(['Raw Cost of Propane',raw_cost_of_propane])
		filewriter.writerow(['WI Propane MFT',propane_mft])
		filewriter.writerow(['Propane Price',propane_price])
	
	return propane_price
	

#R&D Diesel logic.
def rd_diesel():
	html = get_http('https://www.gasbuddy.com/Station/29546')
	prices_list = get_prices_from_web(html)
	price_final = show_prices(prices_list)
	retail_gas = float(price_final[3])
	sale_gas = retail_gas - .10
	current_date = datetime.datetime.now().strftime("%m-%d-%y")
	filename = 'r&d_diesel_price_' + current_date + '.csv'
	with open(filename, 'wb') as csvfile:
		filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
		filewriter.writerow(['Retail Diesel at Falcon Fuel, 300 S Cicero Ave',retail_gas])
		filewriter.writerow(['AFS Weekly Diesel Fuel Price, 4654 W Washington Blvd',sale_gas])
		
	return sale_gas
		
def main():
	
	winnebago()
	rd_diesel()


if __name__ == '__main__':
    main()