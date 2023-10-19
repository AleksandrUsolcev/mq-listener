from fastapi import APIRouter

from config import settings
from queues.publisher import send_message
from queues.schemas import Content

router = APIRouter(
    tags=['Очереди']
)


@router.post('/queue_reverse_text', summary='Текст')
async def post_queue_text(content: Content):
    """Отправляет текст в очередь rabbitmq."""
    await send_message(
        message=content.text,
        routing_key=settings.RABBITMQ_QUEUE_NAME
    )
    return {'result': 'Text successfully sent to queue'}
