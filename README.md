## Описание

Инструментарий для сбора данных по инстансам сети [Mastodon](https://joinmastodon.org/).    

## Алгоритм работы

* _Получение первоначального списка_\
Используя запрос из [query.txt](query.txt), получить список и часть метаданных из [The Federation](https://the-federation.info/graphql) и сохранить результат в файл `dump.json`.

* _Перепаковка данных_\
Запустить [restructure.py](restructure.py), в результате чего будет создан файл `restructured_dump.json`.

* _Опрос инстансов_\
Запустить [threads_parse_data.py](threads_parse_data.py). Данный скрипт в многопоточном режиме опросит инстансы из файла `restructured_dump.json` для получения описания и списка забаненных инстансов и сохранит результат в файл `full.json`.
