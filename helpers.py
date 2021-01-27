import re

import xlsxwriter
from bs4 import BeautifulSoup

from player import Player
from webdriver import driver


def get_all_players(html: str, next_page_btn: object, page_count: int, page: int):
    all_players = []
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
        get_all_players(html, next_page_btn, page_count, page)

    return all_players


def write_players_to_xlsx(all_players: list):
    workbook = xlsxwriter.Workbook('Fantasy_all_players.xlsx')
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': 1})
    worksheet.write('A1', 'Name', bold)
    worksheet.write('B1', 'Team', bold)
    worksheet.write('C1', 'Position', bold)
    worksheet.write('D1', 'Cost', bold)
    worksheet.write('E1', 'Selected by', bold)
    worksheet.write('F1', 'Form', bold)
    worksheet.write('G1', 'Total points', bold)

    row = 1
    col = 0

    for player_index, player in enumerate(all_players):
        values = list(player.__dict__.values())
        for value_index, value in enumerate(values):
            worksheet.write(row + player_index, col + value_index, value)

    print('Workbook created!')
    workbook.close()
