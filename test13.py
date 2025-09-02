import csv

maxwOBA = 0
numwOBA = 0
rows = []

# Open the CSV file for reading and writing
with open('../Data/befShould2.csv', 'r') as file:
    reader = csv.reader(file)

    # Skip the header row
    header = next(reader)
    rows.append(header)  # Store header separately

    # Iterate through the data rows
    for row in reader:
        # Convert values to floats and calculate wOBA
        try:
            wOBA = ((0.689*(float(row[12])-float(row[13]))) +
                    (0.72*float(row[15])) +
                    (0.882*float(row[6])) +
                    (1.254*float(row[7])) +
                    (1.59*float(row[8])) +
                    (2.05*float(row[9]))) / (
                           float(row[4]) + float(row[12]) - float(row[13]) +
                           float(row[16]) + float(row[15]))
            print(wOBA)
            row[22] = wOBA
            maxwOBA += wOBA
            numwOBA += 1
        except ValueError:
            # Skip rows where data is invalid (e.g., empty cells or non-numeric values)
            print("Error in data row:", row)

        rows.append(row)  # Store modified row

# Calculate average wOBA
print("Average wOBA:", maxwOBA / numwOBA)

# Write the modified rows back to the CSV file
with open('befShould2.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)