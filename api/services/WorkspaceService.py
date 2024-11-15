from typing import Union

from api.ApiRequest import ApiRequest

class WorkspaceService(ApiRequest):
    '''Класс взаимодействия с рабочими областями'''
    def __init__(self, protocol: str, address: str, cert: Union[str, bool], bearer: str):
        '''Инициализация объекта со списком рабочих областей'''
        self.__protocol = protocol
        self.__address = address
        self.__cert = cert
        self.__headers = {'Authorization': f'{bearer}'}

    def getList(self):
        '''Метод получения списка рабочих областей'''
        self.__endpoint = 'workspace-service/api/v1/workspaces'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest().json()
        return self.__response

    def getLicenseInfo(self):
        self.__endpoint = f'workspace-service/api/v1/license'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response.json()