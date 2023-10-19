from fastapi import FastAPI

from queues.routers import router as router_queues

app = FastAPI()

app.include_router(router_queues)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
