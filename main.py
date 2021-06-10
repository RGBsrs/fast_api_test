from typing import Optional
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx
from starlette.requests import Request

app = FastAPI()
client = httpx.AsyncClient()

templates = Jinja2Templates(directory="templates")
drinks_list = httpx.get('https://www.thecocktaildb.com/api/json/v1/1/list.php?c=list')
drinks = drinks_list.json()['drinks']
drinks_str = [drink['strCategory'] for drink in drinks]


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    result_group = {}
    for drink in drinks_str:
        result = await client.get(f'https://www.thecocktaildb.com/api/json/v1/1/filter.php?c={ drink }')
        result_group[drink] = result.json()['drinks']  
    return templates.TemplateResponse("gallery.html", {"request": request, 'results' : result_group, 'drinks_list': drinks_str, 'filter': drinks_str})

@app.post("/")
async def filter(request: Request):
    filtered_drinks = await request.form()
    result_group = {}
    for drink in filtered_drinks:
        result = await client.get(f'https://www.thecocktaildb.com/api/json/v1/1/filter.php?c={ drink }')
        result_group[drink] = result.json()['drinks']
    return templates.TemplateResponse("gallery.html", {"request": request, 'results' : result_group, 'drinks_list': drinks_str, 'filter': filtered_drinks})