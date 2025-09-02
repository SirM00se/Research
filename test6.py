from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time
import unicodedata
from datetime import datetime
from dateutil.relativedelta import relativedelta
import csv
import os
import shutil
def click_anywhere(driver, x_offset=0, y_offset=600):
    actions = ActionChains(driver)
    actions.move_by_offset(x_offset, y_offset).click().perform()
def get_most_recent_file(download_dir, file_extension='.csv'):
    # List all files in the directory
    files_in_dir = os.listdir(download_dir)

    # Filter files by the desired extension
    csv_files = [file for file in files_in_dir if file.endswith(file_extension)]

    if not csv_files:
        raise FileNotFoundError(f"No {file_extension} files found in the directory.")

    # Get the most recent file based on modification time
    most_recent_file = max(csv_files, key=lambda f: os.path.getmtime(os.path.join(download_dir, f)))

    return most_recent_file
def close_modal_if_present(driver):
    try:
        # Try to click the close button of the modal
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@class="close"]')))  # Modify this XPath to match the modal close button
        close_button.click()
    except Exception as e:
        print("No modal found or close button not clickable:", e)
def wait_for_modal_to_disappear(driver, timeout=10):
    try:
        # Wait for the modal to disappear (e.g., by checking for its invisibility)
        WebDriverWait(driver, timeout).until(EC.invisibility_of_element_located((By.CLASS_NAME, "MuiDialog-container")))
    except Exception as e:
        print(f"Error waiting for modal: {e}")
def wait_for_download(download_dir, expected_file_extension='.csv', timeout=60):
    start_time = time.time()
    while True:
        files_in_dir = os.listdir(download_dir)
        for file in files_in_dir:
            if file.endswith(expected_file_extension):
                file_path = os.path.join(download_dir, file)
                initial_size = os.path.getsize(file_path)
                time.sleep(1)
                final_size = os.path.getsize(file_path)
                if initial_size == final_size:
                    return file
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Download did not complete within {timeout} seconds.")
        time.sleep(1)
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def getPlayerData(id, start, end, num):
    # Set up Chrome options to specify download directory
    download_dir = r'/Data'  # Replace with your desired folder (Windows example)

    # Set up the Chrome Options object
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Optionally run Chrome in headless mode (without GUI)
    chrome_options.add_argument('--no-sandbox')  # For headless mode on certain systems
    chrome_options.add_argument('--disable-dev-shm-usage')  # Disable shared memory usage

    # Set the custom download directory
    chrome_options.add_experimental_option('prefs', {
        "download.default_directory": download_dir,  # Set custom download directory
        "download.prompt_for_download": False,  # Disable download prompt
        "directory_upgrade": True  # Allows overwriting existing files
    })

    # Set up the Chrome service and WebDriver
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open the website
    url = f'https://www.fangraphs.com/splitstool-legacy.aspx?playerid={id}&splitArr=&splitArrPitch=&autoPt=false&splitTeams=false&statType=player&statgroup=1&startDate={start}&endDate={end}&players=&filter=&groupBy=career&wxTemperature=&wxPressure=&wxAirDensity=&wxElevation=&wxWindSpeed=&sort=-1,1'
    driver.get(url)

    # Wait for the page to load

    # Find the "Export Data" button by inspecting the element
    wait = WebDriverWait(driver, 10)
    click_anywhere(driver)
    click_anywhere(driver)
    # Try to find the "Export Data" button
    try:
        export_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="data-export"]')))
    except TimeoutException:
        print("Export Data button not found. Stopping the function.")
        driver.quit()  # Close the browser if the button is not found
        return 1# Exit the function if the button is not found

    # Click the "Export Data" button
    export_link.click()

    # Wait for download to complete
    downloaded_file = wait_for_download(download_dir, expected_file_extension='.csv')



    # Close the browser
    driver.quit()

    # Print confirmation
    print(f"File has been downloaded")


def emptyrow(target_csv):
    with open(target_csv, mode='a', newline='') as tgt_file:
        csv_writer = csv.writer(tgt_file)
        # Append the row to the target CSV
        csv_writer.writerow([])
def append_row_to_csv(source_csv, target_csv):
    # Open the source CSV to read the row
    with open(source_csv, mode='r', newline='') as src_file:
        csv_reader = csv.reader(src_file)
        # Read the first row from the source CSV
        next(csv_reader)
        row = next(csv_reader)

    # Open the target CSV to append the row
    with open(target_csv, mode='a', newline='') as tgt_file:
        csv_writer = csv.writer(tgt_file)
        # Append the row to the target CSV
        csv_writer.writerow(row)
def player(readerfile,writerfile):
    with open('people.csv', 'r', newline='', encoding='utf-8') as people_file:
        people_reader = csv.reader(people_file)
        people_data = list(people_reader)  # Load all people data into memory for later comparison


    with open(readerfile, 'r', newline='', encoding='utf-8') as infile:
        num = -1
        reader = csv.reader(infile)
        next(reader)
        for row in reader:
            num += 1
            print(len(row))
            print(row)
            if len(row) < 4:
                print(f"Skipping row with insufficient data: {row}")
                continue
            # Safely handle splitting first and last name
            try:
                name = str(row[3]).replace('•', '').strip().split()
                firstName = name[0]  # The first element is always the first name
                lastName = name[1] if len(name) > 1 else ''  # The second element is the last name if available
            except ValueError:
                print(f"Skipping row with invalid name format: {row[2]}")
                continue  # Skip rows with invalid name format

            for row2 in people_data:
                # Check if the names match
                if lastName == remove_accents(str(row2[12])) and firstName == remove_accents(str(row2[13])):
                    id = row2[6]
                    end = row[0]
                    date_obj = datetime.strptime(end, "%Y-%m-%d").date()
                    start = date_obj - relativedelta(years=2)
            if (getPlayerData(id,start,end,num) != 1):
                most_recent_file = get_most_recent_file(r'/Data', file_extension='.csv')
                most_recent_file_path = os.path.join(r'/Data', most_recent_file)
                append_row_to_csv(most_recent_file_path, writerfile)
            else:
                emptyrow(writerfile)
player('backup.csv','befElbow.csv')