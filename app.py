import re

import lxml  # noqa
from bs4 import BeautifulSoup
from flask import Flask

from player import Player
from webdriver import driver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

app = Flask(__name__)

# set browser to use this page
STATISTICS_URL = 'https://fantasy.premierleague.com/statistics'
driver.get(STATISTICS_URL)
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, 'sc-AykKC sc-AykKD iKIfJP'))
    )

except TimeoutException:
    print('Loading took too much time!')

pagination = driver.find_element_by_xpath(
    "//div[@class='sc-AykKC sc-AykKD iKIfJP']")

next_page_btn = pagination.find_elements_by_tag_name('button')[2]

# get 2 last chars which will be actually a number from 1 to 99
page_count = int(pagination.find_elements_by_tag_name(
    'div')[0].get_attribute('innerHTML')[-2:])

# copy from chrome process to your python instance
html = driver.page_source

all_players = []

# with open('output.html', 'w') as output:
# output.write(driver.page_source)


def get_all_players(html: str, page: int):
    soup = BeautifulSoup(html, 'lxml')
    tbody = soup.find('tbody')
    table_rows = tbody.findAll('tr')

    for row in table_rows:
        table_data = row.findAll('td')

        player_name = ''
        player_team = ''
        player_position = ''
        player_cost = ''
        player_selected_by = ''
        player_form = ''
        player_total_points = ''

        for index, data in enumerate(table_data):
            if (index == 0):
                continue

            if (index == 1):
                player_media = data.find(
                    'div', class_=re.compile('^Media__Body'))

                player_name = player_media.find(
                    'div', class_=re.compile('^ElementInTable__Name')).contents[0]

                player_info = player_media.findAll('span')
                player_team, player_position = player_info[0].contents[0], player_info[1].contents[0]

            if (index == 2):
                player_cost = data.contents[0]

            if (index == 3):
                player_selected_by = data.contents[0]

            if (index == 4):
                player_form = data.contents[0]

            if (index == 5):
                player_total_points = data.contents[0]

        player = Player(player_name, player_team, player_position, player_cost,
                        player_selected_by, player_form, player_total_points)
        all_players.append(player)

    if (page < page_count):
        next_page_btn.click()
        html = driver.page_source
        page += 1
        get_all_players(html, page)


get_all_players(html, page=1)
print(len(all_players))

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5050)
