import requests

from typing import Union

class ApiRequest:
    '''Класс для отправки запросов к API Visiology3'''
    def __init__(self, method: str, protocol: str, address: str, cert: Union[str, bool], endpoint='', headers:dict={}, data:dict={}, jsondata:dict={}, files='') -> None:
        '''Инициализация данных объекта запроса'''
        self.__method = method
        #self.__platform = f'{protocol}://{address}/v3/'
        self.__url = f'{protocol}://{address}/v3/{endpoint}'
        if self.__method == 'http':
            self.__cert = False
        elif cert: 
            self.__cert = cert
        else:
            self.__cert = True
        #self.__endpoint = endpoint
        self.__headers = headers
        self.__data = data
        self.__jsondata = jsondata
        self.__files = files
    
    def sendRequest(self):
        '''Метод отправки запроса к API'''
        if self.__method == 'get':
            #url = self.__platform + self.__endpoint
            self.__response = requests.get(self.__url, headers=self.__headers, verify=self.__cert)
        elif self.__method == 'post':
            #url = self.__platform + self.__endpoint
            if self.__data:
                self.__response = requests.post(self.__url, headers=self.__headers, verify=self.__cert, data=self.__data)
            elif self.__jsondata:
                self.__response = requests.post(self.__url, headers=self.__headers, verify=self.__cert, json=self.__jsondata)
            elif self.__files:
                self.__response = requests.post(self.__url, headers=self.__headers, verify=self.__cert, files=self.__files)
            else:
                self.__response = requests.post(self.__url, headers=self.__headers, verify=self.__cert, json={})
        elif self.__method == 'put':
            #url = self.__platform + self.__endpoint
            if self.__data:
                self.__response = requests.put(self.__url, headers=self.__headers, verify=self.__cert, data=self.__data)
            if self.__jsondata:
                self.__response = requests.put(self.__url, headers=self.__headers, verify=self.__cert, json=self.__jsondata)
            if self.__files:
                self.__response = requests.put(self.__url, headers=self.__headers, verify=self.__cert, files=self.__files)
        else:
            raise Exception('Неизвестный метод запроса к API.')
            #print('Unknown request method!')
            #self.__response = {"ok": False, "status_code": 400, "content": "Unknown request method!"}
        
        return self.__response
        #if self.__response.ok:
        #    return self.__response
        #else:
        #    return self.__response