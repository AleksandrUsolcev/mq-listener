from fastapi import APIRouter

from internal.config import settings
from queues.schemas import Content
from services.mq_publisher import send_message
from workers.celery import send_message_to_queue

router = APIRouter(
    tags=['Очереди']
)


@router.post('/queue_reverse_text', summary='Текст')
async def post_queue_text(content: Content, use_celery: bool = False):
    """Отправляет текст в очередь rabbitmq.

    __use_celery__: отправляет текст через активный celery воркер,
    предотвращая потери и сохраняя очередность отправки,
    в случае если сервис rabbitmq недоступен.
    """
    kwargs = {
        'message': content.text,
        'routing_key': settings.RABBITMQ_QUEUE_NAME,
    }
    if use_celery:
        send_message_to_queue.delay(**kwargs)
    else:
        await send_message(**kwargs)
    return {'result': 'Text successfully sent to queue'}
