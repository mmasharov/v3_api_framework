'''Скрипт выводит в файл назначенные права доступа пользователей к рабочим областям. Если заполнено поле группы, то данное право пользователь получил через указанную группу.'''
import csv

from api.services.AuthService import AuthService
from api.services.WorkspaceService import WorkspaceService

PROTOCOL = 'https' # Протокол соединения: http или https
ADDRESS = 'visiology.domain.local' # Адрес платформы (без v3)
USER = 'admin' # Имя пользователя (с административными правами)
PASS = '123456' # Пароль
CERT = 'e:/projects/v3migrate/vis.crt' # Путь к файлу сертификата, если используется самоподписанный https При использовании http вместо строки присвоить False
FILE = 'd:/temp/rolemappings_workspace.csv' # Путь к CSV файлу в который будут записаны данные

token = AuthService(PROTOCOL, ADDRESS, CERT, USER, PASS).getBearerString()

wss = WorkspaceService(PROTOCOL, ADDRESS, CERT, token)

data = []
field_names = ['username', 'usergroupname', 'WorkspaceName', 'assignedRole']

for user in wss.getUsers():
    usergroups = []
    for g in wss.getGroups():
        gusers = list(filter(lambda u: u['userInfo']['username'] == user['username'], wss.getGroupUsers([g['id']])))
        if gusers:
            usergroups.append(g['path'])
    for workspace in wss.getList():
        mappings = list(filter(lambda u: u['username'] == user['username'] or u['usergroupname'] in usergroups, wss.getRoleMappings(workspace['id'])))
        if mappings:
            for m in mappings:
                m['WorkspaceName'] = workspace['name']
                m['username'] = user['username']
                del m['id']
                del m['subjectType']
            data.extend(mappings)

with open(FILE, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(data)