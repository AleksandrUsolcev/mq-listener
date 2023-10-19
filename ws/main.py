from fastapi import FastAPI

from config import settings
from wss.routers import router as router_wss

app = FastAPI()


app.include_router(router_wss)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host=settings.WS_HOST, port=settings.WS_PORT)
