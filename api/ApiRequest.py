import requests

from typing import Union

class ApiRequest:
    '''Класс для отправки запросов к API Visiology3'''
    def __init__(self, method: str, protocol: str, address: str, cert: Union[str, bool], endpoint='', headers:dict={}, data: Union[dict, str]={}) -> None:
        '''Инициализация данных объекта запроса'''
        if method in ['get', 'post', 'put']:
            self.__method = method
        else:
            raise Exception('Неизвестный метод запроса к API: {method}')
        if protocol in ['http', 'https']:
            self.__url = f'{protocol}://{address}/{endpoint}'
            if protocol == 'http':
                self.__cert = False
            elif protocol == 'https' and (type(cert) is str or type(cert) is bool):
                self.__cert = cert
            else: self.__cert = False
        else:
            raise Exception(f'Не поддерживаемый протокол запроса: {protocol}')
        self.__headers = headers
        if type(data) is dict:
            self.__data = data
        else:
            raise Exception('Неизвестный тип тела запроса.')
    
    def sendRequest(self):
        '''Метод отправки запроса к API'''
        if self.__method == 'get':
            self.__response = requests.get(self.__url, headers=self.__headers, verify=self.__cert)
        elif self.__method == 'post':
            if self.__data:
                self.__response = requests.post(self.__url, headers=self.__headers, verify=self.__cert, data=self.__data)
            else:
                self.__response = requests.post(self.__url, headers=self.__headers, verify=self.__cert, data={})
        elif self.__method == 'put':
            if self.__data:
                self.__response = requests.put(self.__url, headers=self.__headers, verify=self.__cert, data=self.__data)
        if self.__response.status_code == 200:
            return self.__response.json()
        else:
            return {"ApiRequestError": f'Статус запроса: {self.__response.status_code}'}