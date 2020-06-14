# binance-bot — stock technical analysis
###### Other language readme files
- [en](README.md)
- [ru](ru_README.md)
## Описание
Project goal — разработка механизма технического анализа рынка криптовалют, который опирается на 
популярные рыночные индикаторы и паттерны.

Task — посчитать связь между значениями индикаторов технического анализа, их производными, относительными кросс-индикаторными значенииями и трендом на рынке.

Uber-Task — найти все возможные линейно независимые значения и запихнуть в нейронку обучать.
## Branches
There is 1 branch now:
- [master](https://github.com/omelched/exmo-bot/tree/master) — stable branch
## Launch
Для запуска необходимо иметь установленный интерпретатор python, версии не ниже 3.7 (версии ниже ещё не тестировались).
Процесс запуска:
1.  Скачать ветку;
2.  ~~Запустить в IDE~~ Выполнить команду оболочки `python main.py`.
## Использование
Вызов команд происходит в виде строки формата `<имя_команды>:<агрументы(опционально)>` без кавычек соответственно.
- Сервер
  - `plot` - обновить файл графика
  - `show` - ~~показать график~~ (отключена - графики всегда выгружаются в файл пока что)
  - `print` - напечатать аналитические данные
  - `q` - выключить программу
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
## TO-DO
TO-DO list may be found in [TO-DO.md](TO-DO.md)