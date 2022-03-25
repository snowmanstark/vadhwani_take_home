from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from agro.upload import uploadData
from agro.view import viewData

app = FastAPI(
        title="Cotton Farmer Backend", 
        description= "All the APIs that are used in the Cotton Farmer app"
    )

app.mount("/static", StaticFiles(directory="./agro/static"), name="static")


app.include_router(uploadData.router)
app.include_router(viewData.router)


@app.get("/")
def view_farmer_data():
    return RedirectResponse("/upload")