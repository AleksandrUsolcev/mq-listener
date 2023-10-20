## Скрипты для базовой проверки работоспособности

Запускать после того как [контейнеры](../docker-compose.yaml) успешно подняты с [дефолтными значениями](../example.env).

Если используете [poetry](https://python-poetry.org/) то необходимые пакеты уже присутствуют в [зависимостях](../pyproject.toml). В ином случае устанавливаем виртуальное окружение, активируем и устанавливаем зависимости:

```bash
python -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
```
