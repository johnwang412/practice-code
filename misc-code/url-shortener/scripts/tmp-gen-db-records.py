import csv
import random
import string
import argparse


def generate_csv(filename, n):
    short_codes = set()
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['original_url', 'short_code', 'created_at'])
        for _ in range(n):
            domain = ''.join(random.choices(string.ascii_lowercase, k=12))
            path = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            original_url = f'https://{domain}.com/{path}'
            short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            while short_code in short_codes:
                short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            short_codes.add(short_code)
            created_at = "2025-07-24 08:08:08"
            writer.writerow([original_url, short_code, created_at])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a CSV file with random URL records.')
    parser.add_argument('file_name', nargs='?', default='test_urls.csv', help='Output CSV file name')
    parser.add_argument('num_records', nargs='?', type=int, default=100000000, help='Number of records to generate')
    args = parser.parse_args()

    generate_csv(args.file_name, args.num_records)
