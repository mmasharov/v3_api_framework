from typing import Union

from api.ApiRequest import ApiRequest

class Platform(ApiRequest):
    def __init__(self, protocol:str, address:str, cert:Union[str, bool], bearer:str):
        self.__protocol = protocol
        self.__address = address
        self.__cert = cert
        self.__headers = {'Authorization': f'{bearer}'}
    
    def versionInfo(self):
        self.__endpoint = 'version'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest().json()
        for item in self.__response:
            self.__response[item] = self.__response[item]['VERSION']
        return self.__response