from typing import Union

from api.ApiRequest import ApiRequest

class SmartForms(ApiRequest):
    '''Класс для работы с модулем SmartForms'''
    def __init__(self, protocol:str, address:str, cert:Union[str, bool], bearer:str):
        '''Инициализация экземпляра подключения к API модуля SmartForms'''
        self.__protocol = protocol
        self.__address = address
        self.__cert = cert
        self.__headers = {'Authorization': f'{bearer}'}
    
    def getDimensions(self):
        '''Метод получения списка измерений'''
        self.__endpoint = 'smart-forms/api/dimensions'
        headers = self.__headers
        headers['x-api-version'] = '2.0'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=headers)
        self.__response = super().sendRequest().json()
        return self.__response