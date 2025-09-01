import os
import csv

# Function to append contents of CSV files to an existing target CSV file
def append_csv_files(folder_path, target_file):
    # List all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file is a CSV file
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, mode='r', newline='', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                # Open the target CSV file in append mode
                with open(target_file, mode='a', newline='', encoding='utf-8') as outfile:
                    writer = csv.writer(outfile)
                    # Loop through each row in the current CSV and write it to the target file
                    for row in reader:
                        writer.writerow(row)
            print(f'Appended data from {filename}')

# Define the folder containing the CSV files and the target CSV file
folder_path = r'C:\Users\Blake\IdeaProjects\Research\.idea\people'  # replace with your folder path
target_file = r'C:\Users\Blake\IdeaProjects\Research\.idea\people.csv'  # replace with the path to your target CSV

# Call the function to append CSV files into the target CSV
append_csv_files(folder_path, target_file)

print('All CSV files have been appended to the target CSV.')
