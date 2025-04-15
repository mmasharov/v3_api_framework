'''Скрипт выводит в CSV файл количество строк в таблицах наборов данных в порядке убывания.'''
import csv

from api.services.AuthService import AuthService
from api.services.WorkspaceService import WorkspaceService
from api.services.FormulaEngineService import FormulaEngineService

PROTOCOL = 'https' # Протокол соединения: http или https
ADDRESS = 'visiology.domain.local' # Адрес платформы (без v3)
USER = 'admin' # Имя пользователя (с административными правами)
PASS = '123456' # Пароль
CERT = 'd:/projects/v3migrate/vis.crt' # Путь к файлу сертификата, если используется самоподписанный https При использовании http вместо строки присвоить False
FILE = 'd:/temp/datasets_info.csv' # Путь к CSV файлу в который будут записаны данные

token = AuthService(PROTOCOL, ADDRESS, CERT, USER, PASS).getBearerString()

wss = WorkspaceService(PROTOCOL, ADDRESS, CERT, token)

data = []
field_names = ['Workspace', 'Dataset', 'Table', 'Rows']

for ws in wss.getList():
    fe = FormulaEngineService(PROTOCOL, ADDRESS, CERT, token, ws['id'])
    for ds in fe.getFEEntity('datasets'):
        dsObj = fe.getFEEntity('datasets', ds[0])
        for table in dsObj['tables']:
            rows = fe.tableQuery(ds[0], table['name'])['results'][0]['values'][0][0]
            results = {
                'Workspace': ws['name'],
                'Dataset': dsObj['name'],
                'Table': table['name'],
                'Rows': rows if rows else 0
            }
            data.append(results)

data.sort(key=lambda x: x['Rows'], reverse=True)

with open(FILE, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(data)