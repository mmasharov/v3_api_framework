from typing import Union

from api.ApiRequest import ApiRequest

class FormulaEngineService(ApiRequest):
    '''Класс взаимодействия с сервисом formula-engine'''
    def __init__(self, protocol: str, address: str, cert: Union[str, bool], bearer: str, wsId: str):
        '''Инициализация экземпляра общих свойств соединения с сервисом formula-engine'''
        self.__entities = ['datasets', 'relationships', 'measures']
        self.__protocol = protocol
        self.__address = address
        self.__cert = cert
        self.__headers = {'Authorization': f'{bearer}'}
        self.__wsId = wsId

    def getFEEntity(self, entity: str, objectId: str='list') -> Union[list, dict]:
        '''Метод получения сущности сервиса FE\n
        Поддерживаемые сущности: "datasets"'''
        if entity not in self.__entities:
            raise Exception('Unknown entity!')
        
        if entity == 'datasets' and objectId == 'list':
            self.__endpoint = f'formula-engine/api/v1/workspaces/{self.__wsId}/{entity}'
        elif entity == 'datasets' and objectId != 'list':
            self.__endpoint = f'formula-engine/api/v1/workspaces/{self.__wsId}/{entity}/{objectId}/model'
        elif entity == 'relationships':
            self.__endpoint = f'formula-engine/api/v1/workspaces/{self.__wsId}/datasets/{objectId}/relationships'

        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest().json()

        if objectId == 'list':
            return list(map((lambda ob: [ob['id'], ob['name']]), self.__response))
        else:
            return self.__response
        
    def importFEEntity(self, dsId:str, dsName:str):
        self.__endpoint = f'formula-engine/api/v1/workspaces/{self.__wsId}/datasets/{dsId}/model'
        super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers, jsondata={'name': dsName})
        self.__response = super().sendRequest()
        print(self.__response.status_code, self.__response.text)

    def importRelationship(self, dsId:str, rId:str, data:dict, version:int):
        '''Метод импорта связей таблиц в модели данных'''
        self.__endpoint = f'formula-engine/api/v1/workspaces/{self.__wsId}/datasets/{dsId}/relationships/{rId}'
        headers = self.__headers
        headers['If-Match'] = str(version)
        headers['Content-Type'] = 'application/json'
        super().__init__('put', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=headers, jsondata=data)
        self.__response = super().sendRequest()
        return self.__response.content.decode('utf-8')
    
    def importMeasure(self, dsId:str, tId:str, mId:str, data:dict, version:int):
        '''Метод импорта мер в набор данных'''
        self.__endpoint = f'formula-engine/api/v1/workspaces/{self.__wsId}/datasets/{dsId}/tables/{tId}/measures/{mId}'
        headers = self.__headers
        headers['If-Match'] = str(version)
        headers['Content-Type'] = 'application/json'
        super().__init__('put', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=headers, jsondata=data)
        self.__response = super().sendRequest()
        return self.__response.content.decode('utf-8')
    
    def getMeasures(self, dsId:str, tId:str):
        '''Метод получения мер привязанных к таблице набора данных'''
        self.__endpoint = f'formula-engine/api/v1/workspaces/{self.__wsId}/datasets/{dsId}/tables/{tId}/measures'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response.content.decode('utf-8')
    
    def getDatasetPermissions(self, dsId:str):
        '''Метод получения сведений о доступах пользователей к набору данных'''
        self.__endpoint = f'formula-engine/api/v1/workspaces/{self.__wsId}/datasets/{dsId}/permission-mappings'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response.json()