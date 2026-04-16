from typing import Union

from api.ApiRequest import ApiRequest

class FormulaEngineService(ApiRequest):
    '''Класс взаимодействия с сервисом formula-engine'''
    def __init__(self, protocol: str, address: str, cert: Union[str, bool], bearer: str):
        '''Инициализация экземпляра общих свойств соединения с сервисом formula-engine'''
        self.__protocol = protocol
        self.__address = address
        self.__cert = cert
        self.__headers = {'Authorization': f'{bearer}'}

    def getDatasets(self, wsId:str, dsId:str='') -> Union[list, dict]:
        '''Метод получения списка наборов данных рабочей области или метаданных определенного набора'''
        if dsId:
            self.__endpoint = f'formula-engine/api/v1/workspaces/{wsId}/datasets/{dsId}/model'
        else:
            self.__endpoint = f'formula-engine/api/v1/workspaces/{wsId}/datasets'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response
    
    def createDataset(self, wsId:str, dsId:str, dsData:dict):
        '''Метод создания пустого набора данных.\n
        Идентификатор dsId - валидный uuid\n
        Формат сведений dsData - {'name': 'xxx', 'description': 'yyy', 'storageMode': 'Import}'''
        self.__endpoint = f'formula-engine/api/v1/workspaces/{wsId}/datasets/{dsId}/model'
        headers = self.__headers
        headers['Content-Type'] = 'application/json'
        super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=headers, json=dsData)
        self.__response = super().sendRequest()
        return self.__response
    
    def getDatasetPermissions(self, wsId:str, dsId:str):
        '''Метод получения сведений о доступах пользователей к набору данных'''
        self.__endpoint = f'formula-engine/api/v1/workspaces/{wsId}/datasets/{dsId}/permission-mappings'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response
    
    def getDatasetRelationships(self, wsId:str, dsId:str):
        '''Метод получения сведений о связях в наборе данных'''
        self.__endpoint = f'formula-engine/api/v1/workspaces/{wsId}/datasets/{dsId}/relationships'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response

    def importDatasetRelationship(self, wsId:str, dsId:str, rId:str, relData:dict, version:int):
        '''Метод импорта связей таблиц в модели данных'''
        self.__endpoint = f'formula-engine/api/v1/workspaces/{wsId}/datasets/{dsId}/relationships/{rId}'
        headers = self.__headers
        headers['If-Match'] = str(version)
        headers['Content-Type'] = 'application/json'
        super().__init__('put', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=headers, json=relData)
        self.__response = super().sendRequest()
        return self.__response
    
    def getDatasetMeasures(self, wsId:str, dsId:str, tId:str):
        '''Метод получения мер из таблицы набора данных'''
        self.__endpoint = f'formula-engine/api/v1/workspaces/{wsId}/datasets/{dsId}/tables/{tId}/measures'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response
    
    def importDatasetMeasure(self, wsId:str, dsId:str, tId:str, mId:str, measureData:dict, version:int):
        '''Метод импорта мер в набор данных.\n
        version - версия метаданных набора'''
        self.__endpoint = f'formula-engine/api/v1/workspaces/{wsId}/datasets/{dsId}/tables/{tId}/measures/{mId}'
        headers = self.__headers
        headers['If-Match'] = str(version)
        headers['Content-Type'] = 'application/json'
        super().__init__('put', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=headers, json=measureData)
        self.__response = super().sendRequest()
        return self.__response
    
    def getDatasetRoleMemberships(self, wsId:str, dsId:str, rId:str):
        '''Метод получения пользователей назначеных в роли RLS/OLS\n
        Идентификаторы ролей rId берутся из метаданных набора, свойство roles'''
        self.__endpoint = f'formula-engine/api/v1/workspaces/{wsId}/datasets/{dsId}/roles/{rId}/memberships'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response

    def tableDataQuery(self, wsId:str, dsId:str, table:str, quantity:int=1000):
        '''Метод DAX запроса данных таблицы набора данных по ее имени\n
        Название таблицы - как в наборе\n
        По умолчанию выбирается 1я тысяча записей (параметр quantity)'''
        self.__endpoint = f'formula-engine/api/v1/workspaces/{wsId}/datasets/{dsId}/model/query'
        payload = {
            "expression": f"EVALUATE {{COUNTROWS('{table}')}} EVALUATE TOPNSKIP({quantity},0,'{table}')",
            "format": "JsonCompact"
        }
        super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers, json=payload)
        self.__response = super().sendRequest()
        return self.__response