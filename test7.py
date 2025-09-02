import requests
import csv
from bs4 import BeautifulSoup

def get_position_from_player_page(url):
    # Send a request to fetch the player's page
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: Could not retrieve data from {url}. Status code {response.status_code}")
        return None

    # Parse the player's page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Try to find the player's position
    position = None
    try:
        # Find the <strong> tag with "Position:" text
        position_tag = soup.find('strong', string='Position:')
        if position_tag:
            # The next sibling should contain the position text (e.g., "Third Baseman")
            position = position_tag.find_next_sibling(string=True).strip()
            return position  # Return the position immediately if found
        else:
            print("Position not found in the expected location.")
    except AttributeError:
        print("Error while parsing the player position.")

    return position

def getRidofPitchers(readFileName, writeFileName):
    # Open the people.csv file properly using csv.reader
    with open('people.csv', 'r', newline='', encoding='utf-8') as people_file:
        people_reader = csv.reader(people_file)
        people_data = list(people_reader)  # Load all people data into memory for later comparison

    with open(readFileName, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)

        with open(writeFileName, 'a', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)

            for row in reader:
                # Safely handle splitting first and last name
                try:
                    name = str(row[2]).replace('•', '').split()
                    firstName, lastName = name[0], name[1]  # Assuming the name has two parts
                except ValueError:
                    print(f"Skipping row with invalid name format: {row[2]}")
                    continue  # Skip rows with invalid name format

                # Loop through people.csv to find matching first and last names
                for row2 in people_data:
                    # Check if the names match
                    if lastName == str(row2[12]) and firstName == str(row2[13]):
                        letter = lastName[0].lower()
                        testURL = f'https://www.baseball-reference.com/players/'+letter+'/'+str(row2[4])+'.shtml'

                        if get_position_from_player_page(testURL) != 'Pitcher':  # Check if the URL exists
                            writer.writerow(row)  # Write the modified row to the new file


# Calling the function with file names
getRidofPitchers('transactions_dataFA.csv', 'transactions_dataNA.csv')
getRidofPitchers('transactions_dataFD.csv', 'transactions_dataND.csv')
#player_url = "https://www.baseball-reference.com/players/s/snellbl01.shtml"  # Example URL
#position = get_position_from_player_page(player_url)

#if position:
    #print(f"Player's position is {position}.")
#else:
    #print("Could not find the position.")