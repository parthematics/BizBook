import csv

def format_data(tsv_file="raw_data.tsv"):
	concatenated_terms = []
	output_file = "cleaned_data.tsv"
	
	with open(tsv_file, 'r') as f:
		file = csv.reader(f, delimiter='\t')
		for line in file:
			parent = line[0]
			children = line[1].split(", ")
			for child in children:
				concatenated_terms.append([parent + ", " + child, parent])
		f.close()

	with open(output_file, 'w') as f:
		for tup in concatenated_terms:
			f.write('%s\t%s\n' % (tup[0], tup[1]))
		f.close()

if __name__ == "__main__":
	format_data()
