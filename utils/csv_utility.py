import csv
from datetime import datetime


class CSVUtility:

    @staticmethod
    def create_csv(header_fields, data, item_ids_list, file_name):
        csv_filename = '{}_{}.csv'.format(file_name, str(datetime.utcnow()))

        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=header_fields)
            writer.writeheader()

            for item in item_ids_list:
                data_to_write = data[item]
                writer.writerow(data_to_write) 