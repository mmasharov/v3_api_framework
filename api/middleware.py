def transformDataloader(data:list) -> list:
    '''Функция преобразование данных JDBC загрузчиков.'''
    for item in data:
        for option in item['dataSource'].items():
            item[option[0]] = option[1]
        del item['dataSource']
        del item['hasPassword']
        print(f'Database: {item["connectionString"]}')
        item['password'] = ''
        item['tableName'] = item.pop('sourceTableName')
    return data

def transformColumns(data: list):
    '''Функция преобразование данных CSV загрузчиков.'''
    result = []
    for col in data:
        new_col = {}
        new_col['originalHeader'] = col['name']
        new_col['originalType'] = col['dataType']
        new_col['newHeader'] = col['name']
        new_col['newType'] = col['dataType']
        new_col['isNullable'] = col['isNullable']
        new_col['enabled'] = True
        result.append(new_col)
    return result

def transformDbMeasures(data: list) -> list:
    '''Функция преобразования мер дашбордов.'''
    for m in data:
        del m['id']
        del m['modifiedTime']
        del m['dashboardGuid']
        m['dashboardMeasureName'] = m.pop('name')
    return data