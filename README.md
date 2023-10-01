**grnatm**

Серивс получает из GraphQL данные, сохраняет их в своей БД и возвращает кол-во строк по всем таблицам.

В сервисе 5 методов:

`GET localhost:8001/get_launches` Получает Launches из GraphQL и сохраняет в таблицу t_launches.

`GET localhost:8001/get_missions` Получает Launches из GraphQL и сохраняет в таблицу t_missions.

`GET localhost:8001/get_rockets` Получает Launches из GraphQL и сохраняет в таблицу t_rockets.

`GET localhost:8001/get_totals` Показывает кол-во публикаций по миссиям, ракетам и пускам (считает кол-во строк в таблицах t_launches, t_missions, t_rockets).

`GET localhost:8001/clear_all_data` Удаляет все записи из табилиц t_launches, t_missions, t_rockets.

Запуск:

Нужно склонировать репозиторий и в склонированной директории выполнить docker-compose up. 
При запуске сервис создает свою БД postgresql с таблицами t_launches, t_missions, t_rockets.
