import csv
file = open('../Data/transactions_data6.csv', 'r')
file2 = open('../Data/transactions_dataD.csv', 'r')
file3 = open('../Data/transactions_dataFD.csv', 'w')
for line in file:
    if ("placed" in line) or ("transferred" in line):
        file3.write(line)
    print('row complete')
file.close()
for line in file2:
    if ("placed" in line) or ("transferred" in line):
        file3.write(line)
    print('row complete')
file2.close()
file3.close()