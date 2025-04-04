from selenium.webdriver.firefox.service import Service # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium import webdriver # type: ignore
import pandas as pd # type: ignore
import os

import pytest # type: ignore

class TestScraper:
    def test_driver_get(self):
        service = Service()
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")

        driver = webdriver.Firefox(service=service, options=options)
        driver.get('https://hoopshype.com/salaries/players/')

        assert driver.title == "NBA Player Salaries | HoopsHype"
        driver.quit()

    def test_csv_format(self):
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

        player_salaries = dict(zip(players_list, salaries_list))
        player_salaries_df = pd.DataFrame(player_salaries.items())

        header = player_salaries_df.iloc[0]
        player_salaries_df = player_salaries_df[1:]
        player_salaries_df.columns = header

        assert list(player_salaries_df.columns.values) == ['PLAYER', '2024/25']
        driver.quit()
