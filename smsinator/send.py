# Download the helper library from https://www.twilio.com/docs/python/install
import argparse
from csv import DictReader, DictWriter
import os
from twilio.rest import Client


def main():
    parser = argparse.ArgumentParser(description='send sms')
    parser.add_argument('csv_file', help='CSV file with phone_number, name')
    parser.add_argument('message', help='message, with optional {name}')

    args = parser.parse_args()

    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    with open(args.csv_file, 'r') as r, open(f'{args.csv_file}.failed', 'w') as w:

        reader = DictReader(r)
        assert 'name' in reader.fieldnames and 'phone_number' in reader.fieldnames, 'missing required fieldnames: names, phone_number'

        writer = DictWriter(w, reader.fieldnames)
        writer.writeheader()

        attempts = 0
        failed = 0

        for row in reader:
            attempts += 1
            try:
                print(f'sending to {row["name"]} @ {row["phone_number"]}')
                assert row['name'] and row['phone_number'], 'name and phone_number are required'

                message = client.messages.create(
                        messaging_service_sid='MGcfadc2cf6a443e9bed782a44923dfc03',
                        body=args.message.format(name=row['name']),
                        to=row['phone_number'])
    
            except Exception as x:
                failed += 1
                print(f'ERROR: {x}')
                writer.writerow(row)

    print(f'{attempts} records processed; {failed} failed')
