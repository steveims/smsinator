import argparse
from csv import DictReader
import json


def main():
    parser = argparse.ArgumentParser(description='send sms')
    parser.add_argument('csv_file', help='CSV file with phone_number, name')

    args = parser.parse_args()

    directory = {}
    with open(args.csv_file, 'r') as f:
        reader = DictReader(f)
        assert 'name' in reader.fieldnames and 'phone_number' in reader.fieldnames, 'missing required fieldnames: names, phone_number'


        for row in reader:
            k = '+1' + ''.join([c for c in row["phone_number"] if c.isdigit()])
            directory[k] = row["name"]

    with open('directory.json', 'w') as f:
        json.dump(directory, f)


    print('results saved to directory.json')
