from typing import Union

from api.ApiRequest import ApiRequest

class DataManagementService(ApiRequest):
    '''Класс для работы с сервисом DataManagement'''
    def __init__(self, protocol: str, address: str, cert: Union[str, bool], bearer: str) -> None:
        '''Инициализация экземпляра общих параметров обращения к data-management-service.'''
        self.__protocol = protocol
        self.__address = address
        self.__cert = cert
        self.__headers = {'Authorization': f'{bearer}'}
    
    def getWorkspaceDatasources(self, wsId:str):
        '''Метод получения подключений JDBC рабочей области'''
        self.__endpoint = f'data-management-service/api/v1/workspaces/{wsId}/datasources/all'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response
    
    def getDatasetDatasources(self, wsId:str, dsId:str):
        '''Метод получения подключений JDBC набора данных'''
        self.__endpoint = f'data-management-service/api/v1/workspaces/{wsId}/datasets/{dsId}/datasources/all'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response

    def getJDBCDataLoaders(self, wsId:str, dsId:str):
        '''Метод получения JDBC загрузчиков данных'''
        self.__endpoint = f'data-management-service/api/v1/workspaces/{wsId}/datasets/{dsId}/dataloader/Dataloaders'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response
    
    def getTableJDBCDatasource(self, wsId:str, dsId:str, tId:str):
        '''Метод получения подключения JDBC таблицы'''
        self.__endpoint = f'data-management-service/api/v1/workspaces/{wsId}/datasets/{dsId}/datasources/JDBC/{tId}'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response
    
    # def importJDBCLoader(self, data, version:int):
    #     '''DEPRECATED Метод импорта JDBC загрузчика'''
    #     self.__endpoint = f'data-management-service/api/v1/workspaces/{wsId}/datasets/{dsId}/dataloader/changedPassword/true/LoadJDBC'
    #     headers = self.__headers
    #     headers['If-Match'] = str(version)
    #     super().__init__('put', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=headers, jsondata=data)
    #     self.__response = super().sendRequest()
    #     return self.__response.text
    
    def importJDBCLoader(self, wsId:str, dsId:str, loaderData:dict, version:int):
        '''Метод импорта JDBC загрузчика'''
        self.__endpoint = f'data-management-service/api/v1/workspaces/{self.__wsId}/datasets/{self.__dsId}/dataloader'
        headers = self.__headers
        headers['If-Match'] = str(version)
        super().__init__('put', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=headers, json=loaderData)
        self.__response = super().sendRequest()
        return self.__response
    
    def refreshJDBC(self, wsId:str, dsId:str, tableList: list):
        '''Метод обновления данных нескольких JDBC-загрузчиков.\n
        tableList - список строк с идентификаторами обновляемых JDBC таблиц'''
        self.__endpoint = f'data-management-service/api/v1/workspaces/{wsId}/datasets/{dsId}/refresh'
        super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers, json=tableList)
        self.__response = super().sendRequest()
        return self.__response
    
    def refreshTable(self, wsId:str, dsId:str, tId: str):
        '''Метод обновления данных в таблице.\n
        Работает с JDBC и CSV источниками.'''
        self.__endpoint = f'data-management-service/api/v1/workspaces/{wsId}/datasets/{dsId}/table/{tId}/refresh'
        super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers, json={})
        self.__response = super().sendRequest()
        return self.__response
    
    def getExcelDataSource(self, wsId:str, dsId:str, sourceId:str):
        self.__endpoint = f'data-management-service/api/v1/workspaces/{wsId}/datasets/{dsId}/datasources/Excel/{sourceId}'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response
    
    def importExcelLoader(self, wsId:str, dsId:str, loaderData: dict, version: int):
        '''Метод импорта данных источника Excel\n
        Требует проверки версии набора данных.'''
        self.__endpoint = f'data-management-service/api/v1/workspaces/{wsId}/datasets/{dsId}/dataloader/LoadExcelWithMeta'
        headers = self.__headers
        headers['If-Match'] = str(version)
        super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=headers, json=loaderData)
        self.__response = super().sendRequest()
        return self.__response
    
    def getExcelMeta(self, wsId:str, dsId:str, objectData:dict, sourceId:str=''):
        '''Метод получения метаданных источников данных Excel из набора данных.'''
        if sourceId:
            self.__endpoint = f'data-management-service/api/v1/workspaces/{wsId}/datasets/{dsId}/datasources/Excel/GetExcelMeta/{sourceId}'
        else:
            self.__endpoint = f'data-management-service/api/v1/workspaces/{wsId}/datasets/{dsId}/datasources/Excel/GetExcelMeta'
        super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers, json=objectData)
        self.__response = super().sendRequest()
        return self.__response
    
    def triggerExcelUpdate(self, wsId:str, dsId:str, objectData:dict):
        '''Метод обновления данных в источнике Excel'''
        self.__endpoint = f'data-management-service/api/v1/workspaces/{wsId}/datasets/{dsId}/datasources/Excel/Trigger'
        super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers, json=objectData)
        self.__response = super().sendRequest()
        return self.__response
    
    def getCSVDataSource(self, wsId:str, dsId:str, sourceId:str):
        self.__endpoint = f'data-management-service/api/v1/workspaces/{wsId}/datasets/{dsId}/datasources/CSV/{sourceId}'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response
    
    def importCSVLoader(self, wsId:str, dsId:str, objectData:dict, version:int):
        '''Метод импорта данных источника CSV'''
        self.__endpoint = f'data-management-service/api/v1/workspaces/{wsId}/datasets/{dsId}/dataloader/LoadCSVWithMeta'
        headers = self.__headers
        headers['If-Match'] = str(version)
        super().__init__('put', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=headers, json=objectData)
        self.__response = super().sendRequest()
        return self.__response
    
    def checkOperations(self, wsId:str, dsId:str):
        '''Метод проверки операций с данными модели'''
        self.__endpoint = f'data-management-service/api/v1/workspaces/{wsId}/datasets/{dsId}/model/operations'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response
    
    def getScheduleJobs(self, wsId:str):
        '''Метод получения заданий обновлений наборов данных рабочей области.'''
        self.__endpoint = f'data-management-service/api/v1/workspaces/{wsId}/scheduled-refresh/GetAll'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response
    
    def triggerScheduledUpdate(self, wsId:str, dsId:str, version):
        '''Метод запуска запланированного обновления набора данных'''
        self.__endpoint = f'data-management-service/api/v1/workspaces/{wsId}/scheduled-refresh/{dsId}/Trigger'
        headers = self.__headers
        headers['If-Match'] = str(version)
        super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=headers, jsondata={})
        self.__response = super().sendRequest()
        return self.__response
    
    def getNetworkStorage(self):
        '''Метод получения информации о настроенных сетевых папках.'''
        self.__endpoint = f'data-management-service/api/v1/NetworkStorage'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response

    def getMinioLink(self, wsId:str, dsId:str, operation: str, fileName: str):
        '''Метод получения ссылки на файл в хранилище minio\n
        Типы операций: "download", "upload"'''
        if operation not in ['download', 'upload']:
            raise Exception('Unknown operation!')
        
        if operation == 'download':
            self.__endpoint = f'data-management-service/api/v1/workspaces/{wsId}/datasets/{dsId}/datasources/{fileName}/PresignedDownloadURI'
        elif operation == 'upload':
            self.__endpoint = f'data-management-service/api/v1/workspaces/{wsId}/datasets/{dsId}/fileLoader/{fileName}/PresignedUploadURI'

        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response