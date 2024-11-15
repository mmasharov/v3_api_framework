import json
import os

from typing import Union

from api.services.DashboardService import DashboardService
from api.services.FormulaEngineService import FormulaEngineService
from api.services.DataManagementService import DataManagementService

from api.middleware import transformDataloader, transformColumns
from app.utils import fileDump, saveUrl, fillSheetNames, transformExcelMetadata

class Dashboard:
    '''Класс экспорта дашборда'''
    def __init__(self, protocol: str, address: str, cert: Union[str, bool], bearer: str, wsId: str, dbId: str) -> None:
        '''Инициализация экземпляра дашборда с составляющими'''
        self.__protocol = protocol
        self.__address = address
        self.__bearer = bearer
        self.__wsId = wsId
        self.__cert = cert
        self.__ds = DashboardService(protocol, address, self.__cert, bearer, wsId)
        self.__dashboard = self.__ds.getDSEntity('dashboards', dbId)
        self.__dbMeasures = self.__ds.getDSEntity('dbmeasures', dbId)
        self.__dataset = FormulaEngineService(protocol, address, self.__cert, bearer, wsId).getFEEntity('datasets', self.__dashboard['dataset']['datasetId'])
        self.__dms = DataManagementService(protocol, address, self.__cert, bearer, wsId, self.__dashboard['dataset']['datasetId'])
        self.__jdbc = DataManagementService(self.__protocol, self.__address, self.__cert, self.__bearer, self.__wsId, self.__dataset['id']).getDMSEntity('jdbc')
        self.__datasetMetadata = {'id': self.__dataset['id'],
                                  'name': self.__dataset['name'],
                                  'jdbc': transformDataloader(self.__jdbc),
                                  'csv': [],
                                  'excel': [],
                                  'relationships': self.__dataset['relationships'],
                                  'measures': []}
        for table in self.__dataset['tables']:
            dataSource = json.loads(table['source'])
            if dataSource['SourceType'] == 1:
                csvFile = self.__dms.getDMSEntity('csv', dataSource['DataSourceId'])
                csvFile['columns'] = transformColumns(table['columns'])
                csvFile['tableName'] = table['name']
                self.__datasetMetadata['csv'].append({
                    "tableId": table['id'],
                    "tableName": table['name'],
                    "fileName": dataSource['SourceTableName'],
                    "data": csvFile
                })
            elif dataSource['SourceType'] == 2:
                if not self.__datasetMetadata['excel'] or dataSource['DataSourceId'] not in list(map(lambda x: x['id'], self.__datasetMetadata['excel'])):
                    excelMeta = self.__dms.getDMSEntity('excel', dataSource['DataSourceId'])
                    self.__datasetMetadata['excel'].append(fillSheetNames(excelMeta, dataSource['PageDataSourceId'], dataSource['TempTableName'], dataSource['SourceTableName']))
                else:
                    for element in self.__datasetMetadata['excel']:
                        element = fillSheetNames(element, dataSource['PageDataSourceId'], dataSource['TempTableName'], dataSource['SourceTableName'])
            if table['measures']:
                measuresData = {'tableName': table['name'], 'tableMeasures': table['measures']}
                self.__datasetMetadata['measures'].append(measuresData)
        self.__datasetMetadata['excel'] = transformExcelMetadata(self.__datasetMetadata['excel'])

        self.__theme = self.__ds.getDSEntity('themes', self.__dashboard['themeGuid'])
        self.__userWidgets = []
        for sheet in self.__dashboard['sheets']:
            for widget in sheet['widgets']:
                if widget['Type'] == 'UserWidget':
                    widgetData = self.__ds.getDSEntity('user-widgets', widget['templateGuid'])
                    del widgetData['guid']
                    self.__userWidgets.append(widgetData)
    
    def export(self, parentDir: str):
        '''Метод экспорта дашборда и связанных сущностей'''
        fileDump('dashboard_data.json', os.path.join(parentDir, self.__dashboard['name']), self.__dashboard)
        fileDump('dashboard-measures.json', os.path.join(parentDir, self.__dashboard['name']), self.__dbMeasures)
        fileDump('dataset_data.json', os.path.join(parentDir, self.__dashboard['name']), self.__dataset)
        fileDump('datasources.json', os.path.join(parentDir, self.__dashboard['name']), self.__datasetMetadata)

        for file in self.__datasetMetadata['csv']:
            saveUrl(self.__dms.getMinioLink('download', 'csv', file['fileName']), os.path.join(parentDir, self.__dashboard['name']), file['fileName'], self.__cert)
        for file in self.__datasetMetadata['excel']['fileSheetsMappings']:
            saveUrl(self.__dms.getMinioLink('download', 'excel', file['uniqueFileName']), os.path.join(parentDir, self.__dashboard['name']), file['uniqueFileName'], self.__cert)

        if self.__theme and not self.__theme['IsSystem']:
            fileDump('theme_data.json', os.path.join(parentDir, self.__dashboard['name']), self.__theme)
        if self.__userWidgets:
            fileDump('user_widgets.json', os.path.join(parentDir, self.__dashboard['name']), self.__userWidgets)