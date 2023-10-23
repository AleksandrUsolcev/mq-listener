from fastapi import FastAPI

from internal.config import settings
from sockets.routers import router as router_sockets

app = FastAPI()


app.include_router(router_sockets)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host=settings.WS_HOST, port=settings.WS_PORT)
