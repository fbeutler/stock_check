
import sys, os
from matplotlib import pyplot as plt

from harvest_trading212 import get_tags


def main():

	exclude = ['NON-ISA OTC Markets']

	tags, markets = get_tags()

	filename = 'existing_tags2.txt'
	# Check whether file exists... in which case we might attach
	pbratios = []
	tags = []
	global_ids = []
	pb_dict = {}
	if os.path.isfile(filename):
		with open(filename, 'r') as f:
			for line in f:
				if line[0] != '#':
					dummy = line.split()
					if markets[int(dummy[-1])] not in exclude:
						tags.append(dummy[0])
						pbratios.append(float(dummy[1]))
						pb_dict[dummy[-1]] = float(dummy[1])
						global_ids.append(dummy[-1])

	filename = 'existing_tags_pe.txt'
	# Check whether file exists... in which case we might attach
	pe_dict = {}
	if os.path.isfile(filename):
		with open(filename, 'r') as f:
			for line in f:
				if line[0] != '#':
					dummy = line.split()
					if markets[int(dummy[-1])] not in exclude:
						pe_dict[dummy[-1]] = float(dummy[1])

	filename = 'existing_tags_sector.txt'
	# Check whether file exists... in which case we might attach
	sector_dict = {}
	industry_dict = {}
	if os.path.isfile(filename):
		with open(filename, 'r') as f:
			for line in f:
				if line[0] != '#':
					dummy = line.split(', ')
					if markets[int(dummy[-1])] not in exclude:
						sector_dict[int(dummy[-1])] = dummy[1]
						industry_dict[int(dummy[-1])] = dummy[2]

	filename = 'existing_tags_country.csv'
	# Check whether file exists... in which case we might attach
	country_dict = {}
	if os.path.isfile(filename):
		with open(filename, 'r') as f:
			for line in f:
				if line[0] != '#':
					dummy = line.split(',')
					country_dict[int(dummy[-1])] = dummy[1]

	max_num = 200
	max_dict = {'Financial Services': 0.20, 
				'Real Estate': 0.1, 'Energy': 0.1,
				'Argentina': 0.01, 'Greece': 0.01,
				'Bermuda': 0.0, 'Panama': 0.0, 'Monaco': 0.0, 'Cayman Islands': 0.0}

	counter = 0
	zipped_lists = zip(pbratios, tags, global_ids)
	sorted_zipped_lists = sorted(zipped_lists)
	sectors = []
	industries = []
	countries = []
	for pbratio, tag, global_id in sorted_zipped_lists:
		if global_id in pe_dict and int(global_id) in sector_dict and int(global_id) in country_dict:
			if ((sector_dict[int(global_id)] in max_dict and 
				sectors.count(sector_dict[int(global_id)]) < max_num*max_dict[sector_dict[int(global_id)]]) or
				sector_dict[int(global_id)] not in max_dict):

				if ((country_dict[int(global_id)] in max_dict and 
					countries.count(country_dict[int(global_id)]) < max_num*max_dict[country_dict[int(global_id)]]) or
					country_dict[int(global_id)] not in max_dict):
					print(tag, pbratio, pe_dict[global_id], markets[int(global_id)], sector_dict[int(global_id)], industry_dict[int(global_id)], country_dict[int(global_id)])
					sectors.append(sector_dict[int(global_id)])
					industries.append(industry_dict[int(global_id)])
					countries.append(country_dict[int(global_id)])

					counter += 1
					if counter == max_num:
						break

	unique_countries = list(set(countries))
	num_countries = []
	for el in unique_countries:
		num_countries.append(countries.count(el))

	print("unique_countries = ", unique_countries)
	print("num_countries = ", num_countries)

	plt.pie(num_countries, labels=unique_countries, autopct='%1.2f%%')
	plt.show()

	unique_industries = list(set(industries))
	num_industries = []
	for el in unique_industries:
		num_industries.append(industries.count(el))

	print("unique_industries = ", unique_industries)
	print("num_industries = ", num_industries)

	plt.pie(num_industries, labels=unique_industries, autopct='%1.2f%%')
	plt.show()

	unique_sectors = list(set(sectors))
	num_sectors = []
	for el in unique_sectors:
		num_sectors.append(sectors.count(el))

	print("unique_sectors = ", unique_sectors)
	print("num_sectors = ", num_sectors)

	plt.pie(num_sectors, labels=unique_sectors, autopct='%1.2f%%')
	plt.show()
	return 


if __name__ == "__main__":
    main()
