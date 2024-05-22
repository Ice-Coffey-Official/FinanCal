from itertools import product

import json
from multiprocessing import current_process
from util.customLogger import customLogging
import os

logger = customLogging("utilLogger").getLogger()

# Read the existing JSON data from the file
def read_json(filename='data.json'):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File '{filename}' not found. Creating a new one with an empty dictionary.")
        data = {}
        logger.info(filename + " is the filename")
        try:
            with open(filename, 'w+') as new_file:
                json.dump(data, new_file)
        except FileNotFoundError:
            os.mkdir(filename.split('/')[0])
            with open(filename, 'w+') as new_file:
                json.dump(data, new_file)
        return data

# Append new data to the JSON object
def append_to_json(key, new_data, filename='results/data'):
    pid = str(current_process().pid)
    filename = "{}{}{}".format(filename,pid,'.json')
    logger.info("saving to {}".format(filename))
    data = read_json(filename)
    if(key not in data):
        data[key] = []
    data[key].append(new_data)

    # Write the updated data back to the file
    with open(filename, 'w+') as file:
        json.dump(data, file, indent=4)

def generate_urls(base_url, years, expense_types, cities):
    pid = str(current_process().pid)
    # Generate all combinations of the three lists
    all_combinations = product(years, expense_types, cities)
    
    # Replace placeholders in the base URL with values from each combination
    urls = []
    for year, expense_type, city in all_combinations:
        url = base_url.format(year=year, expenseType=expense_type, city=city)
        urls.append((url, city, expense_type, year, pid))
    
    return urls