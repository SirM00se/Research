import csv
file = open('../.idea/transactions_data3.csv', 'r')
file2 = open('../.idea/transactions_dataD.csv', 'w')
file3 = open('../.idea/transactions_dataA.csv', 'w')
for line in file:
    if "activated" in line:
        file3.write(line)
    else:
        file2.write(line)
    print('row complete')
file.close()
file2.close()
file3.close()