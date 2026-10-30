from typing import Union

from api.ApiRequest import ApiRequest

class WorkspaceService(ApiRequest):
    '''Класс взаимодействия с рабочими областями'''
    def __init__(self, protocol: str, address: str, cert: Union[str, bool], bearer: str):
        '''Инициализация объекта компонента работы с рабочими областями'''
        self.__protocol = protocol
        self.__address = address
        self.__cert = cert
        self.__headers = {'Authorization': f'{bearer}'}
    
    def getIdentifiers(self) -> list:
        '''Метод получения списка идентификаторов рабочих областей'''
        self.__endpoint = 'workspace-service/api/v1/workspaces/identifiers'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response

    def getWorkspaces(self, wsId:str='') -> Union[list, dict]:
        '''Метод получения списка рабочих областей или сведений о рабочей области'''
        if wsId:
            self.__endpoint = f'workspace-service/api/v1/workspaces/{wsId}'
        else:
            self.__endpoint = 'workspace-service/api/v1/workspaces'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response

    def getLicenseInfo(self) -> dict:
        '''Метод получени сведений о лицензии'''
        self.__endpoint = f'workspace-service/api/v1/license'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response
    
    def getUsers(self) -> list:
        '''Метод получения списка пользователей с данными об активности.'''
        self.__endpoint = 'workspace-service/api/v1/access/users'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response
    
    def getGroups(self, take:int=10) -> list:
        '''Метод получения списка групп.\nПараметр take задает максимальное количество выборки. По умолчанию - 10'''
        self.__endpoint = f'workspace-service/api/v1/groups?take={take}'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response
    
    def getGroupUsers(self, gIds:list) -> list:
        '''Метод получения пользователей групп'''
        self.__endpoint = 'workspace-service/api/v1/groups/query-by-ids/users'
        if gIds:
            super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers, json=gIds)
            self.__response = super().sendRequest()
            return self.__response
        else:
            raise Exception('Отсутствует список идентификаторов групп для которых запрашиваются пользователи.')
    
    def getRoleMappings(self, wsId:str) -> list:
        '''Метод получения сведений о пользовательских ролях'''
        if wsId:
            self.__endpoint = f'workspace-service/api/v1/workspaces/{wsId}/role-mappings'
            super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
            self.__response = super().sendRequest()
            return self.__response
        else:
            raise Exception('Отсутствует идентификатор рабочей области.')
    
    def createWorkspace(self, wsData:dict) -> dict:
        '''Метод создания рабочей области'''
        if wsData and 'name' in wsData and wsData['name'] not in list(map(lambda x: x['name'], self.getList())):
            self.__endpoint = 'workspace-service/api/v1/workspaces'
            super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers, json=wsData)
            self.__response = super().sendRequest()
            return self.__response
        elif wsData and 'name' in wsData and wsData['name'] in list(map(lambda x: x['name'], self.getList())):
            raise Exception(f'Рабочая область с именем \"{wsData["name"]}\" уже существует.')
        else:
            raise Exception('Отсутствуют данные о создаваемой рабочей области, либо они не верны.')
