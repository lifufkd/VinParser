#####################################
#            Created by             #
#                SBR                #
#####################################
import time
from tqdm import tqdm
import simpleaudio as sa
import pandas as pd
import threading
import sys
import keyboard
import logging
from datetime import datetime
from config_parser import ConfigParser
from backseat import CarDetermineByVin, ChatGpt
####################################################################
config_name = 'config.json'
####################################################################


def read_xlsx(name, column):
    df = pd.read_excel(name)
    return df[column].tolist()


def convert_to_xlsx(filename):
    df = pd.read_excel(filename)
    df.to_excel(filename + 'x')
    return filename + 'x'


def write_xlsx(data):
    new_file = convert_to_xlsx(args.get_config()['excell_name'])
    df = pd.read_excel(args.get_config()['excell_name'])
    new_df = pd.DataFrame(data)
    df.update(new_df)
    df.to_excel(new_file, index=False)


def key_writer():
    global key_realise
    key_realise = True


def keyboardr():
    keyboard.add_hotkey('enter', lambda: key_writer())


def get_prices(vin_numbers, sound):
    global key_realise
    flag = False
    output = {args.get_config()['Private_Price_Column']: [], args.get_config()['Traid_In_Column']: []}
    for vin in tqdm(vin_numbers):
        data, counter = car_detect.check_vin(vin, flag)
        if counter >= 60:
            logging.info(f'Остановка на 300s для избежания блокировки!!! (Вы можете продолжить включив VPN и нажав ENTER) {datetime.now()}')
            flag = True
            threading.Thread(target=keyboardr).start()
            for i in range(300):
                if key_realise:
                    key_realise = False
                    break
                time.sleep(1)
        elif flag:
            flag = False
        output[args.get_config()['Traid_In_Column']].append(data[0])
        output[args.get_config()['Private_Price_Column']].append(data[1])
        write_xlsx(output)
    play_alarm(sound)


def play_alarm(sound):
    logging.info(f'Обновление документа завершено!!! {datetime.now()}')
    wave_obj = sa.WaveObject.from_wave_file(sound)
    play_obj = wave_obj.play()
    play_obj.wait_done()


if '__main__' == __name__:
    key_realise = False
    logging.basicConfig(handlers=[logging.FileHandler("log.txt"), logging.StreamHandler(sys.stdout)],
                        level=logging.INFO)
    args = ConfigParser(config_name)
    chat_gpt = ChatGpt()
    car_detect = CarDetermineByVin(chat_gpt)
    get_prices(read_xlsx(args.get_config()['excell_name'], args.get_config()['VIN_Column']), args.get_config()['sound_file_name'])
