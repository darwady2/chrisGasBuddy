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





def main():

	html = get_http('https://www.gasbuddy.com/Station/66970')
	prices_list = get_prices_from_web(html)
	price_final = show_prices(prices_list)
	print price_final[0]
	print price_final[3]

if __name__ == '__main__':
    main()