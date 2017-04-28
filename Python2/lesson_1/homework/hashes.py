import csv
import hashlib

csv.register_dialect('excel-semicolon', delimiter=';')

with open('need_hashes.csv', 'r', encoding='UTF-8') as f:
    reader = csv.reader(f, dialect="excel-semicolon")
    readed = [row for row in reader]

with open('need_hashes.csv', 'w', encoding='UTF-8') as f:
    writer = csv.writer(f, dialect="excel-semicolon")
    for row in readed:
        if not row[2]:
            if row[1] == 'md5':
                h = hashlib.md5()
                h.update(row[0].encode('koi8-r'))
            elif row[1] == 'sha512':
                h = hashlib.sha512()
                h.update(row[0].encode('koi8-r'))
            elif row[1] == 'sha1':
                h = hashlib.sha1()
                h.update(row[0].encode('koi8-r'))
            writer.writerow([row[0], row[1], h.hexdigest()])
        else:
            writer.writerow(row)
