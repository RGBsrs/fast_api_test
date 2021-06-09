from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx
from starlette.requests import Request

app = FastAPI()
client = httpx.AsyncClient()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    drinks_list = httpx.get('https://www.thecocktaildb.com/api/json/v1/1/list.php?c=list')
    drinks = drinks_list.json()['drinks']
    result_group = {}
    for drink in drinks:
        result = await client.get(f'https://www.thecocktaildb.com/api/json/v1/1/filter.php?c={ drink["strCategory"] }')
        result_group[drink["strCategory"]] = result.json()['drinks']  
    return templates.TemplateResponse("gallery.html", {"request": request, 'results' : result_group})