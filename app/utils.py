import os
import json
import requests
import time

from typing import Union

def fileDump(name:str, dir:str, data:Union[list, dict]):
    '''Функция сохранения данных в файл'''
    if not os.path.exists(dir):
        os.mkdir(dir)
    fullFilePath = os.path.join(dir, name)

    with open(fullFilePath, 'w') as file:
        file.write(json.dumps(data))

def saveUrl(url: str, path: str, name: str, cert):
    '''Функция сохранения файлов по ссылке из minio.'''
    if not os.path.exists(f'{path}'):
        os.mkdir(f'{path}')
    response = requests.get(url, verify=cert)
    if response.status_code == 200:
        with open(f'{path}//{name}', 'wb') as file:
            file.write(response.content)

def uploadFile(fileType:str, url: str, fileName: str, cert):
    '''Функция загрузки файлов в minio.'''
    if fileType == 'csv':
        headers = {"Content-Type": "text/csv"}
    elif fileType == 'excel':
        headers = {"Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}
    else:
        raise Exception('Неизвестный тип файла.')
    with open(fileName, 'rb') as file:
        data = file.read()
        response = requests.put(url, verify=cert, headers=headers, data=data)
        print(f'{response.status_code} Uploaded {os.path.split(fileName)[1]}')

def fillSheetNames(data: dict, id: str, tempName: str, sourceName: str):
    '''Функция заполнения имен листов в метаданных для файлов Excel.'''
    for sheet in data['excelPageDataSources']:
        if sheet['id'] == id:
            sheet['tempTableName'] = tempName
            sheet['originalPageName'] = sourceName
    return data

def transformExcelMetadata(data: list) -> dict:
    '''Функция преобразования метаданных файлов Excel.'''
    result = {"bucketName": "excel", "fileSheetsMappings": []}
    for excelMeta in data:
        excelMeta['tempFileName'] = excelMeta['uniqueFileName']
        del excelMeta['id']
        excelMeta['bucketName'] = ''
        excelMeta['sheets'] = excelMeta.pop('excelPageDataSources')
        for sheet in excelMeta['sheets']:
            del sheet['tempTableName']
            sheet['originalName'] = sheet.pop('originalPageName')
            sheet['newName'] = sheet['originalName']
            sheet['values'] = []
            sheet['schema'] = sheet.pop('columns')
        result['fileSheetsMappings'].append(excelMeta)
    return result

def recursiveCheck(anchor):
    '''Функция проверки отрабатывания операций для исключения их пересечений.'''
    time.sleep(5)
    condition = anchor()
    print(condition)
    if condition:
        recursiveCheck(anchor)
    else:
        return

def askPasswords(data: list):
    '''Функция подстановки паролей к внешним базам данных через CLI.'''
    for loader in data:
        if loader['webAddress']:
            print(loader['webAddress'])
            password = input('Введите пароль к базе данных: ')
            loader['password'] = password
        if loader['connectionString']:
            print(loader['connectionString'])
            password = input('Введите пароль к базе данных: ')
            loader['password'] = password
    return data