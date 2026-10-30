import requests

from typing import Union

class ApiRequest:
    '''Класс для отправки запросов к API Visiology3'''
    def __init__(self, method: str, protocol: str, address: str, cert: Union[str, bool], endpoint='', headers:dict={}, data: Union[dict, list, str]={}, json: Union[dict, list]={}, files: Union[dict, list]={}, params:dict={}) -> None:
        '''Инициализация данных объекта запроса'''
        if method in ['get', 'post', 'put']:
            self.__method = method
        else:
            raise Exception('Неизвестный метод запроса к API: {method}')
        if protocol in ['http', 'https']:
            if address[-1] == '/':
                address = address[:-1]
            self.__url = f'{protocol}://{address}/{endpoint}'
            if protocol == 'http':
                self.__cert = False
            elif protocol == 'https' and (type(cert) is str or type(cert) is bool):
                self.__cert = cert
            else: self.__cert = False
        else:
            raise Exception(f'Не поддерживаемый протокол запроса: {protocol}')
        self.__headers = headers
        self.__data = data
        self.__json = json
        self.__files = files
        self.__params = params
    
    def sendRequest(self):
        '''Метод отправки запроса к API'''
        if self.__method == 'get' and self.__params:
            self.__response = requests.get(self.__url, headers=self.__headers, verify=self.__cert, params=self.__params)
        elif self.__method == 'get' and not self.__params:
            self.__response = requests.get(self.__url, headers=self.__headers, verify=self.__cert)
        elif self.__method == 'post' and self.__data:
            self.__response = requests.post(self.__url, headers=self.__headers, verify=self.__cert, data=self.__data)
        elif self.__method == 'post' and self.__json:
            self.__response = requests.post(self.__url, headers=self.__headers, verify=self.__cert, json=self.__json)
        elif self.__method == 'post' and self.__json == {}:
            self.__response = requests.post(self.__url, headers=self.__headers, verify=self.__cert, json={})
        elif self.__method == 'post' and self.__files:
            self.__response = requests.post(self.__url, headers=self.__headers, verify=self.__cert, files=self.__files)
        elif self.__method == 'put' and self.__json:
            self.__response = requests.put(self.__url, headers=self.__headers, verify=self.__cert, json=self.__json)
        else:
            raise Exception('Неизвестный тип запроса или неверные входные данные.')
        
        if self.__response.status_code == 200:
            if self.__response.headers['Content-Type'] == 'application/json' or self.__response.headers['Content-Type'] == 'application/json; charset=utf-8':
                return self.__response.json()
            elif self.__response.headers['Content-Type'] == 'text/plain; charset=utf-8':
                return self.__response.content.decode('utf-8')
        elif self.__response.status_code == 204:
            return {"Status": "Success. Code 204."}
        else:
            return {"ApiRequestError": f'Статус запроса: {self.__response.status_code}', "info": f'{self.__response.reason}'}