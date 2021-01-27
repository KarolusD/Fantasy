import lxml  # noqa

from flask import Flask

from webdriver import driver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from helpers import get_all_players, write_players_to_xlsx

app = Flask(__name__)


def main():
    try:
        # set browser to use this page
        STATISTICS_URL = 'https://fantasy.premierleague.com/statistics'
        driver.get(STATISTICS_URL)

        pagination = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.sc-AykKC.sc-AykKD.iKIfJP'))
        )

        next_page_btn = pagination.find_elements_by_tag_name('button')[2]

        # get 2 last chars which will be actually a number from 1 to 99
        page_count = int(pagination.find_elements_by_tag_name(
            'div')[0].get_attribute('innerHTML')[-2:])

        # copy from chrome process to your python instance
        html = driver.page_source

        all_players = get_all_players(html, next_page_btn, page_count, page=1)
        write_players_to_xlsx(all_players)

    except TimeoutException as TE:
        print(f'Loading took too much time! {TE}')

    finally:
        driver.quit()


main()

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5050)
