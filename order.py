
import sys, os


def main():

	filename = 'existing_tags.txt'
	# Check whether file exists... in which case we might attach
	pbratios = []
	tags = []
	price = []
	bvalue = []
	if os.path.isfile(filename):
		with open(filename, 'r') as f:
			for line in f:
				if line[0] != '#':
					dummy = line.split()
					if dummy[14] != 'None' and float(dummy[14]) > 0:
						tags.append(dummy[0])
						price.append(float(dummy[2]))
						print("price[-1] = ", price[-1])
						bvalue.append(float(dummy[14]))
						print("bvalue[-1] = ", bvalue[-1])
						pbratios.append(price[-1]/bvalue[-1])

	zipped_lists = zip(pbratios, tags)
	sorted_zipped_lists = sorted(zipped_lists)
	for pbratio, tag in sorted_zipped_lists:
		print(tag, pbratio)
	return 


if __name__ == "__main__":
    main()
