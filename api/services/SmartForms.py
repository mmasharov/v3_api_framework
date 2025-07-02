from typing import Union

from api.ApiRequest import ApiRequest

class SmartForms(ApiRequest):
    '''Класс для работы с модулем SmartForms'''
    def __init__(self, protocol:str, address:str, cert:Union[str, bool], bearer:str):
        '''Инициализация экземпляра подключения к API модуля SmartForms'''
        self.__protocol = protocol
        self.__address = address
        self.__cert = cert
        self.__headers = {'Authorization': f'{bearer}', 'x-api-version': '2.0'}
    
    def getDimensions(self):
        '''Метод получения списка измерений'''
        self.__endpoint = 'smart-forms/api/dimensions'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest().json()
        return self.__response
    
    def getDimElements(self, dimName:str):
        '''Метод получения элементов измерения'''
        self.__endpoint = f'smart-forms/api/dimensions/{dimName}/elements'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest().json()
        return self.__response
    
    def getDimFolders(self, dimName:str):
        '''Метод получения каталогов измерения'''
        self.__endpoint = f'smart-forms/api/dimensions/{dimName}/folders'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest().json()
        return self.__response
    
    def getDimLevels(self, dimName:str):
        '''Метод получения уровней измерения'''
        self.__endpoint = f'smart-forms/api/dimensions/{dimName}/levels'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest().json()
        return self.__response
    
    def getDimAttributes(self, dimName:str):
        '''Метод получения атрибутов измерения'''
        self.__endpoint = f'smart-forms/api/dimensions/{dimName}/attributes'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest().json()
        return self.__response
    
    def addDimElement(self, dimName:str, data:list):
        '''Метод добавления элемента в измерение'''
        self.__endpoint = f'smart-forms/api/dimensions/{dimName}/elements'
        super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers, jsondata=data)
        self.__response = super().sendRequest().json()
        return self.__response
    
    def getMeasureGroups(self):
        '''Метод получения списка группы показателей'''
        self.__endpoint = 'smart-forms/api/measuregroups'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest().json()
        return self.__response
    
    def getMGdescr(self, mgName:str):
        '''Метод получения описания группы показателей'''
        self.__endpoint = f'smart-forms/api/measuregroups/{mgName}'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest().json()
        return self.__response
    
    def getMGforms(self, mgName:str):
        '''Метод получения списка форм группы показателей'''
        self.__endpoint = f'smart-forms/api/measuregroups/{mgName}/forms'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest().json()
        return self.__response
    
    def getMGformStates(self, mgName:str, formId:str):
        '''Метод получения статусов формы группы показателей'''
        self.__endpoint = f'smart-forms/api/measuregroups/{mgName}/forms/{formId}/states'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest().json()
        return self.__response
    
    def getMGelements(self, mgName:str):
        '''Метод получения элементов группы показателей'''
        self.__endpoint = f'smart-forms/api/measuregroups/{mgName}/elements'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest().json()
        return self.__response
    
    def addMGElements(self, mgName:str, data:list):
        '''Метод добавления элементов в группу показателей'''
        self.__endpoint = f'smart-forms/api/measuregroups/{mgName}/elements'
        super().__init__('post', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers, jsondata=data)
        self.__response = super().sendRequest().json()
        return self.__response
    
    def getMGelementsDetails(self, mgName:str):
        '''Метод получения элементов группы показателей с именами измерений и их элементами'''
        self.__endpoint = f'smart-forms/api/measuregroups/{mgName}/elements/details'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest().json()
        return self.__response
    
    def getBusinessProcesses(self):
        '''Метод получения списка бизнес-процессов'''
        self.__endpoint = 'smart-forms/api/businessprocesses'
        super().__init__('get', self.__protocol, self.__address, self.__cert, endpoint=self.__endpoint, headers=self.__headers)
        self.__response = super().sendRequest().json()
        return self.__response