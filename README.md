## Описание

Репозиторий представляет собою инструментарий для сбора данных по инстансам [Мастодона](https://joinmastodon.org/).    

## Ход работы

### * Получение первоначального списка:     
Используюя [query](https://raw.githubusercontent.com/dobrosketchkun/mastodondump/main/query.txt) запрос получить список и часть метаданных из [The Federation](https://the-federation.info/graphql) и сохранить это всё в ```dump.json```

### * Перепаковка данных:   
Запустить [restructure.py](https://github.com/dobrosketchkun/mastodondump/blob/main/restructure.py), в результате чего будет создан файл ```restructured_dump.json```

### * Опрос инстансов:   
Запустить [threads_parse_data.py](https://github.com/dobrosketchkun/mastodondump/blob/main/threads_parse_data.py). Данный скрипт многопотомчно опросит инстансы из файла estructured_dump.json для получения описания и списка забаненных инстансов. Конечный результат будет сохранён в файл ```full.json```
