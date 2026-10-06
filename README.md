# Умный дом

## Техническая задача: реализовать чтение данных датчиков, используя Django Rest Framework

**REST API** — архитектурный стиль, при котором приложение предоставляет данные по HTTP-запросам (например, `GET`) в формате JSON. Подробнее: https://ru.wikipedia.org/wiki/REST.

## Описание

У нас есть программируемые датчики, измеряющие температуру. Они хранят свои показания на сервере. Необходимо реализовать REST API, которое позволяет **получать данные** о датчиках и их измерениях.

Требуется задать две модели — они уже описаны в `models.py`:

- датчик:

  - название,
  - описание (необязательное, например, «спальня» или «коридор на 2 этаже»).

- измерение температуры:

  - ID датчика (внешний ключ),
  - температура при измерении,
  - дата и время измерения.

Для сериализаторов используйте `ModelSerializer`.

---

## Реализованно в проекте

Запросы, которые должны быть реализованы в системе (только чтение данных):

1. Получение списка датчиков. Выдаётся список с краткой информацией по датчикам: ID, название и описание.

```json
[
  {
    "id": 2,
    "name": "ESP32",
    "description": "Датчик на кухне за холодильником"
  },
  {
    "id": 1,
    "name": "ESP32",
    "description": "Датчик в спальне"
  }
]
```

2. Получение информации по конкретному датчику. Выдаётся полная информация по датчику: ID, название, описание и список всех измерений с температурой и временем.

```json
{
  "id": 1,
  "name": "ESP32",
  "description": "Датчик в спальне",
  "measurements": [
    {
      "temperature": 22.3,
      "created_at": "2021-10-23T16:44:51.432328Z"
    },
    {
      "temperature": 22.5,
      "created_at": "2021-10-23T16:45:51.091212Z"
    }
  ]
}
```


## Основные изменения

1. Изменены файлы `models.py`, `serializers.py`, `views.py` и `urls.py`.

2. Для автоматического проставления времени измерения использован аргумент `auto_now_add` (проставляется при создании).

3. Для сериализатора с подробной информацией по датчику (отображение списка измерений) используется [вложенный сериализатор](https://www.django-rest-framework.org/api-guide/serializers/#dealing-with-nested-objects). Получился такой код:

```python
class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['temperature', 'created_at']


class SensorDetailSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']
```

4. Для обработки только чтения использованы готовые generic-классы DRF: `ListAPIView` (вывод списка) и `RetrieveAPIView` (вывод одного объекта). Задействованы поле `queryset` и атрибут `serializer_class`.

## Дополнительные задания

### Прикрепление картинки к измерению

Датчики стали более продвинутыми и могут также прикреплять снимки. Добавлены nullable-поле к модели `Measurement` для сохранения изображений. https://www.django-rest-framework.org/api-guide/fields/#imagefield

Поле опциональное — некоторые датчики прикладывают фото, а некоторые — нет. Для старых датчиков ничего не ломается.

## Документация по проекту

Для запуска проекта необходимо установить зависимости:

```bash
pip install -r requirements.txt
```
Настроить подключение к PostgreSQL в `settings.py` и указать пароль базы данных в переменной окружения `DB_PASSWORD`.

```powershell
$env:DB_PASSWORD = "ваш_пароль_от_postgres"
```

Применить миграции и загрузить тестовые данные:

```bash
python manage.py migrate
python manage.py loaddata sample_data
```

Выполнить команду:

```bash
python manage.py runserver
```
