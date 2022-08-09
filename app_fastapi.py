import uvicorn
from fastapi import FastAPI, Request, Form, Depends, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import *
from scrapfromfacebook import FaceBookBot

FaceBookBot=FaceBookBot()
username=""

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/basic', response_class=HTMLResponse)
def get_basic_form(request: Request):
    return templates.TemplateResponse("basic-form.html", {"request": request})

@app.post('/basic', response_class=HTMLResponse)
async def post_basic_form(request: Request, username: str = Form(...)):

    print(f'username: {username}')
    
    data=FaceBookBot.find_url(40,'{}'.format(username))
    createtable(username)
    print(data)
    savedata(data,username)
    con.close()

    return templates.TemplateResponse("basic-form.html", {"request": request})


if __name__ == '__main__':

    uvicorn.run(app)