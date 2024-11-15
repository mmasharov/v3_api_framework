import os
import json
import re

from typing import Union

from api.services.DashboardService import DashboardService
from api.services.FormulaEngineService import FormulaEngineService
from api.services.DataManagementService import DataManagementService

from api.middleware import transformDbMeasures

from app.utils import recursiveCheck, uploadFile

class UserWidgetImport:
    def __init__(self, protocol: str, address: str, cert: Union[str, bool], bearer: str, wsId: str,  dirName:str):
        self.__protocol = protocol
        self.__address = address
        self.__cert = cert
        self.__bearer = bearer
        self.__wsId = wsId
        self.__importFile= os.path.join(dirName, 'user_widgets.json')
    
    def importWidget(self):
        if os.path.exists(self.__importFile):
            with open(self.__importFile, 'r') as file:
                self.__widgetData = json.load(file)
        
        if self.__widgetData:
            for widget in self.__widgetData:
                ds = DashboardService(self.__protocol, self.__address, self.__cert, self.__bearer, self.__wsId)
                ds.importDSEntity('user-widgets', widget)

class ThemeImport:
    def __init__(self, protocol: str, address: str, cert: Union[str, bool], bearer: str, wsId: str, dirName:str):
        self.__protocol = protocol
        self.__address = address
        self.__cert = cert
        self.__bearer = bearer
        self.__wsId = wsId
        self.__importFile= os.path.join(dirName, 'theme_data.json')
    
    def importTheme(self):
        if os.path.exists(self.__importFile):
            with open(self.__importFile, 'rb') as f:
                files = {'file': ('theme_data.json', f, 'application/json')}
                ds = DashboardService(self.__protocol, self.__address, self.__cert, self.__bearer, self.__wsId)
                ds.importDSEntity('themes', files)

class DatasetImport:
    def __init__(self, protocol: str, address: str, cert: Union[str, bool], bearer: str, wsId: str, dirName:str):
        '''Инициализация параметров экземпляра объекта импорта набора данных.'''
        self.__protocol = protocol
        self.__address = address
        self.__cert = cert
        self.__bearer = bearer
        self.__wsId = wsId
        self.__dirName = dirName
        self.__datasources = os.path.join(self.__dirName, 'datasources.json')
        if os.path.exists(self.__datasources):
            with open(self.__datasources, 'r') as file:
                self.__sourceList = json.load(file)
        self.__fes = FormulaEngineService(self.__protocol, self.__address, self.__cert, self.__bearer, self.__wsId)
        self.__dms = DataManagementService(self.__protocol, self.__address, self.__cert, self.__bearer, self.__wsId, self.__sourceList['id'])
    
    def returnId(self):
        return self.__sourceList['id']
            
    def createDataset(self):
        '''Метод импорта пустого набора данных'''
        self.__fes.importFEEntity(self.__sourceList['id'], self.__sourceList['name'])

    def importLoaders(self, jdbcData: list):
        '''Метод импорта загрузчиков.\n
        Данные JDBC должны быть обработаны заранее.'''
        # JDBC загрузчики
        for loader in jdbcData:
            recursiveCheck(self.__dms.checkOperations)
            version = self.__fes.getFEEntity('datasets', self.__sourceList['id'])['version']
            loaderId = self.__dms.importJDBCLoader(loader, version)
            recursiveCheck(self.__dms.checkOperations)
            self.__dms.refreshTable(loaderId)

        # Excel загрузчики
        for f in self.__sourceList['excel']['fileSheetsMappings']:
            link = self.__dms.getMinioLink('upload', 'excel', f['uniqueFileName'])
            uploadFile('excel', link, os.path.join(self.__dirName, f['uniqueFileName']), self.__cert)
            body = {
                "bucketName": "excel",
                "originalFileName": f['originalFileName'],
                "newFileName": f['newFileName'],
                "timeStamp": f['timeStamp'],
                "inNetworkStorage": f['inNetworkStorage']
                }
            result = self.__dms.getExcelMeta(body)            
            for sheet1 in f['sheets']:
                for sheet2 in result['fileSheetsMappings'][0]['sheets']:
                    if sheet1['originalName'] == sheet2['originalName']:
                        sheet1['id'] = sheet2['id']
                        sheet1['tomTableId'] = sheet2['tomTableId']
        recursiveCheck(self.__dms.checkOperations)
        version = self.__fes.getFEEntity('datasets', self.__sourceList['id'])['version']
        self.__dms.importExcelLoader(self.__sourceList['excel'], version)
        recursiveCheck(self.__dms.checkOperations)
        self.__dms.triggerExcelData(self.__sourceList['excel'])

        # CSV загрузчики
        for csv in self.__sourceList['csv']:
            link = self.__dms.getMinioLink('upload', 'csv', csv['fileName'])
            uploadFile('csv', link, os.path.join(self.__dirName, csv["fileName"]), self.__cert)
            recursiveCheck(self.__dms.checkOperations)
            version = self.__fes.getFEEntity('datasets', self.__sourceList['id'])['version']
            csvId = self.__dms.importCSVLoader(csv['data'], version)
            self.__dms.refreshTable(csvId)

    def importRelationships(self):
        '''Метод импорта связей таблиц.'''
        tableinfo = self.__fes.getFEEntity('datasets', self.__sourceList['id'])['tables']
        for rel in self.__sourceList['relationships']:
            result = re.findall("\'(.+)\'\[(.+)\]->\'(.+)\'\[(.+)\]", rel['name'])
            tableFrom = list(filter(lambda t: t['name'] == result[0][0], tableinfo))[0]
            columnFrom = list(filter(lambda c: c['name'] == result[0][1], tableFrom['columns']))[0]
            tableTo = list(filter(lambda t: t['name'] == result[0][2], tableinfo))[0]
            columnTo = list(filter(lambda c: c['name'] == result[0][3], tableTo['columns']))[0]
            rel['fromTableId'] = tableFrom['id']
            rel['fromColumnId'] = columnFrom['id']
            rel['toTableId'] = tableTo['id']
            rel['toColumnId'] = columnTo['id']
            del rel['extendedProperties']
            del rel['modelId']
            del rel['isBlockedForUpdate']
            del rel['modifiedTime']
            relId = rel.pop('id')
            recursiveCheck(self.__dms.checkOperations)
            version = self.__fes.getFEEntity('datasets', self.__sourceList['id'])['version']
            self.__fes.importRelationship(self.__sourceList['id'], relId, rel, version)
    
    def importMeasures(self):
        '''Метод импорта обычных мер.'''
        tableinfo = self.__fes.getFEEntity('datasets', self.__sourceList['id'])['tables']
        for tm in self.__sourceList['measures']:
            tId = list(filter(lambda t: t['name'] == tm['tableName'], tableinfo))[0]['id']
            for m in tm['tableMeasures']:
                m['tableId'] = tId
                m['isDashboardMeasure'] = False
                m['isNewMeasure'] = False
                m['state'] = 'Ready'
                del m['extendedProperties']
                recursiveCheck(self.__dms.checkOperations)
                version = self.__fes.getFEEntity('datasets', self.__sourceList['id'])['version']
                self.__fes.importMeasure(self.__sourceList['id'], tId, m['id'], m, version)

class DashboardImport:
    def __init__(self, protocol: str, address: str, cert: Union[str, bool], bearer: str, wsId: str, dsId:str, dirName:str):
        self.__protocol = protocol
        self.__address = address
        self.__cert = cert
        self.__bearer = bearer
        self.__wsId = wsId
        self.__dsId = dsId
        self.__dbs = DashboardService(self.__protocol, self.__address, self.__cert, self.__bearer, self.__wsId)
        if os.path.exists(os.path.join(dirName, 'dashboard_data.json')):
            with open(os.path.join(dirName, 'dashboard_data.json'), 'r') as dbFile:
                self.__dbData = json.load(dbFile)
        else:
            raise Exception('Отсутствуют данные дашборда.')
        if os.path.exists(os.path.join(dirName, 'dashboard-measures.json')):
            with open(os.path.join(dirName, 'dashboard-measures.json'), 'r') as mFile:
                self.__dbMeasuresData = transformDbMeasures(json.load(mFile))
    
    def importDashboard(self):
        newDb = self.__dbs.createDashboard(self.__dbData['name'], self.__dsId)
        for m in self.__dbMeasuresData:
            self.__dbs.importDashboardMeasure(newDb['dashboardGuid'], m)
        self.__dbData['guid'] = newDb['dashboardGuid']
        self.__dbData['workspaceId'] = self.__wsId
        self.__dbData['themeGuid'] = self.__dbs.getDefaultTheme()
        self.__dbData['dataset']['workspaceId'] = self.__wsId
        self.__dbData['dataset']['datasetId'] = self.__dsId
        for s in self.__dbData['sheets']:
            for w in s['widgets']:
                if w['type'] == 'UserWidget':
                    wGuid = list(filter(lambda x: x[1] == w['title']['text'], self.__dbs.getDSEntity('user-widgets')))
                    w['templateGuid'] = wGuid[0][0]
                if w['type'] != 'UserWidget':
                    w['dataQuery']['datasetId'] = self.__dsId
                    w['dataQuery']['workspaceId'] = self.__wsId
        self.__dbs.importDashboard(newDb['dashboardGuid'], self.__dbData)