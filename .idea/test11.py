import pandas as pd

# Define custom column names
column_names = ['date', 'team', 'name', 'notes']

# Read the comparison and input CSV files without headers (header=None)
comparison_df = pd.read_csv('onWrist.csv', header=None, names=column_names)
input_df = pd.read_csv('../.idea/transactions_dataNA.csv', header=None, names=column_names)

# Strip any leading or trailing spaces from column names
comparison_df.columns = comparison_df.columns.str.strip()
input_df.columns = input_df.columns.str.strip()

# Check the column names to ensure 'date' exists
print("Comparison CSV columns:", comparison_df.columns)
print("Input CSV columns:", input_df.columns)

# Make sure the 'date' columns are in datetime format
comparison_df['date'] = pd.to_datetime(comparison_df['date'], errors='coerce')
input_df['date'] = pd.to_datetime(input_df['date'], errors='coerce')

# Check for any invalid dates after conversion
print("Comparison CSV dates:", comparison_df['date'].head())
print("Input CSV dates:", input_df['date'].head())

# Initialize an empty list to hold the new rows for the output CSV
output_rows = []

# Iterate through each row in the comparison DataFrame
for idx, comparison_row in comparison_df.iterrows():
    # Find the rows in the input DataFrame where the date is greater than the comparison date
    matching_rows = input_df[(input_df['date'] > comparison_row['date']) &
                             (input_df['name'] == comparison_row['name'])]

    # If matching rows are found, take the first match and add it to the output rows
    if not matching_rows.empty:
        matching_row = matching_rows.iloc[0]
        # Create a new row with the relevant columns from the comparison and input data
        output_row = {
            'date': matching_row['date'],
            'team': matching_row['team'],
            'name': matching_row['name'],
            'notes': matching_row['notes']
        }
        output_rows.append(output_row)

# Convert the output rows into a DataFrame
output_df = pd.DataFrame(output_rows)

# Save the output DataFrame to a new CSV file
output_df.to_csv('offWrist.csv', index=False)

print("Output CSV has been created successfully!")
