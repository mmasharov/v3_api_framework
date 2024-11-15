import time

from typing import Union

from api.ApiRequest import ApiRequest

class AuthService(ApiRequest):
    '''Класс для работы с авторизацией в API платформы'''
    def __init__(self, protocol: str, address: str, cert: Union[str, bool], user: str, password: str) -> None:
        '''Инициализация объекта запроса к сервису авторизации.'''
        self.__endpoint = 'keycloak/realms/Visiology/protocol/openid-connect/token'
        self.__headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.__data = {
            'client_id':'visiology_designer',
            'grant_type':'password',
            'scope':'openid data_management_service formula_engine workspace_service dashboard_service',
            'username': user,
            'password': password
        }
        
        super().__init__('post', protocol, address, cert, self.__endpoint, self.__headers, self.__data)
        self.__timeRecieved = time.time()
        self.__response = super().sendRequest().json()
    
    def getBearerString(self):
        '''Метод получения строки с токеном авторизации'''
        if type(self.__response) is dict:
            return f'Bearer {self.__response["access_token"]}'
        else:
            return self.__response
        
    def isExpired(self) -> bool:
        '''Метод проверки срока действия токена'''
        self.__expire_time = self.__timeRecieved + self.__response['expires_in']
        if self.__expire_time <= time.time():
            return True
        else:
            return False