# Airflow ETL Pipeline: User Events
<img width="640" height="256" alt="image" src="https://github.com/user-attachments/assets/bdd283c1-644f-49dc-aebc-ead226169572" />

### 1-2. Ознакомиться с метаданными на странице Kaggle. Прочитать данные.

Данные взяты из Kaggle:  
[https://www.kaggle.com/retailrocket/ecommerce-dataset](https://www.kaggle.com/retailrocket/ecommerce-dataset).
##### Загрузил и прочитал данные, сделал мини еда для понимания датасета `eda.ipynb`. Сделал заметки и выводы по структуре нашего датасета для дальнейшего создания таблицы в базе данных.


### 3. Очистка и инициализация БД
##### Скрипт `scripts/clean_data.py` реализует построчную обработку файла чанками по 50k строк, чтобы работать с большим объёмом без переполнения памяти.
##### На этом этапе заполняются пропуски в `brand` и `category_code`, а строки без `user_session` удаляются.
##### Результат сохраняется в `/opt/airflow/data/cleaned_user_events.csv`, который используется для последующей загрузки.
##### Структура таблицы `user_events` описана и создаётся в `scripts/init_table.py`.
##### После инициализации, чистки данных, script `load_to_postgres.py` загружает наши чистые данные в postgres.

### 4. Аналитика через SQL.
##### Файл `scripts/run_analytics.py` запускает три SQL-запроса к PostgreSQL: топ-3 продукта по продажам в месяц, топ-10 пользователей по росту покупок и товары с высокой корзиной при низкой конверсии.
##### Итоги выгружаются в CSV в каталоге `data/`.


### 5. Оркестрация через Airflow.
##### DAG `dags/upload_csv_dag.py` последовательно вызывает задачи `init_table → clean_data → load_csv → run_analytics`, обеспечивая end-to-end процесс.

## Структура репозитория
- `dags/` — DAG Airflow.
- `scripts/` — Python-скрипты подготовки, загрузки и аналитики.
- `data/` — исходный CSV и итоговые отчёты.
- `docker-compose.yml`, `entrypoint.sh`, `.env` — окружение для Airflow и PostgreSQL.

## Коротко и пошагово что делает наш код:
	1.	Читаем большой CSV
	2.	Чистим данные
	3.	Сохраняем в новый файл
	4.	Создаём таблицу в БД
	5.	Загружаем данные в таблицу
	6.	Запускаем SQL-запросы
	7.	Сохраняем результаты в CSV
	8.	Всё выполняет Airflow


