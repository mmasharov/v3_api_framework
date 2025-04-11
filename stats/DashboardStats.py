from api.services.DashboardService import DashboardService

class DashboardStats:
    '''Класс сбора базовой статистики дашборда'''
    def __init__(self, dashboard):
        self.__dashboard = dashboard
        self.__stats = {'sheetsTotal': 0, 'widgetsTotal': 0, 'customCodeWidgets': 0, 'customCodeLines': 0}
    
    def getDashboardStats(self, mode:str='compact'):
        '''Метод получения объекта с базовой статистикой дашборда'''
        if mode == 'extended':
            self.__stats['sheets'] = []
            self.__stats['widgets'] = {}
        for sheet in self.__dashboard['sheets']:
            self.__stats['sheetsTotal'] += 1
            if mode == 'extended':
                self.__stats['sheets'].append(sheet['name'])
            for widget in sheet['widgets']:
                self.__stats['widgetsTotal'] += 1
                if mode == 'extended':
                    if widget['Type'] not in self.__stats['widgets']:
                        self.__stats['widgets'][widget['Type']] = 1
                    else:
                        self.__stats['widgets'][widget['Type']] += 1
                if widget['overriddenCode']:
                    self.__stats['customCodeWidgets'] += 1
                    self.__stats['customCodeLines'] += widget['overriddenCode'].count('\r\n')
        return self.__stats

class WorkspaceStats:
    '''Класс для получения базовой статистики по всем дашбордам рабочей области.'''
    def __init__(self, dbService: DashboardService):
        self.__dbService = dbService
        self.__dbList = self.__dbService.getDSEntity('dashboards')
        self.__stats = {'dashboardsTotal': len(self.__dbList), 'sheetsTotal': 0, 'widgetsTotal': 0, 'customCodeWidgets': 0, 'customCodeLines': 0}
    
    def getWorkspaceStats(self, mode:str='compact'):
        '''Метод получения объекта с базовой статистикой рабочей области.'''
        if mode == 'extended':
            self.__stats['dashboards'] = list(map(lambda x: x[1], self.__dbList))
        for dbId in list(map(lambda x: x[0], self.__dbList)):
            dbStats = DashboardStats(self.__dbService.getDSEntity('dashboards', dbId)).getDashboardStats()
            self.__stats['sheetsTotal'] += dbStats['sheetsTotal']
            self.__stats['widgetsTotal'] += dbStats['widgetsTotal']
            self.__stats['customCodeWidgets'] += dbStats['customCodeWidgets']
            self.__stats['customCodeLines'] += dbStats['customCodeLines']
        return self.__stats