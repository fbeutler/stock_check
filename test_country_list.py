from harvest_trading212 import get_tags
from scrape_pb import get_country

def main():
	# Get list of ticker symbols from trading212
	tags = get_tags()
	print("num of tags: %d" % len(tags))

	filename = 'existing_tags_country.csv'
	with open(filename, 'w') as f: 
		f.write('tag,country,tag_id\n')
		for i, tag in enumerate(tags):
			if tag[0] not in ['2', '3', '4', '5', '6', '8']:
				value = get_country(tag, i)
				if value:
					#print("found %s of %s\n" % (value, tag))
					f.write("%s,%s,%d\n" % (tag, value, i))

	return


if __name__ == "__main__":
    main()
