import os
import pandas as pd
import sqlite3
import re

df = pd.read_csv('semi-data.csv')

def clean_string(s):
    # Replace non-alphanumeric characters except hyphens with hyphens
    s = re.sub(r'[^\w\s-]', '', s)
    # Replace multiple consecutive hyphens with a single hyphen
    s = re.sub(r'-+', '-', s)
    # Strip leading or trailing hyphens
    s = s.strip('-')
    return s

def remove_dimensions(name):
    # Improved regex to remove dimension formats
    # Matches dimensions like 74-cm, 105x36-cm, 100x200x50cm, etc.
    name = re.sub(r'(\d+\s*[-xX]\s*\d+(\s*[-xX]\s*\d+)?\s*(cm|cm\.|cm|cm\.|cm)|\d+\s*(cm|cm\.|cm|cm\.|cm)|\d+\s*x\s*\d+\s*(cm|cm\.|cm|cm\.|cm)|\d+\s*x\s*\d+\s*x\s*\d+\s*(cm|cm\.|cm|cm\.|cm))', '', name, flags=re.IGNORECASE)
    name = re.sub(r'-+', '-', name).strip('-')
    return name

master_path = 'database/images'
data = []

# Process each file in the master_path directory
for index, row in df.iterrows():
    path = str(row.iloc[-2])
    description = str(row.iloc[-1])
    
    path_no_ext = path.replace('.jpg', '')

    path_no_ext = path_no_ext.replace('database/images\\', '')

    readable = path_no_ext.split(',')
    if not readable:
        continue
    readable = readable[0].split('-')
    readable = [clean_string(name) for name in readable]

    # Determine the split index for categories and names
    split_index = 6  # Adjust if necessary

    if len(readable) > split_index:
        categories = readable[:split_index]
        names = readable[split_index:]
    else:
        categories = readable
        names = []

    # Handle empty names
    f_cate = [category for category in categories if category]
    f_name = [remove_dimensions(name) for name in names if name]

    f_cate_str = '-'.join(f_cate) if f_cate else 'Unknown-Category'
    f_name_str = '-'.join(f_name) if f_name else 'Unknown-Name'

    f_name_str = f_name_str.split('-')

    remove = ['cm', 'mm', 'm']

    for i in remove:
        if i in f_name_str:
            f_name_str.remove(i)
            del f_name_str[-1]
            if f_name_str[-1].isnumeric():
                del f_name_str[-1]
    
    f_name_str = '-'.join(f_name_str)

    

    data.append((f_cate_str, f_name_str, path, description))

# Convert data to a pandas DataFrame
df = pd.DataFrame(data, columns=['Category', 'Name', 'Image Path', 'Description'])

# Save DataFrame to a CSV file
csv_filename = 'final.csv'
df.to_csv(csv_filename, index=False)

print(f"Data has been saved to {csv_filename}")


