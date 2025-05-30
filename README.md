# PAYMENTS SYSTEM
Это backend-сервис на Django, имитирующий обработку webhook-ов от банка.
Сервис принимает платежные уведомления, защищается от дублирования операций, корректно начисляет баланс организации по ИНН и логирует изменения баланса.

# Требования
- Python 3.9
- Django 4.2.17
- MySQL
- Docker, Docker Compose

# Как запустить
- Указать переменные окружения в файле .env, пример можно посмотреть в .env.template
- Собрать и запустить контейнеры
```bash
docker compose -f docker-compose.yaml build
docker compose -f docker-compose.yaml up -d
```
- Применить миграции в контейнере с бекендом

# Как запустить тесты
- Дать права пользователю БД на работу с базой
    - Зайти в контейнер с БД
    - Выполнить команду для подключения
    ```bash
    mysql -h db -P 3306 -u <root_user_name> -p
    ```
    - Выдать все права 
    ```bash
    GRANT ALL PRIVILEGES ON *.* TO 'your_db_user_name'@'%' WITH GRANT OPTION;
    FLUSH PRIVILEGES;
    ```

- В контейнере с бекендом зайти в корневую директорию проекта и запустить команду

```bash
pytest
```

