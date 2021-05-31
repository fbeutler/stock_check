
import sys, os
from matplotlib import pyplot as plt

from harvest_trading212 import get_tags

max_num = 200
market_exclude = ['NON-ISA OTC Markets']
country_exclude = ['Cayman Islands', 'Monaco', 'Panama', 'Bermuda', 'Argentina', 'Greece']
max_dict = {'Financial Services': 0.20, 
			'Real Estate': 0.1, 'Energy': 0.1}

def get_data(filename, col_id=1, exclude=[], sep=' '):

	out_dict = {}
	if os.path.isfile(filename):
		with open(filename, 'r') as f:
			for line in f:
				if line[0] != '#':
					dummy = line.split(sep)
					if dummy[col_id] and int(dummy[-1]) not in exclude:
						out_dict[int(dummy[-1])] = dummy[col_id]
		return out_dict
	else:
		return None


def check(dummy_dict, dummy, global_id):
	return ((dummy_dict[global_id] in max_dict and 
		     dummy.count(dummy_dict[global_id]) < max_num*max_dict[dummy_dict[global_id]]) or
			 dummy_dict[global_id] not in max_dict)


def cook_pie(ingredients):
	unique_ingredients = list(set(ingredients))
	num_ingredients = [ingredients.count(ingredient) for ingredient in unique_ingredients]

	plt.pie(num_ingredients, labels=unique_ingredients, autopct='%1.2f%%')
	plt.show()
	return 


def main():

	tags, markets = get_tags()

	filename = 'existing_tags2.txt'
	# Check whether file exists... in which case we might attach
	pbratios = []
	tags = []
	global_ids = []
	if os.path.isfile(filename):
		with open(filename, 'r') as f:
			for line in f:
				if line[0] != '#':
					dummy = line.split()
					tags.append(dummy[0])
					pbratios.append(float(dummy[1]))
					global_ids.append(int(dummy[-1]))

	filename = 'existing_tags2.txt'
	pb_dict = get_data(filename, sep=' ')
	for k, v in pb_dict.items():
		pb_dict[k] = float(v)

	filename = 'existing_tags_pe.txt'
	pe_dict = get_data(filename, sep=' ')
	for k, v in pe_dict.items():
		pe_dict[k] = float(v)

	filename = 'existing_tags_sector.txt'
	sector_dict = get_data(filename, col_id=1, sep=', ')
	industry_dict = get_data(filename, col_id=2, sep=', ')

	filename = 'existing_tags_country.csv'
	country_dict = get_data(filename, sep=',')

	counter = 0
	zipped_lists = zip(pbratios, tags, global_ids)
	sorted_zipped_lists = sorted(zipped_lists)
	sectors = []
	industries = []
	countries = []
	for pbratio, tag, global_id in sorted_zipped_lists:
		if global_id in pe_dict and global_id in country_dict:

			if (markets[global_id] not in market_exclude and 
				country_dict[global_id] not in country_exclude):

				if check(sector_dict, sectors, global_id) and check(country_dict, countries, global_id):

					print("%s, %f, %f, %s, %s, %s, %s" % (tag, pbratio, pe_dict[int(global_id)], markets[int(global_id)], sector_dict[int(global_id)], industry_dict[int(global_id)], country_dict[int(global_id)]))
					sectors.append(sector_dict[int(global_id)])
					industries.append(industry_dict[int(global_id)])
					countries.append(country_dict[int(global_id)])

					counter += 1
					if counter == max_num:
						break

	cook_pie(countries)
	cook_pie(industries)
	cook_pie(sectors)
	return 


if __name__ == "__main__":
    main()
