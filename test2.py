import requests
import pandas as pd
from bs4 import BeautifulSoup
baseurl = "https://www.prosportstransactions.com/baseball/Search/SearchResults.php?Player=&Team=&BeginDate=2016-03-01&EndDate=2022-11-01&DLChkBx=yes&submit=Search&start="
def fetchpagedata(startvalue):
    url = baseurl+str(startvalue)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'datatable'})
    rows = []
    for row in table.find_all('tr')[1:]:  # Skip the header
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        rows.append(cols)
    return rows
allrows = []
for x in range(0,12076,25):
    pagedata = fetchpagedata(x)
    allrows.extend(pagedata)
    print("page:"+str(x/25)+"complete")
df = pd.DataFrame(allrows, columns=["Date", "Team", "Acquired", "Relinquished", "Notes"])
df.to_csv('transactions_data2.csv', index=False)

print("Data has been saved to transactions_data2.csv")