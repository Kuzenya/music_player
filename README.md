# PR4 — Music Player: статический и динамический анализ

Проект содержит три независимые версии:

- `original` — рабочая версия без намеренных ошибок;
- `static_defects` — пять ошибок для повторного статического анализа;
- `dynamic_defects` — три ошибки, выбираемые отдельными сценариями.

Не объединяйте версии и не исправляйте ошибки до завершения эксперимента.

## 1. Установка

Нужен Python 3.10 или новее. Из корня распакованного проекта выполните:

```bash
python -m pip install -r requirements-analysis.txt
```

Если команда называется `python3`, используйте `python3 -m pip ...`.

Проверка:

```bash
python --version
python -m pylint --version
python -m ruff --version
python -m bandit --version
```

`cProfile` и `tracemalloc` входят в состав Python, отдельная установка не нужна.

## 2. Проверка исходной версии

```bash
cd original
python -m unittest discover -s tests -v
python main.py --demo
python analysis_runner.py --scenario baseline --iterations 1000
```

Ожидается: 19 тестов пройдены, демонстрация и нагрузочный сценарий завершаются без ошибок.

## 3. Статический анализ до внесения ошибок

Из каталога `original`:

```bash
python -m pylint music_player.py main.py analysis_runner.py memory_profiler.py > ../results/static_before/pylint.txt 2>&1
python -m ruff check music_player.py main.py analysis_runner.py memory_profiler.py > ../results/static_before/ruff.txt 2>&1
python -m bandit music_player.py main.py analysis_runner.py memory_profiler.py > ../results/static_before/bandit.txt 2>&1
```

Ненулевой код завершения Pylint/Ruff/Bandit при наличии сообщений не означает сбой эксперимента. Сохраните вывод полностью.

## 4. Статический анализ после внесения ошибок

Перейдите в `static_defects` и выполните те же проверки:

```bash
cd ../static_defects
python -m pylint music_player.py main.py analysis_runner.py memory_profiler.py > ../results/static_after/pylint.txt 2>&1
python -m ruff check music_player.py main.py analysis_runner.py memory_profiler.py > ../results/static_after/ruff.txt 2>&1
python -m bandit music_player.py main.py analysis_runner.py memory_profiler.py > ../results/static_after/bandit.txt 2>&1
```

Намеренные ошибки находятся в `music_player.py`:

| Код | Ошибка | Ожидаемое обнаружение |
|---|---|---|
| S1 | Неиспользуемая `temporary_counter` в `play()` | Pylint, Ruff |
| S2 | Голый `except` в `unsafe_command()` | Pylint, Ruff |
| S3 | Небезопасный `eval()` | Pylint, Ruff, Bandit |
| S4 | Код после `return` в `unreachable_example()` | Pylint |
| S5 | `next_track()` использует шаг 2 вместо 1 | Обычно не обнаруживается статически |

Не запускайте unittest для этой версии как критерий статического анализа: S5 ожидаемо нарушает часть тестов.

## 5. Динамический анализ до ошибок

Из каталога `original`:

```bash
cd ../original
python -m cProfile -s cumulative analysis_runner.py --scenario performance --iterations 5000 > ../results/dynamic_before/cprofile_performance.txt
python memory_profiler.py --scenario memory --iterations 50000 > ../results/dynamic_before/tracemalloc_memory.txt
python analysis_runner.py --scenario baseline --iterations 20000 > ../results/dynamic_before/baseline_run.txt
```

Сохраните время выполнения, наиболее затратные функции, текущую и пиковую память.

## 6. Динамический анализ после ошибок

### D1. Исключение из-за удалённой проверки пустого списка

```bash
cd ../dynamic_defects
python analysis_runner.py --scenario exception > ../results/dynamic_after/exception.txt 2>&1
```

Ожидается `TypeError` в `_move()`: к `None` прибавляется индекс. Сохраните traceback полностью.

### D2. Рост памяти из-за бесконечной истории

```bash
python memory_profiler.py --scenario memory --iterations 50000 > ../results/dynamic_after/tracemalloc_memory.txt
```

Сравните с `dynamic_before/tracemalloc_memory.txt`. В дефектной версии каждый `play()` сохраняет название трека в `_history`.

### D3. Лишняя работа при переключении трека

```bash
python -m cProfile -s cumulative analysis_runner.py --scenario performance --iterations 5000 > ../results/dynamic_after/cprofile_performance.txt
```

В отчёте должен быть виден вклад `_waste_cycles()`. Сравнивайте только запуски с одинаковым числом итераций.

## 7. Что передать для составления отчёта

1. Все файлы из четырёх подкаталогов `results`.
2. Скриншоты терминала для статических проверок до/после — желательно по одному на инструмент и версию.
3. Скриншот или текст traceback для D1.
4. Скриншоты/текст результатов tracemalloc для исходной и дефектной версии.
5. Скриншоты/текст cProfile для производительности до/после.
6. Краткая таблица: какие ошибки нашёл каждый инструмент и какие сообщения вы считаете ложными срабатываниями.
7. Версии Python и ОС.

Лучше передать саму папку `results` архивом, а скриншоты назвать понятно, например `python_ruff_after.png`.
