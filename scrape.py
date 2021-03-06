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
