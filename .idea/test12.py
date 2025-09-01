import csv
onElbow = open('onElbow.csv','w')
file4 = open('../.idea/transactions_dataND.csv', 'r')
for line in file4:
    if 'elbow' in line:
        onElbow.write(line)
onElbow.close()
file4.close()