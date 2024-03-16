from freeGPT import Client
import requests
import json
import random

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
