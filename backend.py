import random
import time
import undetected_chromedriver as UC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class Parser:
    def __init__(self, config):
        super(Parser, self).__init__()
        self.__config = config
        self.__driver = None
        self.__profile_id = None
        self.__api = None

    def parser_init(self):
        options = UC.ChromeOptions()
        ###############################################
        options.add_argument("--start-maximized")
        ###############################################
        self.__driver = UC.Chrome(options=options)

    def authorization(self, vin):
        self.__driver.get(self.__config.get_config()['url'] + vin)
        self.__driver.find_element(By.ID, 'username').send_keys(self.__config.get_config()['login'])
        time.sleep(1)
        self.__driver.find_element(By.ID, 'password').send_keys(self.__config.get_config()['password'])
        time.sleep(1)
        self.__driver.find_element(By.XPATH, "/html/body/main/section/div/div/div/form/div[2]/button").click()
        time.sleep(5)

    def second_task(self):
        return self.__driver.find_element(By.CSS_SELECTOR, 'carfax-value-row.carfax-price-text').text.split('\n')[0]

