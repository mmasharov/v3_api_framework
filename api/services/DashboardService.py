from typing import Union

from api.ApiRequest import ApiRequest

class DashboardService(ApiRequest):
    '''Класс взаимодействия с дашбордами'''
    def __init__(self, protocol: str, address: str, cert: Union[str, bool], bearer: str):
        '''Инициализация экземпляра общих параметров для соединения с dashboard-service.'''
        self.__protocol = protocol
        self.__address = address
        self.__cert = cert
        self.__headers = {'Authorization': f'{bearer}'}

    def getDSVersion(self):
        '''Метод получения сведений о версии DashboardService'''
        self.__endpoint = f'dashboard-service/version'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response
    
    def healthCheck(self):
        '''Метод запроса хелсчека сервиса'''
        self.__endpoint = f'dashboard-service/health'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response
    
    def getDashboards(self, wsId:str, dbId:str='', hidden:bool=True) -> Union[list, dict]:
        '''Метод получения списка дашбордов рабочей области или метаданных определенного дашборда'''
        if dbId:
            self.__endpoint = f'dashboard-service/api/workspaces/{wsId}/dashboards/{dbId}'
        else:
            self.__endpoint = f'dashboard-service/api/workspaces/{wsId}/dashboards'
        if hidden:
            self.__params = {'withHiddenSheets': 'true'}
            super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers, params=self.__params)
        else:
            super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response
    
    def createDashboard(self, wsId:str, dbName:str, dsInfo:dict) -> dict:
        '''Метод создания пустого дашборда.\n
        Информация о наборе данных: {'datasetId': 'идентификатор', 'workspaceId': 'идентификатор'}\n
        Возвращает объект с идентификатором созданного дашборда.'''
        self.__endpoint = f'dashboard-service/api/workspaces/{wsId}/dashboards'
        self.__data = {'dashboardName': dbName,
                    'dataset': dsInfo
                    }
        super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers, json=self.__data)
        self.__response = super().sendRequest()
        return self.__response
    
    def importDashboard(self, wsId:str, dbId: str, dbData: dict):
        '''Метод импорта метаданных дашборда.'''
        self.__endpoint = f'dashboard-service/api/workspaces/{wsId}/dashboards/{dbId}'
        self.__data = {'dashboard': dbData}
        headers = self.__headers
        headers['Content-Type'] = 'application/json'
        super().__init__('put', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=headers, json=self.__data)
        self.__response = super().sendRequest()
        return self.__response
    
    def getDashboardPermissions(self, wsId:str, dbId:str):
        '''Метод получения сведений о доступах пользователей к дашборду'''
        self.__endpoint = f'dashboard-service/api/workspaces/{wsId}/dashboards/{dbId}/permission-mappings'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response
    
    def exportDashboard(self, wsId:str, dbId:str, data:dict, type:int) -> dict:
        '''Метод экспорта дашборда в PDF/PNG/PPTX\n
        1 - PNG\n
        2 - PDF\n
        4 - PPTX
        '''
        self.__types = [1, 2, 4]
        self.__endpoint = f'dashboard-service/api/workspaces/{wsId}/dashboards/{dbId}/export'
        self.__request = {
            "Dashboard": data,
            "DocumentType": type
        }
        if type not in self.__types:
            raise Exception(f'Неверный тип файла экспорта: {type}')
        super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers, json=self.__request)
        self.__response = super().sendRequest()
        return self.__response
    
    def getDashboardTree(self, minRole:str, depth:int) -> dict:
        '''Метод получения информации о ролевых доступах пользователя к рабочим областям и дашбордам\n
        Роли: viewer, contributor, member, administrator\n
        Уровни: 0 (рабочие области), 1 (дашборды), 2 (листы), 3 (виджеты)
        '''
        if (minRole in ['viewer', 'contributor', 'member', 'administrator'] and depth in [0, 1, 2, 3]):
            self.__endpoint = f'dashboard-service/api/dashboards?minRole={minRole}&depth={str(depth)}'
            super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
            self.__response = super().sendRequest()
            return self.__response
        else:
            raise Exception(f'Неверная роль - {minRole} или глубина поиска - {depth}')
    
    def getThemes(self, wsId:str, tId:str='') -> Union[list, dict]:
        '''Метод получения списка тем рабочей области или метаданных определенной темы'''
        if tId:
            self.__endpoint = f'dashboard-service/api/workspaces/{wsId}/themes/{tId}'
        else:
            self.__endpoint = f'dashboard-service/api/workspaces/{wsId}/themes'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response
    
    def exportTheme(self, wsId:str, tId:str) -> dict:
        '''Метод экспорта пользовательской темы'''
        self.__endpoint = f'dashboard-service/api/workspaces/{wsId}/themes/{tId}/export'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response
    
    def importTheme(self, wsId:str, themeData):
        '''Метод импорта пользовательских тем\n
        Формат входных данных: {'files': ('some_name.json', объект_байткода_файла, 'application/json')}'''
        self.__endpoint = f'dashboard-service/api/workspaces/{wsId}/themes/import'
        super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers, files=themeData)
        self.__response = super().sendRequest()
        return self.__response
    
    def getUserWidgets(self, widgetId:str='') -> list:
        '''Метод получения списка глобальных пользовательских виджетов или сведений о любом определенном виджете'''
        if widgetId:
            self.__endpoint = f'dashboard-service/api/user-widgets/{widgetId}'
        else:
            self.__endpoint = f'dashboard-service/api/user-widgets'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response
    
    def getWSUserWidgets(self, wsId:str) -> list:
        '''Метод получения списка пользовательских виджетов рабочей области'''
        self.__endpoint = f'dashboard-service/api/workspaces/{wsId}/user-widgets'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response
    
    def createUserWidget(self, widgetData:dict):
        '''Метод создания глобального пользовательского виджета из метаданных'''
        self.__endpoint = f'dashboard-service/api/user-widgets'
        super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers, json=widgetData)
        self.__response = super().sendRequest()
        return self.__response
    
    def createWSUserWidget(self, wsId:str, widgetData:dict):
        '''Метод создания глобального пользовательского виджета из метаданных'''
        self.__endpoint = f'dashboard-service/api/workspaces/{wsId}/user-widgets'
        super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers, json=widgetData)
        self.__response = super().sendRequest()
        return self.__response
    
    def exportUserWidget(self, widgetId:str) -> list:
        '''Метод экспорта пользовательского виджета'''
        self.__endpoint = f'dashboard-service/api/user-widgets/{widgetId}/export'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response
    
    def importUserWidget(self, wsId:str, widgetData):
        '''Метод импорта пользовательского виджета из данных файла экспорта'''
        if wsId:
            self.__endpoint = f'dashboard-service/api/workspaces/{wsId}/user-widgets/import'
        else:
            self.__endpoint = f'dashboard-service/api/user-widgets/import'
        super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers, files=widgetData)
        self.__response = super().sendRequest()
        return self.__response
    
    def getDashboardMeasures(self, wsId:str, dbId:str) -> list:
        '''Метод получения мер дашборда'''
        self.__endpoint = f'dashboard-service/api/workspaces/{wsId}/dashboards/{dbId}/measures'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response
    
    def importDashboardMeasure(self, wsId:str, dbId:str, measureData: dict):
        '''Метод импорта мер на дашбордах'''
        self.__endpoint = f'dashboard-service/api/workspaces/{wsId}/dashboards/{dbId}/measures'
        headers = self.__headers
        headers['Content-Type'] = 'application/json'
        super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=headers, json=measureData)
        self.__response = super().sendRequest()
        return self.__response
    
    def getWidgetDataDax(self, wsId:str, dbId:str, wId:str):
        '''Метод получения данных виджета по его идентификатору, в формате DAX ответа от FormulaEngine'''
        self.__endpoint = f'dashboard-service/api/workspaces/{wsId}/dashboards/{dbId}/widgets/{wId}/data/by-widget-id'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response
    
    def getRegularReports(self, wsId:str, rId:str=''):
        '''Метод получения списка регламентных отчетов или сведений об отчете'''
        if rId:
            self.__endpoint = f'dashboard-service/api/workspaces/{wsId}/regular-report/{rId}'
        else:
            self.__endpoint = f'dashboard-service/api/workspaces/{wsId}/regular-report'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response
    
    def getMailSchedules(self, wsId:str, msId:str=''):
        '''Метод получения списка почтовых рассылок или сведений о рассылке'''
        if msId:
            self.__endpoint = f'dashboard-service/api/workspaces/{wsId}/scheduled-reports/dashboard/{msId}'
        else:
            self.__endpoint = f'dashboard-service/api/workspaces/{wsId}/scheduled-reports/dashboard'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response
  
    def vis2Import(self, wsId:str, mongoAddress:str, mongoUser:str, mongoPass:str, dsId:str):
        '''Метод импорта дашбордов (пользовательских тем и виджетов) из 2й версии платформы.'''
        self.__endpoint = f'dashboard-service/api/workspaces/{wsId}/visiology2/import'
        self.__request = {
            'MongoDbConnectionString': f'mongodb://{mongoUser}:{mongoPass}@{mongoAddress}:27017/VisiologyVA',
            'Dataset': {'DatasetId': dsId, 'WorkspaceId': wsId}
        }
        super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers, json=self.__request)
        self.__response = super().sendRequest()
        return self.__response