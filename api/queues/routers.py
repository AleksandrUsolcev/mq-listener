from fastapi import APIRouter

from queues.schemas import Content

router = APIRouter(
    tags=['Очереди']
)


@router.post('/queue_reverse_text', summary='Текст')
def post_queue_text(content: Content):
    """Отправляет текст в очередь rabbitmq."""
    print(content.text)
    return {'result': 'Text successfully sent to queue'}
