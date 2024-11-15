import tkinter as tk
import os
import sys
import json

from tkinter import filedialog
from tkinter.simpledialog import askstring

from api.services.AuthService import AuthService
from api.services.WorkspaceService import WorkspaceService
from api.services.DashboardService import DashboardService
from app.Export import Dashboard
from app.Import import ThemeImport, UserWidgetImport, DatasetImport, DashboardImport

class StdoutRedirect:
    def __init__(self, textWidget):
        self.textWidget = textWidget
    
    def write(self, string):
        self.textWidget.configure(state=tk.NORMAL)
        self.textWidget.insert(tk.END, string)
        self.textWidget.configure(state=tk.DISABLED)

    def flush(self):
        pass

class AppGUI:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title('Перенос данных между стендами Visiology3')

        self.modeVar = tk.StringVar()
        self.modeVar.set('export')
        self.protocolVar = tk.StringVar()
        self.protocolVar.set('http')
        self.addressVar = tk.StringVar()
        self.userVar = tk.StringVar()
        self.passwordVar = tk.StringVar()
        self.certificateVar = tk.StringVar()
        self.workspacesVar = tk.Variable()
        self.dashboardsVar = tk.Variable()
        self.importVar = tk.StringVar()

        self.modeFrame = tk.Frame(self.main_window, borderwidth=1, relief=tk.SOLID)
        self.modeLabel = tk.Label(self.modeFrame, text='Выберите режим работы:')
        self.radioButtonExport = tk.Radiobutton(self.modeFrame, text='Экспорт', value='export', variable=self.modeVar, command=lambda: self.dashVisible(True))
        self.radioButtonImport = tk.Radiobutton(self.modeFrame, text='Импорт', value='import', variable=self.modeVar, command=lambda: self.dashVisible(False))

        self.serverFrame = tk.Frame(self.main_window, borderwidth=1, relief=tk.SOLID)
        self.protocolLabel = tk.Label(self.serverFrame, text='Протокол соединения')
        self.radioButtonHttp = tk.Radiobutton(self.serverFrame, text='HTTP', value='http', variable=self.protocolVar)
        self.radioButtonHttps = tk.Radiobutton(self.serverFrame, text='HTTPS', value='https', variable=self.protocolVar)
        self.serverNameLabel = tk.Label(self.serverFrame, text='Адрес сервера (IP или DNS)')
        self.serverName = tk.Entry(self.serverFrame, width=50, textvariable=self.addressVar, justify='center')
        self.userNameLabel = tk.Label(self.serverFrame, text='Имя пользователя')
        self.userName = tk.Entry(self.serverFrame, textvariable=self.userVar, justify='center')
        self.passwordLabel = tk.Label(self.serverFrame, text='Пароль')
        self.password = tk.Entry(self.serverFrame, textvariable=self.passwordVar, show='*', justify='center')
        self.certButton = tk.Button(self.serverFrame, text='Выбрать сертификат', command=self.certFileDiag)
        self.certLabel1 = tk.Label(self.serverFrame, text='Сертификат сервера')
        self.certLabel2 = tk.Label(self.serverFrame, textvariable=self.certificateVar)

        self.workspaceFrame = tk.Frame(self.main_window, borderwidth=1, relief=tk.SOLID)
        self.workspacesLabel = tk.Label(self.workspaceFrame, text='Рабочие области')
        self.getWorkspacesButton = tk.Button(self.workspaceFrame, text='Получить рабочие области', command=self.getWorkspacesList)
        self.workspacesList = tk.Listbox(self.workspaceFrame, width=60, listvariable=self.workspacesVar, selectmode=tk.SINGLE)

        self.dashboardsFrame = tk.Frame(self.main_window, borderwidth=1, relief=tk.SOLID)
        self.dashboardsLabel = tk.Label(self.dashboardsFrame, text='Дашборды')
        self.getDashboardsButton = tk.Button(self.dashboardsFrame, text='Получить список дашбордов', command=self.getDashboardList)
        self.dashboardsList = tk.Listbox(self.dashboardsFrame, width=60, listvariable=self.dashboardsVar, selectmode=tk.SINGLE)
        self.exportDashboardButton = tk.Button(self.dashboardsFrame, text='Экспортировать дашборд', command=self.makeExport)

        self.importFrame = tk.Frame(self.main_window, borderwidth=1, relief=tk.SOLID)
        self.importLabel = tk.Label(self.importFrame, text='Импорт дашборда из папки')
        self.importDirButton = tk.Button(self.importFrame, text='Выбрать папку', command=self.importDirSelect)
        self.importDirLabel = tk.Label(self.importFrame, textvariable=self.importVar)
        self.importText = tk.Text(self.importFrame, width=40, height=10, state=tk.DISABLED)
        self.importStartButton = tk.Button(self.importFrame, text='Импортировать дашборд', command=self.importDashboard)

        self.logFrame = tk.Frame(self.main_window, borderwidth=1, relief=tk.SOLID)
        self.logLabel = tk.Label(self.logFrame, text='Журнал событий')
        self.logText = tk.Text(self.logFrame, height=25, width=60, state=tk.DISABLED)

        self.consoleFrame = tk.Frame(self.main_window, borderwidth=1, relief=tk.SOLID)
        self.consoleLabel = tk.Label(self.consoleFrame, text='Вывод консоли')
        self.consoleText = tk.Text(self.consoleFrame, height=25, width=60, state=tk.DISABLED)

        self.modeFrame.grid(row=0, column=0, sticky='nsew')
        self.modeLabel.pack()
        self.radioButtonExport.pack()
        self.radioButtonImport.pack()

        self.serverFrame.grid(row=1, column=0, rowspan=3, sticky='ns')
        self.protocolLabel.pack()
        self.radioButtonHttp.pack()
        self.radioButtonHttps.pack()
        self.serverNameLabel.pack()
        self.serverName.pack()
        self.userNameLabel.pack()
        self.userName.pack()
        self.passwordLabel.pack()
        self.password.pack()
        self.certLabel1.pack()
        self.certButton.pack()
        self.certLabel2.pack()

        self.workspaceFrame.grid(row=0, column=1, rowspan=2, sticky='ns')
        self.workspacesLabel.pack()
        self.getWorkspacesButton.pack()
        self.workspacesList.pack()

        self.dashboardsFrame.grid(row=2, column=1, rowspan=2, sticky='ns')
        self.dashboardsLabel.pack()
        self.getDashboardsButton.pack()
        self.dashboardsList.pack()
        self.exportDashboardButton.pack()

        self.importLabel.pack()
        self.importDirButton.pack()
        self.importDirLabel.pack()
        self.importText.pack()
        self.importStartButton.pack()

        self.logFrame.grid(row=0, column=2, rowspan=4, sticky='ns')
        self.logLabel.pack()
        self.logText.pack()

        self.consoleFrame.grid(row=0, column=3, rowspan=4, sticky='ns')
        self.consoleLabel.pack()
        self.consoleText.pack()

        self.logEvent('Начало работы')
        sys.stdout = StdoutRedirect(self.consoleText)

        tk.mainloop()

    def certFileDiag(self):
        certFile = filedialog.askopenfilename(filetypes=[('Сертификаты CRT', '*.crt'), ('Сертификаты PEM', '*.pem')])
        self.certificateVar.set(certFile)
        self.logEvent(f'\nВыбран сертификат {certFile}')

    def authToken(self):
        return AuthService(self.protocolVar.get(), self.addressVar.get(), self.certificateVar.get(), self.userVar.get(), self.passwordVar.get()).getBearerString()
    
    def getWorkspacesList(self):
        ws = WorkspaceService(self.protocolVar.get(), self.addressVar.get(), self.certificateVar.get(), self.authToken()).getList()
        self.workspacesVar.set(list(map(lambda w: f'{w["name"]} (ID: {w["id"]})', ws)))

    def getDashboardList(self):
        self.currentWs = self.workspacesList.get(self.workspacesList.curselection()).split(':')[1].strip()[0:-1]
        dbs = DashboardService(self.protocolVar.get(), self.addressVar.get(), self.certificateVar.get(), self.authToken(), self.currentWs).getDSEntity('dashboards')
        self.dashboardsVar.set(list(map(lambda db: f'{db[1]} (ID: {db[0]})', dbs)))
        self.logEvent('\nОтображены дашборды рабочей области ' + self.currentWs)
    
    def makeExport(self):
        self.currentDs = self.dashboardsList.get(self.dashboardsList.curselection()).split(':')[1].strip()[0:-1]
        self.logEvent('\nЭкспортируем дашборд с ID ' + self.currentDs)
        exportDir = filedialog.askdirectory(title='Выберите папку для экспорта')
        self.logEvent(f'\nЭкспортируем в папку {exportDir}')
        Dashboard(self.protocolVar.get(), self.addressVar.get(), self.certificateVar.get(), self.authToken(), self.currentWs, self.currentDs).export(exportDir)
        self.logEvent('\nЭкспорт дашборда завершен')

    def dashVisible(self, mode: bool):
        if mode:
            self.dashboardsFrame.grid(row=1, column=1, rowspan=2, sticky='ns')
            self.importFrame.grid_forget()
            self.logEvent('\nВыбран режим экспорта')
        else:
            self.dashboardsFrame.grid_forget()
            self.importFrame.grid(row=2, column=1, rowspan=2, sticky='nsew')
            self.logEvent('\nВыбран режим импорта')
    
    def importDirSelect(self):
        importDir = filedialog.askdirectory(title='Выберите папку из которой будет импортирован дашборд')
        self.importVar.set(importDir)
        self.logEvent(f'\nВыбрана папка для импорта: {importDir}')
        with open(os.path.join(importDir, 'dashboard_data.json'), 'r') as importfile:
            data = json.load(importfile)
            self.importText.configure(state=tk.NORMAL)
            self.importText.insert(tk.END, data['name'])
            self.importText.insert(tk.END, f'\nID: {data["guid"]}')
            self.importText.configure(state=tk.DISABLED)

    def importDashboard(self):
        self.currentWs = self.workspacesList.get(self.workspacesList.curselection()).split(':')[1].strip()[0:-1]
        dataDir = self.importVar.get()
        self.logEvent(f'\nИмпортируем пользовательскую тему')
        ThemeImport(self.protocolVar.get(), self.addressVar.get(), self.certificateVar.get(), self.authToken(), self.currentWs, dataDir).importTheme()

        self.logEvent(f'\nИмпортируем пользовательские виджеты из дашборда {os.path.basename(dataDir)} в рабочую область {self.currentWs} сервера {self.addressVar.get()}')
        UserWidgetImport(self.protocolVar.get(), self.addressVar.get(), self.certificateVar.get(), self.authToken(), self.currentWs, dataDir).importWidget()

        self.logEvent(f'\nИмпортируем набор данных дашборда {os.path.basename(dataDir)} в рабочую область {self.currentWs} сервера {self.addressVar.get()}...')
        dataset = DatasetImport(self.protocolVar.get(), self.addressVar.get(), self.certificateVar.get(), self.authToken(), self.currentWs, dataDir)
        dataset.createDataset()
        self.logEvent(f'\nИмпортируем загрузчики данных...')
        dataset.importLoaders(self.fillJDBCPasswords())
        self.logEvent(f'\nИмпорт набора данных завершен.')
        self.logEvent(f'\nИмпорт связей таблиц.')
        dataset.importRelationships()
        self.logEvent(f'\nИмпорт связей таблиц завершен.')
        self.logEvent(f'\nИмпорт мер.')
        dataset.importMeasures()
        self.logEvent(f'\nИмпорт мер завершен.')
        self.logEvent(f'\nИмпортируем дашборд.')
        DashboardImport(self.protocolVar.get(), self.addressVar.get(), self.certificateVar.get(), self.authToken(), self.currentWs, dataset.returnId(), dataDir).importDashboard()
        self.logEvent(f'\nИмпорт завершен.')

        
        
    def logEvent(self, text: str):
        self.logText.configure(state=tk.NORMAL)
        self.logText.insert(tk.END, text)
        self.logText.configure(state=tk.DISABLED)

    def fillJDBCPasswords(self):
        dataDir = self.importVar.get()
        with open(os.path.join(dataDir, 'datasources.json'), 'r') as jdbcFile:
            data = json.load(jdbcFile)['jdbc']
            for loader in data:
                if loader['webAddress']:
                    password = askstring('Введите пароль к базе данных', f'Сервер: {loader["webAddress"]} БД {loader["dataBase"]} Пользователь {loader["login"]}', parent=self.main_window)
                    loader['password'] = password
                if loader['connectionString']:
                    password = askstring('Введите пароль к базе данных', loader['connectionString'], parent=self.main_window)
                    loader['password'] = password
            return data