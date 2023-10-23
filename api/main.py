from fastapi import FastAPI

from internal.config import settings
from queues.routers import router as router_queues

app = FastAPI()

app.include_router(router_queues)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
