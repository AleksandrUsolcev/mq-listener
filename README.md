# mq-listener

Простой пример взаимодействия с rabbitmq, состоящий из нескольких сервисов:
- [api](/api/) - отправка сообщений в очередь rabbitmq;
- [consumer](/consumer/) - чтение очереди rabbitmq с обработкой входящих сообщений и последующей отправкой на websocket канал;
- [ws](/ws/) - websocket сервер, на котором подключенный клиент пассивно получает результаты обработанных сообщений.

## Запуск проекта

Клонировать репозиторий, перейти в `mq-listener/` и копировать переименованный в **.env** [образец](example.env) файла переменного окружения

```bash
git clone https://github.com/AleksandrUsolcev/mq-listener.git
cd mq-listener/
cp example.env .env
```

Для ознакомления, в **.env** уже доступны базовые рабочие значения. При необходимости меняем значения на свои

```bash
vi .env
```

Разворачиваем докер контейнеры

```bash
docker compose up -d
```

## Применение

Далее по тексту хосты и порты указаны с учетом того, что при запуске проекта переменные окружения остались [по умолчанию](example.env).

После успешного запуска проекта подключаемся к websocket эндпоинту (порт в примере из дефолтных значений) `ws://localhost:8001/listen_results`, на который в дальнейшем будут приходить результаты обработанных сообщений из очереди rabbitmq.

Для отправки сообщений необходимо отправить POST запрос на api эндпоинт `http://localhost:8000/queue_reverse_text` со следующим форматом содержимого:

```json
{
  "text": "my text"
}
```

Так же сообщение можно отправить из формы со swagger'а `http://localhost:8000/docs`

При отправке сообщения можно воспользоваться параметром **use_celery** для отправки текста через активный celery воркер, предотвращая потери и сохраняя очередность отправки, в случае если сервис rabbitmq недоступен. Посмотреть состояние задач в воркере можно во flower `http://localhost:5555/`

> Для подключения к ws и api эндпоинту так же можно воспользоваться [приложенными скриптами](https://github.com/AleksandrUsolcev/mq-listener/tree/main/for_example).

После отправки сообщение переходит в персистентную очередь rabbitmq, откуда в дальнейшем переходит в обработку при получении [consumer](/consumer/main.py)'ом. После успешного получения и обработки* отправляется сообщение на наш ws канал со следующим содержимым (с учетом примера выше):

```json
{
  "reversed_text": "txet ym"
}
```

В случае если по каким-либо причинам наш consumer не запущен, сообщения остаются в очереди со статусом "Unacked" в нашей очереди rabbitmq, до тех пор пока consumer не будет снова поднят. Ознакомиться со статусом очереди и не только, можно панели администратора `http://localhost:15672/`

*_В данном примере реверс текста служит лишь для простой наглядности работы обработчика, само собой можно написать свой._

## Автор

[Александр Усольцев](https://github.com/AleksandrUsolcev)
