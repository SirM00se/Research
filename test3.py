import csv
file = open('../Data/transactions_data2.csv', 'r')
file2 = open('../Data/transactions_data5.csv', 'w')
for line in file:
    if "60-day" in line:
        file2.write(line)
    print('row complete')
file.close()
file2.close()