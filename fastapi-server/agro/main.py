from multiprocessing import context
from re import template
from fastapi import FastAPI, Request, File,  UploadFile
from fastapi.responses import HTMLResponse, Response
# from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import csv
from io import StringIO

app = FastAPI()


app.mount("/static", StaticFiles(directory="./agro/static"), name="static")
template = Jinja2Templates("agro/templates")

@app.get("/")
def render_upload_farmers_data_page(request: Request):
    return template.TemplateResponse("upload.html", context={"request":request})

@app.post("/upload")
def upload_farmer_data(file: UploadFile = File(...)):
    if file.filename.split(".")[-1].casefold == "csv" or file.content_type == "text/csv":
        buffer = StringIO(file.file.read().decode())
        file = csv.DictReader(buffer)
        for line in file:
            print(line)
        return Response(status_code=200,content="CSV uploaded successfully")
    else:
        return Response(status_code=422,content="Invalid file type!! Please upload a CSV file")

