### Приложения:
- 1. Скрипт для сбора данных по разным API
  ```excel_saver``` папка
- 2. Парсер процессоров с ситилинка ```citilink_parser``` папка
- 8. Django приложение для загрузки и обработки csv файлов ```django_csv``` папка
  
Ответы на вопросы:
- **3.md**
- **4.md**
- **5.md**
- **6.md**
- **7.md**
  
## Запуск проектов

### Клонирование всего репозитория
```bash
git clone git@github.com:voidCaloneian/colizeum_tt.git
cd colizeum_tt
```

### Сетап и запуск приложений

- 1. Скрипт для сбора данных по разным API
  ```excel_saver``` папка
  
      Во-первых, заполните .env файл в директории приложения, указав туда свои ключи от NEWSAPI и OpenWeatherMapAPi, далее выполните следующие команды:
      ```bash
      cd excel_saver
      python -m venv env
      source env/bin/activate # Либо env\Scripts\Activate на Windows
      pip install -r requirements.txt
      python main.py
      ```
      > В проекте появится готовая таблица с данными ```data.xlsx```

- 2. Парсер процессоров с ситилинка ```citilink_parser``` папка
  
      Во-первых, заполните .env файл в директории приложения, указав туда данные по GOOGLE SHEET API,
      далее выполните следующие команды:
      ```bash
      cd citilink_parser
      python -m venv env
      source env/bin/activate # Либо env\Scripts\Activate на Windows
      pip install -r requirements.txt
      python main.py
      ```
  
- 3. Django приложение для загрузки и обработки csv файлов ```django_csv``` папка
  
      Выполните следующие команды:
      ```bash
      cd django_csv
      docker compose up --build -d 
      ```
      Ждем, пока контейнеры запустятся и дальше выполняем следующие команды:
      ```bash
      docker compose exec web python manage.py makemigrations
      docker compose exec web python manage.py migrate
      ```
      Опционально можем запустить тесты
      ```bash
      docker compose exec web python manage.py test
      ```
      
      **Дополнительно запускается контейнер - локальный smtp сервер для получения писем по окончанию обработки csv файлов, в логах можно посмотреть, как он принимает письма**

      ### Эндпоинты Django приложения
      **POST** ```api/upload/```
      
      - Загрузка csv файла.

        Принимает следующие параметры:
        
        - file через multipart - сам csv файл до 100 мб
        - email - строка, куда будем отправлять email после обработки csv файла
        
        **GET** ```api/file/<int:pk>/```
      - Получение данных об обрабокте конкретного csv файла по его айдишнику, которым получаем после аплоада файла, там можно посмотреть статус обработки. Через минуту такс через Celery выполняется и статус файла меняется на completed

      Адреса Django приложения
      - ```localhost:8000``` - само приложение
      - ```localhost:5555``` - Flower UI
        
      
