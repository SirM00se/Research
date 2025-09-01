import csv

def add_matching_player_row(input_csv, comparison_csv, output_csv, player_column_index=2):
    # Read the player names from the comparison CSV into a set for faster lookup
    comparison_players = set()
    with open(comparison_csv, mode='r', newline='') as comp_file:
        comp_reader = csv.reader(comp_file)
        # Assuming the player names are in the first column (index 0)
        for row in comp_reader:
            comparison_players.add(row[player_column_index])  # Adjust if the player name is in a different column

    # Open the input CSV to read the rows
    with open(input_csv, mode='r', newline='') as input_file:
        input_reader = csv.reader(input_file)

        # Open the output CSV to write the matching rows
        with open(output_csv, mode='w', newline='') as output_file:
            output_writer = csv.writer(output_file)

            for row in input_reader:
                # Check if the player name in the row exists in the comparison set
                if row[player_column_index] in comparison_players:
                    # Write the row to the output CSV if there's a match
                    output_writer.writerow(row)

# Example usage
input_csv = 'transactions_dataFD.csv'
comparison_csv = 'transactions_dataFA.csv'
output_csv = 'transactions_dataND.csv'

add_matching_row(input_csv, comparison_csv, output_csv)