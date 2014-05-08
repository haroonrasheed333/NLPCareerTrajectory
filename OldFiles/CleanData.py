import csv

rows = []
with open('univ_degree_title_4-11-14.csv', 'rb') as univ_file:
    csv_reader = csv.reader(univ_file)

    with open('../univ_degree_title_4-11-14_new.csv', 'wb') as univ_write_file:
        csv_writer = csv.writer(univ_write_file)
        for row in csv_reader:
            try:
                if row[0] and row[1] and row[2] and row[3]:
                    rows.append(row)
                    csv_writer.writerow(row)
            except:
                pass

        print len(rows)

rows = []
with open('univ_degree_employer_4-11-14.csv', 'rb') as univ_file:
    csv_reader = csv.reader(univ_file)

    with open('../univ_degree_employer_4-11-14_new.csv', 'wb') as univ_write_file:
        csv_writer = csv.writer(univ_write_file)
        for row in csv_reader:
            try:
                if row[0] and row[1] and row[2] and row[3]:
                    rows.append(row)
                    csv_writer.writerow(row)
            except:
                pass

        print len(rows)

rows = []
with open('univ_degree_employer_title4-11-14.csv', 'rb') as univ_file:
    csv_reader = csv.reader(univ_file)

    with open('../univ_degree_employer_title4-11-14_new.csv', 'wb') as univ_write_file:
        csv_writer = csv.writer(univ_write_file)
        for row in csv_reader:
            try:
                if row[0] and row[1] and row[2] and row[3]:
                    rows.append(row)
                    csv_writer.writerow(row)
            except:
                pass

        print len(rows)