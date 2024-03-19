#####################################
#            Created by             #
#                SBR                #
#####################################
from tqdm import tqdm
import simpleaudio as sa
import pandas as pd
import sys
import logging
from datetime import datetime
from config_parser import ConfigParser
from backend import Parser
####################################################################
config_name = 'config.json'
####################################################################


def read_vin(name, column):
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


def get_prices():
    output = {args.get_config()['Private_Price_Column']: []}
    vin_numbers = read_vin(args.get_config()['excell_name'], args.get_config()['VIN_Column'])
    parser.parser_init()
    for vin in tqdm(vin_numbers):
        parser.authorization(vin)
        private = parser.second_task()
        output[args.get_config()['Private_Price_Column']].append(private)
        write_xlsx(output)
    play_alarm(args.get_config()['sound_file_name'])


def play_alarm(sound):
    logging.info(f'Обновление документа завершено!!! {datetime.now()}')
    wave_obj = sa.WaveObject.from_wave_file(sound)
    play_obj = wave_obj.play()
    play_obj.wait_done()


if '__main__' == __name__:
    logging.basicConfig(handlers=[logging.FileHandler("log.txt"), logging.StreamHandler(sys.stdout)],
                        level=logging.INFO)
    args = ConfigParser(config_name)
    parser = Parser(args)
    get_prices()
