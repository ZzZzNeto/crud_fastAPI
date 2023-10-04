import datetime, time
from fastapi import FastAPI, Request
from fastapi_sqlalchemy import DBSessionMiddleware
from app.router.library_routes import router

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url="sqlite:///banco_de_dados.db")

app.include_router(router, prefix="/books")

@app.middleware("http")
async def log(request: Request, call_next):
    with open("app/log.txt", "a") as log:
        log.write(f"ACCESS - {datetime.date.today()} | {datetime.datetime.now().strftime('%H:%M:%S')}\n   {request.method}: {request.url}\n")

    response = await call_next(request)
    return response