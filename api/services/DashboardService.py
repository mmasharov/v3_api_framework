from typing import Union

from api.ApiRequest import ApiRequest

class DashboardService(ApiRequest):
    '''Класс взаимодействия с дашбордами'''
    def __init__(self, protocol: str, address: str, cert: Union[str, bool], bearer: str, wsId: str):
        '''Инициализация экземпляра общих параметров для соединения с dashboard-service.\n
        Сущности: "dashboards", "user-widgets", "themes"'''
        self.__entities = ['dashboards', 'themes', 'user-widgets', 'dbmeasures']
        self.__protocol = protocol
        self.__address = address
        self.__cert = cert
        self.__headers = {'Authorization': f'{bearer}'}
        self.__wsId = wsId

    def getDSEntity(self, entity: str, objectId: str='list') -> Union[list, dict]:
        '''Метод получения объектов от сервиса дашбордов.\n
        Отдает либо список ид-имя для сущности, если не указан идентефикатор конкретной сущности,\n
        либо отдельный объект сущности если вторым аргументом указана идентификатор'''

        if entity not in self.__entities:
            raise Exception('Unknown entity!')

        if entity == 'user-widgets' and objectId == 'list':
            self.__endpoint = f'dashboard-service/api/user-widgets'
        elif entity == 'user-widgets' and objectId != 'list':
            self.__endpoint = f'dashboard-service/api/user-widgets/{objectId}'
        elif entity != 'user-widgets' and objectId == 'list':
            self.__endpoint = f'dashboard-service/api/workspaces/{self.__wsId}/{entity}'
        elif entity == 'themes' and objectId != 'list':
            self.__endpoint = f'dashboard-service/api/workspaces/{self.__wsId}/themes/{objectId}/export'
        elif entity == 'dbmeasures' and objectId != 'list':
            self.__endpoint = f'dashboard-service/api/workspaces/{self.__wsId}/dashboards/{objectId}/measures'
        else:
            self.__endpoint = f'dashboard-service/api/workspaces/{self.__wsId}/{entity}/{objectId}'
        
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest().json()
        
        if objectId == 'list':
            if entity == 'dashboards':
                return list(map((lambda ob: [ob['guid'], ob['name']]), self.__response))
            elif entity == 'themes':
                return list(filter((lambda ob: not ob['isSystem']), self.__response))
            elif entity == 'user-widgets':
                return list(map((lambda ob: [ob['guid'], ob['name']]), self.__response['userWidgetList']))
        else:
            return self.__response
        
    def getDefaultTheme(self):
        '''Метод получения идентификатора темы по умолчанию.'''
        self.__endpoint = f'dashboard-service/api/workspaces/{self.__wsId}/themes'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest().json()
        return list(filter((lambda ob: ob['isSystem'] and ob['name'] == 'Системная (по умолчанию)'), self.__response))[0]['themeGuid']
    
    def importDSEntity(self, entity: str, data: dict):
        '''Метод импорта сущностей Dashboard Service.\n
        Поддерживает темы и пользовательские виджеты.'''
        if entity not in self.__entities:
            raise Exception('Unknown entity!')
        
        if entity == 'user-widgets':
            self.__endpoint = f'dashboard-service/api/user-widgets'
            super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers, jsondata=data)
        elif entity == 'themes':
            self.__endpoint = f'dashboard-service/api/workspaces/{self.__wsId}/themes/import'
            super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers, files=data)
        else:
            super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers, data=data)
        
        self.__response = super().sendRequest()
        print(self.__response.status_code, self.__response.text)
    
    def createDashboard(self, dbName:str, dsId:str):
        '''Метод создания пустого дашборда.'''
        self.__endpoint = f'dashboard-service/api/workspaces/{self.__wsId}/dashboards'
        data = {'dashboardName': dbName,
                'dataset': {'datasetId': dsId, 'workspaceId': self.__wsId}
            }
        super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers, jsondata=data)
        self.__response = super().sendRequest()
        return self.__response.json()
    
    def importDashboard(self, dbId: str, data: dict):
        '''Метод импорта данных дашборда.'''
        self.__endpoint = f'dashboard-service/api/workspaces/{self.__wsId}/dashboards/{dbId}'
        data = {'Dashboard': data}
        headers = self.__headers
        headers['Content-Type'] = 'application/json'
        super().__init__('put', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=headers, jsondata=data)
        self.__response = super().sendRequest()
        return self.__response
    
    def importDashboardMeasure(self, dbId:str, data: dict):
        '''Метод импорта мер на дашбордах'''
        self.__endpoint = f'dashboard-service/api/workspaces/{self.__wsId}/dashboards/{dbId}/measures'
        headers = self.__headers
        headers['Content-Type'] = 'application/json'
        super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=headers, jsondata=data)
        self.__response = super().sendRequest()
        return self.__response.content.decode('utf-8')
    
    def vis2Import(self, mongoAddress:str, mongoUser:str, mongoPass:str, dsId:str):
        '''Метод импорта дашбордов (пользовательских тем и виджетов) из 2й версии платформы.'''
        self.__endpoint = f'dashboard-service/api/workspaces/{self.__wsId}/visiology2/import'
        self.__request = {
            'MongoDbConnectionString': f'mongodb://{mongoUser}:{mongoPass}@{mongoAddress}:27017/VisiologyVA',
            'Dataset': {'DatasetId': dsId, 'WorkspaceId': self.__wsId}
        }
        super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers, jsondata=self.__request)
        self.__response = super().sendRequest()
        return self.__response.json()
    
    def healthCheck(self):
        self.__endpoint = f'dashboard-service/health'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response.json()
    
    def getDSVersion(self):
        self.__endpoint = f'dashboard-service/version'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response.json()
    
    def getRegularReports(self):
        '''Метод получения списка регламентных отчетов'''
        self.__endpoint = f'dashboard-service/api/workspaces/{self.__wsId}/regular-report'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response.json()