from selenium.webdriver.firefox.service import Service # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium import webdriver # type: ignore
import pandas as pd # type: ignore
import os

service = Service()
options = webdriver.FirefoxOptions()
options.add_argument("--headless")

driver = webdriver.Firefox(service=service, options=options)
driver.get('https://hoopshype.com/salaries/players/')

players = driver.find_elements(By.XPATH, '//td[@class="name"]')
players_list = []
for p in range(len(players)):
   players_list.append(players[p].text)

salaries = driver.find_elements(By.XPATH, '//td[@class="hh-salaries-sorted"]')
salaries_list = []
for s in range(len(salaries)):
   salaries_list.append(salaries[s].text)

driver.quit()

player_salaries = dict(zip(players_list, salaries_list))
player_salaries_df = pd.DataFrame(player_salaries.items())

header = player_salaries_df.iloc[0]
player_salaries_df = player_salaries_df[1:]
player_salaries_df.columns = header

print(player_salaries_df.head())

os.makedirs('output', exist_ok=True)
player_salaries_df.to_csv('output/player_salaries.csv')