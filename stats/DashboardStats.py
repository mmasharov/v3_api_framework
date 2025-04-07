class DashboardStats:
    '''Класс сбора базовой статистики дашборда'''
    def __init__(self, dashboard):
        self.__dashboard = dashboard
        self.__stats = {'sheetsTotal': 0, 'sheets':[], 'widgetsTotal': 0, 'widgets': {}, 'customCodeWidgets': 0, 'customCodeLines': 0}
    
    def getDashboardStats(self):
        '''Метод получения объекта с базовой статистикой дашборда'''
        for sheet in self.__dashboard['sheets']:
            self.__stats['sheets'].append(sheet['name'])
            for widget in sheet['widgets']:
                if widget['Type'] not in self.__stats['widgets']:
                    self.__stats['widgets'][widget['Type']] = 1
                else:
                    self.__stats['widgets'][widget['Type']] += 1
                self.__stats['widgetsTotal'] += 1
                if widget['overriddenCode']:
                    self.__stats['customCodeWidgets'] += 1
                    self.__stats['customCodeLines'] += widget['overriddenCode'].count('\r\n')
        self.__stats['sheetsTotal'] = len(self.__stats['sheets'])
        return self.__stats