'''Скрипт выводит в файл назначенные права доступа пользователей и групп пользователей к отдельным наборам данных.'''
import csv

from api.services.AuthService import AuthService
from api.services.WorkspaceService import WorkspaceService
from api.services.FormulaEngineService import FormulaEngineService

PROTOCOL = 'https' # Протокол соединения: http или https
ADDRESS = 'visiology.domain.local' # Адрес платформы (без v3)
USER = 'admin' # Имя пользователя (с административными правами)
PASS = '123456' # Пароль
CERT = 'e:/projects/v3migrate/vis.crt' # Путь к файлу сертификата, если используется самоподписанный https При использовании http вместо строки присвоить False
FILE = 'd:/temp/rolemappings_dataset.csv' # Путь к CSV файлу в который будут записаны данные

token = AuthService(PROTOCOL, ADDRESS, CERT, USER, PASS).getBearerString()

wss = WorkspaceService(PROTOCOL, ADDRESS, CERT, token)

data = []
field_names = ['Workspace', 'Dataset', 'Username', 'Groupname', 'Permission']

for ws in wss.getList():
    fes = FormulaEngineService(PROTOCOL, ADDRESS, CERT, token, ws['id'])
    for ds in fes.getFEEntity('datasets'):
        permissions = fes.getDatasetPermissions(ds[0])
        if permissions:
            for p in permissions:
                result = {
                    'Workspace': ws['name'],
                    'Dataset': ds[1],
                    'Username': p['username'] if p['subjectType'] == 'User' else '',
                    'Groupname': p['usergroupname'] if p['subjectType'] == 'Group' else '',
                    'Permission': p['assignedPermissions'][0]
                }
                data.append(result)

with open(FILE, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(data)