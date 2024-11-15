from typing import Union

from api.ApiRequest import ApiRequest

class DataManagementService(ApiRequest):
    '''Класс для работы с сервисом DataManagement'''
    def __init__(self, protocol: str, address: str, cert: Union[str, bool], bearer: str, wsId: str, dsId:str) -> None:
        '''Инициализация экземпляра общих параметров обращения к data-management-service.'''
        self.__entities = ['jdbc', 'csv', 'excel']
        self.__protocol = protocol
        self.__address = address
        self.__cert = cert
        self.__headers = {'Authorization': f'{bearer}'}
        self.__wsId = wsId
        self.__dsId = dsId

    def getDMSEntity(self, entity:str, id:str='list'):
        '''Метод получения сущности DMS\n
        Доступные сущности: "jdbc", "csv", "excel"'''
        if entity not in self.__entities:
            raise Exception('Unknown entity!')
        
        if entity == 'jdbc':
            self.__endpoint = f'data-management-service/api/v1/workspaces/{self.__wsId}/datasets/{self.__dsId}/dataloader/Dataloaders'
        elif entity == 'excel' and id != 'list':
            self.__endpoint = f'data-management-service/api/v1/workspaces/{self.__wsId}/datasets/{self.__dsId}/datasources/Excel/{id}'
        elif entity == 'csv' and id != 'list':
            self.__endpoint = f'data-management-service/api/v1/workspaces/{self.__wsId}/datasets/{self.__dsId}/datasources/CSV/{id}'

        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest().json()

        return self.__response
    
    def getExcelMeta(self, data):
        '''Метод получения метаданных источников данных Excel из набора данных.'''
        self.__endpoint = f'data-management-service/api/v1/workspaces/{self.__wsId}/datasets/{self.__dsId}/datasources/Excel/GetExcelMeta'
        super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers, jsondata=data)
        self.__response = super().sendRequest().json()

        return self.__response
    
    def getMinioLink(self, operation: str, entity: str, fileName: str) -> str:
        '''Метод получения ссылки на файл в хранилище minio\n
        Типы файлов: "csv", "excel"\n
        Типы операций: "download", "upload"'''
        if entity not in ['csv', 'excel'] or operation not in ['download', 'upload']:
            raise Exception('Unknown entity or operation!')
        
        if entity == 'csv' and operation == 'download':
            self.__endpoint = f'data-management-service/api/v1/workspaces/{self.__wsId}/datasets/{self.__dsId}/datasources/CSV/{fileName}/PresignedDownloadURI'
        elif entity == 'excel' and operation == 'download':
            self.__endpoint = f'data-management-service/api/v1/workspaces/{self.__wsId}/datasets/{self.__dsId}/datasources/Excel/{fileName}/PresignedDownloadURI'
        elif entity == 'csv' and operation == 'upload':
            self.__endpoint = f'data-management-service/api/v1/workspaces/{self.__wsId}/datasets/{self.__dsId}/fileLoader/csv/{fileName}/PresignedUploadURI'
        elif entity == 'excel' and operation == 'upload':
            self.__endpoint = f'data-management-service/api/v1/workspaces/{self.__wsId}/datasets/{self.__dsId}/fileLoader/excel/{fileName}/PresignedUploadURI'

        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest().text

        return self.__response.replace('http://minio:9000', f'{self.__protocol}://{self.__address}/v3/minio')
    
    def importJDBCLoader(self, data, version:int):
        '''Метод импорта JDBC загрузчика'''
        self.__endpoint = f'data-management-service/api/v1/workspaces/{self.__wsId}/datasets/{self.__dsId}/dataloader/changedPassword/true/LoadJDBC'
        headers = self.__headers
        headers['If-Match'] = str(version)
        super().__init__('put', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=headers, jsondata=data)
        self.__response = super().sendRequest()
        return self.__response.text
    
    def importCSVLoader(self, data, version:int):
        '''Метод импорта данных источника CSV'''
        self.__endpoint = f'data-management-service/api/v1/workspaces/{self.__wsId}/datasets/{self.__dsId}/dataloader/LoadCSVWithMeta'
        headers = self.__headers
        headers['If-Match'] = str(version)
        super().__init__('put', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=headers, jsondata=data)
        self.__response = super().sendRequest()
        return self.__response.content.decode('utf-8')
    
    def importExcelLoader(self, data: dict, version: int):
        '''Метод импорта данных источника Excel\n
        Требует проверки версии набора данных.'''
        self.__endpoint = f'data-management-service/api/v1/workspaces/{self.__wsId}/datasets/{self.__dsId}/dataloader/LoadExcelWithMeta'
        headers = self.__headers
        headers['If-Match'] = str(version)
        super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=headers, jsondata=data)
        self.__response = super().sendRequest()
        return self.__response.content.decode('utf-8')
    
    def triggerExcelData(self, data):
        '''Метод обновления данных в источнике Excel'''
        self.__endpoint = f'data-management-service/api/v1/workspaces/{self.__wsId}/datasets/{self.__dsId}/datasources/Excel/Trigger'
        super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers, jsondata=data)
        self.__response = super().sendRequest()
        return self.__response.content.decode('utf-8')

    def refreshJDBC(self, data: list):
        '''Метод обновления данных нескольких JDBC-загрузчиков.\n'''
        self.__endpoint = f'data-management-service/api/v1/workspaces/{self.__wsId}/datasets/{self.__dsId}/refresh'
        super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers, jsondata=data)
        self.__response = super().sendRequest()
        return self.__response
    
    def refreshTable(self, tId: str):
        '''Метод обновления данных в таблице.\n
        Работает с JDBC и CSV источниками.'''
        self.__endpoint = f'data-management-service/api/v1/workspaces/{self.__wsId}/datasets/{self.__dsId}/table/{tId}/refresh'
        super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response.content.decode('utf-8')
    
    def checkOperations(self):
        '''Метод проверки операций с данными модели'''
        self.__endpoint = f'data-management-service/api/v1/workspaces/{self.__wsId}/datasets/{self.__dsId}/model/operations'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest()
        return self.__response.json()