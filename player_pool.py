
from probabilities import expValue
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver.v2 as uc

from time import sleep
import pandas as pd
import re
from utils import get_free_proxies
import random
import pickle


class Player:
    def __init__(self, id, name, type, rating, price):
        self.id = id
        self.name = name
        self.type = type
        self.rating = int(rating)

        if "M" in price:
            self.price = float(re.sub(r'M', "", price)) * 1000000
        elif "K" in price:
            self.price = float(re.sub(r'K', "", price)) * 1000

        self.price = float(price)

    def viewPlayer(self):
        print(self.id, self.name, self.type, self.rating, self.price)


class PlayerList:
    def __init__(self):
        self.all = {}

    def addPlayer(self, player):
        """
        Adds new players and replaces old ones.
        This means we need to add special cards in packs after we add regular ones
        """
        self.all[player.name] = player


def parse(url, player_list):

    # maybe move this to to run once per session
    # proxies = get_free_proxies()
    """
    # rotate proxy
    PROXY = random.choice(proxies)

    """

    PROXY = "145.239.169.47"
    options = webdriver.ChromeOptions()
    options.add_argument('proxy-server={}'.format(PROXY))

    # prevent session crash
    options.add_argument('--no-sandbox')

    browser = uc.Chrome(options=options)

    # create selenium driver
    # options = Options()
    # options.binary_location = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
    # browser = webdriver.Chrome(chrome_options=options,
    #                           executable_path=r'C:/Users/riley/chromedriver_win32/chromedriver.exe')

    # iterate through pages of results
    page = 1
    page_exists = True
    while page_exists:
        page_exists = False
        url = re.sub(r'page=\d+', "page=" + str(page), url)

        browser.get(url)
        sleep(3)

        # find player_table
        player_table = browser.find_element_by_xpath(
            "/html/body/div[8]/div[2]/div[5]/div[4]/table/tbody")

        # iterate through rows of the table
        for row in player_table.find_elements_by_css_selector("tr"):
            page_exists = True

            # get information from each player in table
            items = []
            for cell in row.find_elements_by_tag_name('td'):
                items.append(cell.text)

            if len(items) < 5:
                page_exists = False
                break

            # add player object to the player list
            player_list.addPlayer(
                Player(id=0, name=items[0], type=items[3], price=items[4], rating=items[1]))

        page += 1

    browser.quit()
    return


"""
if __name__ == "__main__":

    gold_player_list = PlayerList()
    url = "https://www.futbin.com/22/players?page=1&version=gold_rare&player_rating=91-99&"
    parse(url, gold_player_list)

    with open("bin.dat", "wb") as f:
        pickle.dump(gold_player_list, f, pickle.HIGHEST_PROTOCOL)
"""

with open('bin.dat', 'rb') as f:
    players = pickle.load(f)
