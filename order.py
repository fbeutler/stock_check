
import sys, os


def main():

	filename = 'existing_tags2.txt'
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
					tags.append(dummy[0])
					pbratios.append(float(dummy[1]))

	zipped_lists = zip(pbratios, tags)
	sorted_zipped_lists = sorted(zipped_lists)
	for pbratio, tag in sorted_zipped_lists:
		print(tag, pbratio)
	return 


if __name__ == "__main__":
    main()
