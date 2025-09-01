from baseball_scraper import fangraphs
import pandas as pd
player_id = 19755
fg = fangraphs.Scraper("Steamer (RoS)")
df = fg.scrape(player_id, scrape_as=fangraphs.ScrapeType.HITTER)
df.columns
Index(['index', 'Name', 'Team', 'G', 'PA', 'AB', 'H', '2B', '3B', 'HR', 'R',
       'RBI', 'BB', 'SO', 'HBP', 'SB', 'CS', '-1', 'AVG', 'OBP', 'SLG', 'OPS',
       'wOBA', '-1.1', 'wRC+', 'BsR', 'Fld', '-1.2', 'Off', 'Def', 'WAR',
       'playerid'],
      dtype='object')
df