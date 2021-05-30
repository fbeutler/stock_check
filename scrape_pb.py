import sys
import urllib
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

from bs4 import BeautifulSoup


def read_t212(filename):
    '''

    '''
    with open(filename,mode='r') as file:
        content = BeautifulSoup(file.read(), "html.parser")
    return content


def get_pb(tag):
	'''
	'''
	print("tag = ", tag)
	link = 'https://ycharts.com/companies/%s/price_to_book_value' % tag.split('.')[0].strip()
	soup = get_soup(link)
	
	if soup is None:
		return None
	else:
		value = soup.findAll("span", {"id": "pgNameVal"})
		if value:
			return float(value[0].text.split()[0])
		else:
			return None


def get_sector(tag):
	'''
	'''
	print("tag = ", tag)
	link = 'https://ycharts.com/companies/%s' % tag.split('.')[0].strip()
	soup = get_soup(link)
	
	if soup is None:
		return None, None
	else:
		sector = ''
		industry = ''
		ul_el = soup.findAll("ul", {"class": "compProfile"})
		if ul_el:
			for li_el in ul_el[0].findAll('li'):
				if li_el.findAll('strong')[0].text == 'Sector':
					a_el = li_el.findAll('a')
					if a_el:
						sector = a_el[0].text
				if li_el.findAll('strong')[0].text == 'Industry':
					a_el = li_el.findAll('a')
					if a_el:
						industry = a_el[0].text
			return sector, industry
		else:
			return None, None


def get_pe(tag):
	'''
	'''
	print("tag = ", tag)
	link = 'https://ycharts.com/companies/%s/pe_ratio' % tag.split('.')[0].strip()
	soup = get_soup(link)
	
	if soup is None:
		return None
	else:
		value = soup.findAll("span", {"id": "pgNameVal"})
		if value:
			# Maybe save the date?
			return float(value[0].text.split()[0])
		else:
			return None


def get_soup(link):
	'''
	'''
	try:
	    html = urlopen(link)
	except HTTPError as err: # The page is not found on the server
	    print("ERROR: Internal server error!", err)
	    return None
	except URLError as err:
	    print("ERROR: The server could not be found!", err)
	    return None
	else:
	    return BeautifulSoup(html.read(), "html.parser")
