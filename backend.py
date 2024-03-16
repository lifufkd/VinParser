from freeGPT import Client
import requests
import json
import random
import time
import selenium_dolphin as dolphin
from selenium_dolphin import DolphinAPI, STABLE_CHROME_VERSION
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

class ChatGpt:
    def __init__(self):
        super(ChatGpt, self).__init__()

    def gpt_query(self, query):
        try:
            answer = Client.create_completion("gpt3", f'determine the price of a used car {query} In the USA. In the response, specify the Traid In and Private Price in json format without any another information')
            print(answer)
        except:
            pass
        return answer


class CarDetermineByVin:
    def __init__(self, chat_gpt):
        super(CarDetermineByVin, self).__init__()
        self.__chat_gpt = chat_gpt
        self.__counter = 0

    def unparse_json(self, data):
        return json.loads(data)

    def check_vin(self, vin, clean):
        output = [0, 0]
        if clean:
            self.__counter = 0
        url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{vin}?format=json"
        response = requests.get(url)
        data = json.loads(response.text)
        for i in range(3):
            try:
                self.__counter += 1
                c = 0
                raw_data = self.__chat_gpt.gpt_query(f'Make: {data["Results"][0]["Make"]}, Model: {data["Results"][0]["Model"]}, Year: {data["Results"][0]["ModelYear"]}')
                answer = self.unparse_json(raw_data)
                print(answer)
                for g in answer.keys():
                    if g[:7].lower() == 'private':
                        private = str()
                        for k in answer[g]:
                            if k not in ['$', ',', ' ']:
                                private += k

                        output[1] = int(random.uniform(int(private)-2000, int(private)-1500))
                        c += 1
                    elif g[:5].lower() == 'trade':
                        trade = str()
                        for k in answer[g]:
                            if k not in ['$', ',', ' ']:
                                trade += k
                        output[0] = int(random.uniform(int(trade)-2000, int(trade)-1500))
                        c += 1
                if c == 2:
                    break
            except:
                pass
        return output, self.__counter


class Parser:
    def __init__(self, config):
        super(Parser, self).__init__()
        self.__config = config
        self.__driver = None
        self.__profile_id = None
        self.__api = None

    def parser_init(self):
        self.__api = DolphinAPI(api_key=self.__config.get_config()['dolphin_api'])
        response = self.__api.get_profiles()
        if response['data']:
            self.__profile_id = response['data'][-1]['id']
            if self.__profile_id:
                self.__api.delete_profiles([self.__profile_id])
        fingerprint = []
        while not fingerprint:
            fingerprint = self.__api.generate_fingerprint(platform='windows',
                                                       browser_version=f'{random.randint(114, STABLE_CHROME_VERSION)}')
        data = self.__api.fingerprint_to_profile(name='my superprofile', fingerprint=fingerprint)
        profile_id = self.__api.create_profile(data)['browserProfileId']
        response = dolphin.run_profile(profile_id)
        port = response['automation']['port']
        options = Options()
        ###############################################
        options.add_argument("--start-maximized")
        ###############################################
        self.__driver = dolphin.get_driver(options=options, port=port)

    def get_data(self, vin, odometer, private=None, trade_in=None):
        while private is None or trade_in is None:
            self.parser_init()
            self.__driver.get(self.__config.get_config()['url'])
            self.__driver.find_element(By.ID, 'zip').send_keys(self.__config.get_config()['zip_code'])
            self.__driver.find_element(By.ID, 'vin').send_keys(vin)
            print('Жду нажатия кнопки 5 секунд')
            time.sleep(5)
            private, trade_in = self.second_task(odometer)
        return private, trade_in

    def second_task(self, odometer, private=None, trade_in=None):
        try:
            time.sleep(random.uniform(2, 3))
            odometer_element = self.__driver.find_element(By.ID, 'odometer')
            odometer_element.clear()
            odometer_element.send_keys(odometer)
            time.sleep(random.uniform(4, 5))
            new_data = self.__driver.find_element(By.CLASS_NAME, 'pricesStyle_results__prices__list__pv_hm').text.split('\n')
            private = new_data[3]
            trade_in = new_data[6]
        finally:
            self.__driver.quit()
            dolphin.close_profile(self.__profile_id)
            self.__api.delete_profiles([self.__profile_id])
            return private, trade_in

