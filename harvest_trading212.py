from scrape import read_t212


def get_tags():
	soup = read_t212('t212_source.txt')
	all_market_names = [div.text for div in soup.findAll("div", {"data-label" : "Market name"})]

	all_tags = []
	for ii, div in enumerate(soup.findAll("div", {"data-label" : "Instrument"})):
		#print(div.text, all_market_names[ii])
		if all_market_names[ii] == 'Deutsche Börse Xetra':
			all_tags.append('%s.DE' % div.text)
		elif all_market_names[ii] == 'London Stock Exchange' or all_market_names[ii] == 'LSE AIM':
			all_tags.append('%s.L' % div.text)
		elif all_market_names[ii] == 'Euronext Netherlands':
			all_tags.append('%s.AS' % div.text)
		elif all_market_names[ii] == 'Euronext Paris':
			all_tags.append('%s.PA' % div.text)
		elif all_market_names[ii] == 'SIX Swiss':
			all_tags.append('%s.SW' % div.text)
		else:
			all_tags.append('%s' % div.text)
		#print(all_tags[-1])
	return all_tags, all_market_names