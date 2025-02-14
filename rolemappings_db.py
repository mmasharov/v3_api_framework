'''Скрипт выводит в файл назначенные права доступа пользователей и групп пользователей к отдельным дашбордам.'''
import csv

from api.services.AuthService import AuthService
from api.services.WorkspaceService import WorkspaceService
from api.services.DashboardService import DashboardService

PROTOCOL = 'https' # Протокол соединения: http или https
ADDRESS = 'visiology.domain.local' # Адрес платформы (без v3)
USER = 'admin' # Имя пользователя (с административными правами)
PASS = '123456' # Пароль
CERT = 'e:/projects/v3migrate/vis.crt' # Путь к файлу сертификата, если используется самоподписанный https При использовании http вместо строки присвоить False
FILE = 'd:/temp/rolemappings_dashboard.csv' # Путь к CSV файлу в который будут записаны данные

token = AuthService(PROTOCOL, ADDRESS, CERT, USER, PASS).getBearerString()

wss = WorkspaceService(PROTOCOL, ADDRESS, CERT, token)

data = []
field_names = ['Workspace', 'Dashboard', 'Username', 'Groupname', 'Permission']

for ws in wss.getList():
    dbs = DashboardService(PROTOCOL, ADDRESS, CERT, token, ws['id'])
    for db in dbs.getDSEntity('dashboards'):
        permissions = dbs.getDashboardPermissions(db[0])
        if permissions:
            for p in permissions:
                result = {
                    'Workspace': ws['name'],
                    'Dashboard': db[1],
                    'Username': p['username'] if p['subjectType'] == 'User' else '',
                    'Groupname': p['usergroupname'] if p['subjectType'] == 'Group' else '',
                    'Permission': p['assignedPermission']
                }
                data.append(result)

with open(FILE, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(data)