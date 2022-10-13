import csv,argparse,sys
lists = []
parser = argparse.ArgumentParser(description='Process CSV File Filter')
parser.add_argument("-o",type=str,help='File Name for the Old CSV File')
parser.add_argument("-n",type=str,help='File Name for the New CSV output File')
parser.add_argument("-f",type=str,help='Filter String for CSV File Input')
args = parser.parse_args()
if len(sys.argv) == 1:
    sys.exit("Missing Arguments")
with open(args.o) as file:
    reader = csv.reader(file)
    fieldnames = next(reader)
    for row in reader:
        if args.f in row[0]:
            lists.append(row)

with open(args.n,"w") as file2:
    writer = csv.writer(file2)
    writer.writerow(fieldnames)
    for list in lists:
        writer.writerow(list)
