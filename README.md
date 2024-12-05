# Фреймворк переноса данных между стендами Visiology3

Фреймворк использует "неофициальный" API платформы Visiology3 для управления сущностями в системе
и по сути представляет собой "обертку" методов, выполненную на языке Python, для более удобного их использования.

В качестве примера конечного использования, реализовано решение по переносу дашборда со связанным набором данных
с одного стенда на другой, с промежуточной выгрузкой в json-файлы.

## Структура проекта

- Папка **api**
    Содержит рабочие файлы фреймворка для взаимодействия с платформой
    - Папка **services**
        Содержит файлы классов взаимодействия с базовыми компонентами платформы
        - Файл **AuthService.py**
            Содержит класс взаимодействия с компонентом авторизации платформы
        - Файл **DashboardService.py**
            Содержит класс взаимодействия с компонентом Dashboard Service
        - Файл **DataManagementService.py**
            Содержит класс взаимодействия с компонентом Data Managment Service
        - Файл **FormulaEngineService.py**
            Содержит класс взаимодействия с компонентом Formula Engine
        - Файл **WorkspaceService.py**
            Содержит класс взаимодействия с компонентом Workspace Service
    - Файл **ApiRequest.py**
        Файл содержит базовый класс взаимодействия с API платформы.
    - Файл **Core.py**
        Файл содержит классы базовых функций платформы не попадающих под компоненты сервисов
    - Файл **middleware.py**
        Файл в основном содержит функции промежуточной обраотки данных.
- Папка **app**
    Содержит файлы конечных проектов, основанных на фреймворке.
    - Файл **Export.py**
        Содержит класс экспорта дашборда со связанным набором данных.
    - Файл **Import.py**
        Содержит класс импорта дашборда со связанным набором данных.
    - Файл **utils.py**
        Содержит вспомогательные функции.
- Папка **gui**
    Содержит файл GUI-интерфейса для конечных проектов решений на базе фреймворка.
- Файл **main.py**
    Используется для запуска основной логики проекта. На данный момент - это интерфейс экспорта/импорта дашборда.

=======================================================

### Компонент работы с авторизацией в платформе

api -> services -> AuthService.py

#### Класс AuthService (наследует класс ApiRequest)

Параметры инициализации:
1. Протокол (строка)
    Допустимые значения: http, https
2. Адрес платформы (строка)
    IP или DNS адрес сервера платформы, базовая часть
    Примеры значений: 192.168.100.40, bi.domain.org
3. Сертификат сервера платформы (строка/булево)
    При использовании протокола HTTPS с самоподписанным сертификатом сервера платформы, необходимо передать путь
    к файлу открытой части сертификата для его проверки при соединении. При отсутствии необходимости сверять Сертификат
    передается булево значение **False**
    Примеры значений: 'D:\certs\myserver.crt', False
4. Имя пользователя (строка)
    Имя пользователя для авторизации в системе.
    Пользователь должен обладать соответствующими правами для выполнения операций.
5. Пароль пользователя (строка)
    Пароль пользователя под которым происходит авторизация в системе

Методы класса:
- getBearerString
    Тип возвращаемых данных: строка
    Метод возвращает строку с токеном авторизации в системе вида 'Bearer tokenstring'
- isExpired
    Тип возвращаемых данных: булево
    Метод проверяет время истечения токена авторизации.
    Возвращает **True** если токен уже недействителен.

### Компонент работы с рабочими областями

api -> services -> WorkspaceService.py

#### Класс WorkspaceService (наследует класс ApiRequest)

Параметры инициализации:
1. Протокол (строка)
    Допустимые значения: http, https
2. Адрес платформы (строка)
    IP или DNS адрес сервера платформы, базовая часть
    Примеры значений: 192.168.100.40, bi.domain.org
3. Сертификат сервера платформы (строка/булево)
    При использовании протокола HTTPS с самоподписанным сертификатом сервера платформы, необходимо передать путь
    к файлу открытой части сертификата для его проверки при соединении. При отсутствии необходимости сверять Сертификат
    передается булево значение **False**
    Примеры значений: 'D:\certs\myserver.crt', False
4. Строка с токеном авторизации (строка)
    Строка для авторизации по токену. Содержит ключевое слово Bearer и саму строку с токеном.

Методы класса:
- getList
    Тип возвращаемых данных: json список
    Метод возвращает список рабочих областей платформы
- getLicenseInfo
    Тип возвращаемых данных: json объект
    Метод возвращает сведения о лицензии.
- getRoleMappings
    Тип возвращаемых данных: json список
    Метод возвращает сведения о ролях пользователей в рабочей области.
    Параметры:
    1. Идентификатор рабочей области (строка)
- importRoleMapping
    Метод импорта сведений о роли пользователя в рабочей области.
    Параметры:
    1. Сведения о роли пользователя (json объект)
- getUsers
    Метод возвращает список пользователей платформы с информацией о дате последнего подключения и признаком активности УЗ.

### Компонент для работы с сервисом управления данными

api -> services -> DataManagementService.py

#### Класс DataManagementService (наследует класс ApiRequest)

Параметры инициализации:
1. Протокол (строка)
    Допустимые значения: http, https
2. Адрес платформы (строка)
    IP или DNS адрес сервера платформы, базовая часть
    Примеры значений: 192.168.100.40, bi.domain.org
3. Сертификат сервера платформы (строка/булево)
    При использовании протокола HTTPS с самоподписанным сертификатом сервера платформы, необходимо передать путь
    к файлу открытой части сертификата для его проверки при соединении. При отсутствии необходимости сверять Сертификат
    передается булево значение **False**
    Примеры значений: 'D:\certs\myserver.crt', False
4. Строка с токеном авторизации (строка)
    Строка для авторизации по токену. Содержит ключевое слово Bearer и саму строку с токеном.
5. Идентификатор рабочей области (строка)
    Идентификатор рабочей области платформы с объектами которой работает экземпляр класса.
6. Идентификатор набора данных (строка)
    Идентификатор набора данных с которым работает экземпляр класса.

Методы класса:
- getDMSEntity
    Тип возвращаемых данных: json объект
    Метод возвращает объект сущности сервиса DMS - метаданные загрузчиков JDBC-моста/файлов CSV и Excel
    Параметры:
    1. Название сущности (строка)
    Допустимые значения: jdbc, csv, excel
    2. Идентификатор запроса списка (строка, необязательный)
    Строка 'list' для запроса списка сущностей (передается по умолчанию), либо строка с идентификатором сущности
- getExcelMeta
    Тип возвращаемых данных: json объект
    Метод возвращает метаданные файла Excel находящегося во внутреннем хранилище minio
    Параметры:
    1. Данные запроса (json объект)
    JSON-объект, содержащий данные о запрашиваемом файле: имя бакета, изначальное и текщее имя файла, таймстамп, метку нахождения на сетевом диске
- getMinioLink
    Тип возвращаемых данных: строка
    Метод возвращает строку со ссылкой на загрузку или скачивание файла из внутреннего хранилища minio
    Параметры:
    1. Тип операции (строка)
    Допустимые значения: download, upload
    2. Тип файла (строка)
    Допустимые значения: csv, excel
- importJDBCLoader
    Тип взвращаемых данных: строка
    Метод импорта JDBC-загрузчика. Возвращает идентификатор созданной таблицы загрузчика.
    Параметры:
    1. Данные (json объект)
    2. Версия набора данных (целое число)
- importCSVLoader
    Метод импорта загрузчика файла CSV
    Параметры:
    1. Данные (json объект)
    2. Версия набора данных (целое число)
- importExcelLoader
    Метод импорта загрузчика файла Excel
    Параметры:
    1. Данные (json объект)
    2. Версия набора данных (целое число)
- triggerExcelData
    Метод обновления данных в загрузчике Excel
    Параметры:
    1. Данные (json объект)
    Используется тот же самый объект, что при импорте загрузчика файла Excel.
- refreshJDBC
    Метод обновления нескольких загрузчиков JDBC.
    Параметры:
    1. Список идентификаторов таблиц данных JDBC (json список)
- refreshTable
    Метод обновления данных в таблице загрузчика данных.
    Параметры:
    1. Идентификатор таблицы (строка)
- checkOperations
    Метод проверки наличия выполняемых операций компонентов DMS и FE

### Компонент работы с внутренним движком платформы

api -> services -> FormulaEngineService.py

#### Класс FormulaEngineService (наследует класс ApiRequest)

Параметры инициализации:
1. Протокол (строка)
    Допустимые значения: http, https
2. Адрес платформы (строка)
    IP или DNS адрес сервера платформы, базовая часть
    Примеры значений: 192.168.100.40, bi.domain.org
3. Сертификат сервера платформы (строка/булево)
    При использовании протокола HTTPS с самоподписанным сертификатом сервера платформы, необходимо передать путь
    к файлу открытой части сертификата для его проверки при соединении. При отсутствии необходимости сверять Сертификат
    передается булево значение **False**
    Примеры значений: 'D:\certs\myserver.crt', False
4. Строка с токеном авторизации (строка)
    Строка для авторизации по токену. Содержит ключевое слово Bearer и саму строку с токеном.
5. Идентификатор рабочей области (строка)
    Идентификатор рабочей области платформы с объектами которой работает экземпляр класса.

Методы класса:
- getFEEntity
    Метод получения сущностей компонента Formula Engine в виде списка, либо отдельных объектов.
    Параметры:
    1. Сущность
    Допустимые значения: datasets, relationships
    2. Идентификатор возвращаемого объекта (необязательный)
    Допустимые значения: 'list' (передается по умолчанию) либо строка с идентификатором запрашиваемого объекта.
- importFEEntity
    Метод для создания набора данных.
    Параметры:
    1. Идентификатор набора данных (строка)
    2. Имя набора данных (строка)
- importRelationship
    Метод импорта связи между таблицами набора данных.
    Параметры:
    1. Идентификатор набора данных (строка)
    2. Идентификатор связи (строка)
    3. Данные связи между таблицами (json объект)
    4. Версия набора данных (целое число)
- importMeasure
    Метод импорта меры.
    Параметры:
    1. Идентификатор набора данных (строка)
    2. Идентификатор таблицы (строка)
    3. Идентификатор меры (строка)
    4. Данные меры (json объект)
    5. Версия набора данных (целое число)

### Компонент работы с дашбордами

api -> services -> DashboardService.py

#### Класс DashboardService (наследует класс ApiRequest)

Параметры инициализации:
1. Протокол (строка)
    Допустимые значения: http, https
2. Адрес платформы (строка)
    IP или DNS адрес сервера платформы, базовая часть
    Примеры значений: 192.168.100.40, bi.domain.org
3. Сертификат сервера платформы (строка/булево)
    При использовании протокола HTTPS с самоподписанным сертификатом сервера платформы, необходимо передать путь
    к файлу открытой части сертификата для его проверки при соединении. При отсутствии необходимости сверять Сертификат
    передается булево значение **False**
    Примеры значений: 'D:\certs\myserver.crt', False
4. Строка с токеном авторизации (строка)
    Строка для авторизации по токену. Содержит ключевое слово Bearer и саму строку с токеном.
5. Идентификатор рабочей области (строка)
    Идентификатор рабочей области платформы с объектами которой работает экземпляр класса.

Методы класса:
- getDSEntity
    Метод получения объектов сущностей сервиса дашбордов в виде списка либо конкретных объектов.
    Параметры:
    1. Тип сущности (строка)
    Допустимые значения: user-widgets, themes, dashboards, dbmeasures
    2. Идентификатор объекта (строка, необязательный)
    Значение по умолчанию - 'list', возвращает список объектов данной сущности.
- getDefaultTheme
    Метод получения идентификатора темы по умолчанию.
- importDSEntity
    Метод имопрта отдельных сущностей.
    Параметры:
    1. Тип сущности (строка)
    Допустимые значения: user-widgets, themes
    2. Данные (json объект)
    Данные сущности.
- createDashboard
    Метод создания нового дашборда.
    Параметры:
    1. Название дашборда (строка)
    2. Идентификатор набора данных (строка)
- importDashboard
    Метод импорта данных дашборда.
    Параметры:
    1. Идентификатор дашборда (строка)
    2. Данные (json объект)
- importDashboardMeasure
    Метод импорта мер дашюорда.
    Параметры:
    1. Идентификатор дашборда (строка)
    2. Данные (json объект)
- vis2Import
    Метод импорта дашбордов, пользовательских виджетов и тем из 2й версии платформы.
    Реализует функционал из [статьи официальной документации](https://visiology-doc.atlassian.net/wiki/spaces/3v10/pages/714903587/2.)
    Параметры:
    1. Сервер MongoDB Visiology2 (IP/DNS/внутреннее имя контейнера)
    2. Имя пользователя MongoDB
    3. Пароль пользователя MongoDB
    4. Идентификатор набора данных для привязки к импортируемым виджетам
- healthCheck
    Метод получения информации о состоянии сервера
- getDSVersion
    Метод получения сведений о версии компонента Dashboard Service

### Базовый класс запросов к API

api -> ApiRequest.py

Предоставляет другим классам базовый функционал сетевых запросов к API платформы.
Реализованы методы GET, POST, PUT

### Набор базовых функций платформы

api -> Core.py

#### Класс Platform (наследует класс ApiRequest)

Параметры инициализации:
1. Протокол (строка)
    Допустимые значения: http, https
2. Адрес платформы (строка)
    IP или DNS адрес сервера платформы, базовая часть
    Примеры значений: 192.168.100.40, bi.domain.org
3. Сертификат сервера платформы (строка/булево)
    При использовании протокола HTTPS с самоподписанным сертификатом сервера платформы, необходимо передать путь
    к файлу открытой части сертификата для его проверки при соединении. При отсутствии необходимости сверять Сертификат
    передается булево значение **False**
    Примеры значений: 'D:\certs\myserver.crt', False
4. Строка с токеном авторизации (строка)
    Строка для авторизации по токену. Содержит ключевое слово Bearer и саму строку с токеном.

Методы класса:
- versionInfo
    Метод полчения версий компонентов платформы.

### Набор функций промежуточной обработки данных

api -> middleware.py

Предоставляемые функции:
- transformDataloader
    Преобразует метаданные загрузчика JDBC.
- transformColumns
    Преобразует колонки загрузчика CSV файла.
- transformDbMeasures
    Преобразует меры дашборда.

## Проекты реализации конечного функционала

### Компонент экспорта дашборда со связанными сущностями

app -> Export.py

#### Класс Dashboard

Параметры инициализации:
1. Протокол (строка)
    Допустимые значения: http, https
2. Адрес платформы (строка)
    IP или DNS адрес сервера платформы, базовая часть
    Примеры значений: 192.168.100.40, bi.domain.org
3. Сертификат сервера платформы (строка/булево)
    При использовании протокола HTTPS с самоподписанным сертификатом сервера платформы, необходимо передать путь
    к файлу открытой части сертификата для его проверки при соединении. При отсутствии необходимости сверять Сертификат
    передается булево значение **False**
    Примеры значений: 'D:\certs\myserver.crt', False
4. Строка с токеном авторизации (строка)
    Строка для авторизации по токену. Содержит ключевое слово Bearer и саму строку с токеном.
5. Идентификатор рабочей области (строка)
    Идентификатор рабочей области платформы с объектами которой работает экземпляр класса.
6. Идентификатор дашборда (строка)
    Идентификатор экспортируемого дашборда

Методы класса:
- export
    Метод экспорта метаданных дашборда и связанных сущностей в набор файлов.
    Выходные данные:
    - dashboard_data.json (данные дашборда)
    - dashboard-measures.json (данные мер на дашборде)
    - dataset_data.json (метаданные набора данных, для дебага)
    - datasources.json (метаданные набора данных, для импорта)
    - файлы CSV, Excel из источников данных
    - theme_data.json (данные пользовательской темы)
    - user_widgets.json (данные пользовательских виджетов)

### Компонент импорта дашборда со связанными сущностями

app -> Import.py

#### Класс UserWidgetImport

Управляет загрузкой пользовательских виджетов.

Параметры инициализации:
1. Протокол (строка)
    Допустимые значения: http, https
2. Адрес платформы (строка)
    IP или DNS адрес сервера платформы, базовая часть
    Примеры значений: 192.168.100.40, bi.domain.org
3. Сертификат сервера платформы (строка/булево)
    При использовании протокола HTTPS с самоподписанным сертификатом сервера платформы, необходимо передать путь
    к файлу открытой части сертификата для его проверки при соединении. При отсутствии необходимости сверять Сертификат
    передается булево значение **False**
    Примеры значений: 'D:\certs\myserver.crt', False
4. Строка с токеном авторизации (строка)
    Строка для авторизации по токену. Содержит ключевое слово Bearer и саму строку с токеном.
5. Идентификатор рабочей области (строка)
    Идентификатор рабочей области платформы с объектами которой работает экземпляр класса.
6. Путь к папке с данными дашборда (строка)

Методы класса:
- importWidget
    Импортирует пользовательский виджет.

#### Класс ThemeImport

Управляет загрузкой пользовательских тем

Параметры инициализации:
1. Протокол (строка)
    Допустимые значения: http, https
2. Адрес платформы (строка)
    IP или DNS адрес сервера платформы, базовая часть
    Примеры значений: 192.168.100.40, bi.domain.org
3. Сертификат сервера платформы (строка/булево)
    При использовании протокола HTTPS с самоподписанным сертификатом сервера платформы, необходимо передать путь
    к файлу открытой части сертификата для его проверки при соединении. При отсутствии необходимости сверять Сертификат
    передается булево значение **False**
    Примеры значений: 'D:\certs\myserver.crt', False
4. Строка с токеном авторизации (строка)
    Строка для авторизации по токену. Содержит ключевое слово Bearer и саму строку с токеном.
5. Идентификатор рабочей области (строка)
    Идентификатор рабочей области платформы с объектами которой работает экземпляр класса.
6. Путь к папке с данными дашборда (строка)

Методы класса:
- importTheme
    Импортирует пользовательскую тему.

#### Класс DatasetImport

Управляет загрузкой набора данных.

Параметры инициализации:
1. Протокол (строка)
    Допустимые значения: http, https
2. Адрес платформы (строка)
    IP или DNS адрес сервера платформы, базовая часть
    Примеры значений: 192.168.100.40, bi.domain.org
3. Сертификат сервера платформы (строка/булево)
    При использовании протокола HTTPS с самоподписанным сертификатом сервера платформы, необходимо передать путь
    к файлу открытой части сертификата для его проверки при соединении. При отсутствии необходимости сверять Сертификат
    передается булево значение **False**
    Примеры значений: 'D:\certs\myserver.crt', False
4. Строка с токеном авторизации (строка)
    Строка для авторизации по токену. Содержит ключевое слово Bearer и саму строку с токеном.
5. Идентификатор рабочей области (строка)
    Идентификатор рабочей области платформы с объектами которой работает экземпляр класса.
6. Путь к папке с данными дашборда (строка)

Методы класса:
- returnId
    Возвращает идентификатор набора данных, содержащийся в метаданных.
- createDataset
    Создает новый набор данных.
- importLoaders
    Загружает метаданные источников данных JDBC, CSV, Excel и обновляет их таблицы.
    Параметры:
    1. Преобразованные данные источников JDBC
- importRelationships
    Загружает связи между таблицами.
- importMeasures
    Загружает меры набора данных.

#### Класс DashboardImport

Управляет загрузкой дашборда.

Параметры инициализации:
1. Протокол (строка)
    Допустимые значения: http, https
2. Адрес платформы (строка)
    IP или DNS адрес сервера платформы, базовая часть
    Примеры значений: 192.168.100.40, bi.domain.org
3. Сертификат сервера платформы (строка/булево)
    При использовании протокола HTTPS с самоподписанным сертификатом сервера платформы, необходимо передать путь
    к файлу открытой части сертификата для его проверки при соединении. При отсутствии необходимости сверять Сертификат
    передается булево значение **False**
    Примеры значений: 'D:\certs\myserver.crt', False
4. Строка с токеном авторизации (строка)
    Строка для авторизации по токену. Содержит ключевое слово Bearer и саму строку с токеном.
5. Идентификатор рабочей области (строка)
    Идентификатор рабочей области платформы с объектами которой работает экземпляр класса.
6. Идентификатор набора данных (строка)
7. Путь к папке с данными дашборда (строка)

Методы класса:
- importDashboard
    Импортирует метаданные дашборда.

### Вспомогательные функции для конечных решений

app -> utils.py

Предоставляемые функции:
- fileDump
    Функция сохранения данных сущности в файл.
    Параметры:
    1. Имя файла (строка)
    2. Путь к папке сохранения (строка)
    3. Данные (json объект)
- saveUrl
    Функция сохранения файла из minio по преподписанной ссылке.
    Параемтры:
    1. Ссылка на скачивание файла (строка)
    2. Путь к папке сохранения (строка)
    3. Имя файла (строка)
    4. Сертификат для верификации HTTPS (строка/булево)
- uploadFile
    Функция загрузки файла во внутренний minio по преподписанной ссылке.
    Параметры:
    1. Тип файла (строка)
    Допустимые значения: csv, excel
    2. Ссылка для загрузки (строка)
    3. Имя файла (строка)
    4. Сертификат для верификации HTTPS (строка/булево)
- fillSheetNames
    Функция заполнения имен листов в метаданных файла Excel
    Параметры:
    1. Метаданные файла Excel (json объект)
    2. Идентификатор листа (строка)
    3. Временное имя листа (строка)
    4. Исходное имя листа (строка)
- transformExcelMetadata
    Функция преобразования метаданных файла Excel
    Параметры:
    1. Метаданные файла Excel (json объект)
- recursiveCheck
    Функция рекурсивной проверки. Используется для проверки наличия активных операций сервисов FE, DMS
    Параметры:
    1. Функция-индикатор (функция)
- askPasswords
    Функция подстановки паролей через CLI в данные загрузчиков JDBC.
    Параметры:
    1. Список загрузчиков JDBC