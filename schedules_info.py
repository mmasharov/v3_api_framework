'''Скрипт выводит в файл информацию о настроенных планировщиках обновлений наборов данных (в виде строки cron)'''
import csv

from api.services.AuthService import AuthService
from api.services.WorkspaceService import WorkspaceService
from api.services.FormulaEngineService import FormulaEngineService
from api.services.DataManagementService import DataManagementService

PROTOCOL = 'https' # Протокол соединения: http или https
ADDRESS = 'visiology.domain.local' # Адрес платформы (без v3)
USER = 'admin' # Имя пользователя (с административными правами)
PASS = '123456' # Пароль
CERT = 'e:/projects/v3migrate/vis.crt' # Путь к файлу сертификата, если используется самоподписанный https При использовании http вместо строки присвоить False
FILE = 'd:/temp/schedules.csv' # Путь к CSV файлу в который будут записаны данные

token = AuthService(PROTOCOL, ADDRESS, CERT, USER, PASS).getBearerString()

result = []
field_names = ['Enabled', 'Workspace', 'Dataset', 'Tables', 'crons']

wss = WorkspaceService(PROTOCOL, ADDRESS, CERT, token)

for workspace in wss.getList():
    fes = FormulaEngineService(PROTOCOL, ADDRESS, CERT, token, workspace['id'])
    if fes.getFEEntity('datasets'):
        dms = DataManagementService(PROTOCOL, ADDRESS, CERT, token, workspace['id'], fes.getFEEntity('datasets')[0][0])
        schedules = dms.getScheduleJobs()
        for dataset in fes.getFEEntity('datasets'):
            data = list(filter(lambda x: x['id'] == dataset[0], schedules))
            if data[0]['crons']:
                if data[0]['isEnabled']:
                    result.append(['on', workspace['name'], dataset[1], '---', data[0]['crons']])
                else:
                    result.append(['off', workspace['name'], dataset[1], '---', data[0]['crons']])
                if data[0]['scheduledLoaderTables']:
                    model = fes.getFEEntity('datasets', dataset[0])
                    for table in data[0]['scheduledLoaderTables']:
                        meta = list(filter(lambda x: x['id'] == table['tableId'], model['tables']))
                        if table['isEnabled']:
                            result.append(['on', workspace['name'], dataset[1], meta[0]['name'], data[0]['crons']])
                        else:
                            result.append(['off', workspace['name'], dataset[1], meta[0]['name'], data[0]['crons']])

with open(FILE, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(field_names)
    writer.writerows(result)