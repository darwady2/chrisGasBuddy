import datetime
import csv
import urllib2
import os
from bs4 import BeautifulSoup


#Gets contents of a page.
def get_http(url):
	response = urllib2.urlopen(url)
	return response.read()


#Finds the raw price objects from Gas-Buddy.
def get_prices_from_web(html):
	soup = BeautifulSoup(html, 'html.parser')
	#return soup.find_all(class_='price-display credit-price')
	return soup.find_all(class_='ui header styles__price___1wJ_R')


#Cycles through the returned prices and returns a list of the prices.
def show_prices(prices):
	complete_prices = []
	for price in prices:
		split1_price = str(price).split(">")		#Splits at the first div tag.
		split2_price = split1_price[1].split("<")	#Splits at the second div tag.
		complete_prices.append(split2_price[0][1:])	#Returns the first element (the price) and takes out the dollar sign.
	return complete_prices


#Creates a unique filename with the proper date formatting.
def create_filename(client):
	current_date = datetime.datetime.now().strftime("%m-%d-%y")
	return client + '_' + current_date + '.csv'


#Return the proper directory, and if it doesn't exist, create it.
def create_directory(dir, windows):
	directory = os.path.join(os.path.expanduser('~'), dir)
	if windows:
		directory = os.path.join('C:\\', dir)
	if not os.path.exists(directory):
		os.makedirs(directory)
	return directory


#Combines the output of the filename and directory.
def create_filepath(filename, directory, windows):
	d = create_directory(dir = directory, windows = windows)
	f = create_filename(filename)
	path = os.path.join(d, f)
	return path

#Winnebago logic.
def winnebago():

	#Constants.
	mft = .184
	propane_mft = .226

	#Fetch price.
	html = get_http('https://www.gasbuddy.com/Station/66970')
	prices_list = get_prices_from_web(html)
	price_final = show_prices(prices_list)
	print price_final
	retail_gas = float(price_final[0])

	#Calculate price.
	retail_minus_mft = retail_gas - mft
	sales_tax = .05 * retail_minus_mft
	retail_taxfree = retail_minus_mft - sales_tax
	propane_price = retail_taxfree - 0.50
	raw_cost_of_propane = propane_price - propane_mft

	#Define filepath.
	filepath = create_filepath(
		filename = 'winnebago_price',
		directory = 'Documents/Github/chrisGasBuddy/danTest',
		windows = False #Write False if not running this program on Windows.
		)

	#Create CSV file.
	with open(filepath, 'wb') as csvfile:
		filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
		filewriter.writerow(['Raw Cost of Propane',raw_cost_of_propane])
		filewriter.writerow(['WI Propane MFT',propane_mft])
		filewriter.writerow(['Propane Price',propane_price])

	#Return finishing message.
	print '\nWinnebago file created, see "' + filepath + '"'
	return propane_price


#R&D Diesel logic.
def rd_diesel():

	#Fetch price.
	html = get_http('https://www.gasbuddy.com/Station/29546')
	prices_list = get_prices_from_web(html)
	price_final = show_prices(prices_list)
	diesel_index = len(price_final)-1
	retail_gas = float(price_final[diesel_index])

	#Calculate price.
	sale_gas = retail_gas - .10

	#Define filepath.
	filepath = create_filepath(
		filename = 'r&d_diesel_price',
		directory = 'Documents/Github/chrisGasBuddy/danTest',
		windows = False #Write False if not running this program on Windows.
		)

	#Create CSV file.
	with open(filepath, 'wb') as csvfile:
		filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
		filewriter.writerow(['Retail Diesel at Falcon Fuel, 300 S Cicero Ave',retail_gas])
		filewriter.writerow(['AFS Weekly Diesel Fuel Price, 4654 W Washington Blvd',sale_gas])

	#Return finishing message.
	print '\nR&D file created, see "' + filepath + '".'
	return sale_gas


#Main program.
def main():

	winnebago()
	rd_diesel()
	print '\nFinished, script run successfully.\n'


if __name__ == '__main__':
    main()
