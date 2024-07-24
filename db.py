import os
import pandas as pd

master_path = 'database/images1'
data = []

for path in os.listdir(master_path):
    readable = path.split('-')

    f_name = []
    f_cate = []

    readable = readable[:12]
    names = readable[6:]
    categories = readable[:3]
    print(names)
    for category in categories:
        if category.isalpha():
            f_cate.append(category)

    for name in names:
        if name.isalpha():
            f_name.append(name)

    if len(f_cate) > 1:
        f_cate = '-'.join(f_cate)
    else:
        f_cate = f_cate[-1]

    if len(f_name) > 1:
        f_name = '-'.join(f_name)
    else:
        f_name = f_name[-1]

    path = master_path + '/' + path
    temp = [f_cate, f_name, path]
    data.append(temp)

print(data)

df = pd.DataFrame(data, columns=['Category', 'Name', 'Path'])

filename = 'images_db.csv'

df.to_csv(filename, index=False)
