from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager


from apscheduler.schedulers.background import BackgroundScheduler
from cron.update_pincode_data import pincode_update_job
from utils import read_json_file



scheduler = BackgroundScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(
        func=pincode_update_job,
        trigger="cron",
        hour=0,
        minute=0,
        id="pincode_update_job",
        replace_existing=True,
    )
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)


template = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return template.TemplateResponse(
        request=request,
        name="404.html",
        context={"message": "Page not found"},
        status_code=404,
    )


@app.get("/root/health")
async def root() -> dict[str, str]:
    return {"message":"Application working", "status":"ok"}


@app.get("/")
async def home(req: Request):
    return template.TemplateResponse(request=req, name="pages/home.html")


@app.get("/api-docs")
async def api_docs(req: Request):
    return template.TemplateResponse(request=req, name="pages/api.html")


@app.get("/sdk-docs")
async def sdk_docs(req: Request):
    return template.TemplateResponse(request=req, name="pages/sdk.html")


@app.get("/api/v1/pincode")
async def fetch_code_data(q:str):
    result = read_json_file(pincode=q)
    return result