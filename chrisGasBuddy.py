from bs4 import BeautifulSoup
import urllib2

def main():

	response = urllib2.urlopen('https://www.gasbuddy.com/Station/66970')
	html = response.read()

	soup = BeautifulSoup(html, 'html.parser')

	prices_list = soup.find_all(class_='price-display credit-price')
	
	complete_prices = []
	
	for prices in prices_list:
		split1_price = str(prices).split(">")
		split2_price = split1_price[1].split("<")
		complete_prices.append(split2_price[0])
		
	
	print complete_prices[0]
	print complete_prices[3]

if __name__ == '__main__':
    main()