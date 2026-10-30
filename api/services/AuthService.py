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
            'scope':'openid data_management_service formula_engine workspace_service dashboard_service edge_service forms_service groups profile email',
            'username': user,
            'password': password
        }
        
        super().__init__('post', protocol, address, cert, self.__endpoint, self.__headers, data=self.__data)
        self.__timeRecieved = time.time()
        self.__response = super().sendRequest()
    
    def getBearerString(self):
        '''Метод получения строки с токеном авторизации'''
        if type(self.__response) is dict and 'access_token' in self.__response:
            return f'Bearer {self.__response["access_token"]}'
        else:
            print(self.__response)
            raise Exception('В ответе сервера отсутствует токен авторизации.')
        
    def isExpired(self) -> bool:
        '''Метод проверки срока действия токена'''
        if 'expires_in' in self.__response:
            self.__expire_time = self.__timeRecieved + self.__response['expires_in']
            if self.__expire_time <= time.time():
                return True
            else:
                return False
        elif 'expires_at' in self.__response:
            if time.time() >= self.__response['expires_at']:
                return True
            else:
                return False
        else:
            raise Exception('В ответе сервера авторизации отсутствуют данные о сроке действия токена.')