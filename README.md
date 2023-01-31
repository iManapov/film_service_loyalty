# Сервис системы лояльности


## Запуск в Docker
Предварительно необходимо в корне проекта создать файлы `admin.env` и `api.env`

Параметры `.env` файлов можно найти в
[admin_panel/README.md](./admin_panel/README.md) 
и [loyalty_api/README.md](./loyalty_api/README.md) соответственно.

Для запуска api в `Docker` необходимо выполнить команду
```shell
docker compose up --build
```

Адрес документации: http://localhost:80/api/openapi/