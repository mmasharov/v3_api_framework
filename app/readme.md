# Перенос дашборда со связанными сущностями

## Переносимые сущности

1. Дашборд
2. Пользовательские виджеты дашборда
3. Пользовательская тема дашборда
4. Набор данных, привязанный к дашборду

## Особенности переноса

Перенос данных должен осуществляться между одинаковыми версиями платформы.
Тестировалось на версиях: 3.9, 3.9.1, 3.10

### Набор данных

Переносятся следующие источники данных:
- JDBC загрузчики
- загрузчики файлов CSV
- загрузчики файлов Excel

Перенос загрузчиков файлов из сетевых хранилищ пока не реализован.

На сервере на который переносятся данные должны быть доступны внешние базы данных к которым подключаются JDBC-загрузчики.
Должны присутствовать сторонние драйвера для подключений JDBC-загрузчиков.

В процессе переноса необходимо указать пароли к подключениям переносимых загрузчиков JDBC.