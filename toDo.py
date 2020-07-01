import uvicorn, secrets
import database
from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates



templates = Jinja2Templates(directory = "templates")


app = FastAPI()


@app.get("/")
def authenticate(request : Request):
	return templates.TemplateResponse("signIn.html", {
		"request" : request
	})


@app.get("/signup")
async def signUp(request : Request):
	print("h]ellooo")
	return templates.TemplateResponse("signUp.html", {
		"request" : request
	})



@app.get("/insert")
async def insert_page(request : Request):
	return templates.TemplateResponse("layout1.html", {
		"request" : request
	})


@app.get("/wrong_login")
async def disp(request : Request):
	return templates.TemplateResponse("incorrect_login.html", {
		"request" : request
	})
	

@app.websocket("/signIn")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        coll = database.getUser_collec()
        result = await coll.find_one(data)
        if result is None: await websocket.send_text("wrong credentials")
        else: await websocket.send_text("wright credentials")

@app.websocket("/signUp")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        coll = database.getUser_collec()
        result = await coll.insert_one(data)
        await websocket.send_text("Sign up successful")


@app.get("/insert/{name}/{desc}")
async def insert_item(request : Request, name, desc):
	coll = database.getTodo_collec()
	document = {'name': name, 'desc': desc}
	result = await coll.insert_one(document)
	return templates.TemplateResponse("layout1.html", {
		"request" : request
	})
	
	
	
		
@app.get("/update")
async def getUpdate(request : Request):
    return templates.TemplateResponse("layout2.html", {
		"request" : request
	})


   
@app.get("/update/{old_name}/{old_desc}/{new_name}/{new_desc}")
async def update_item(request : Request, old_name, old_desc, new_name, new_desc):
	
	coll = database.getTodo_collec()
	doc = await coll.find_one({'name': old_name})
	
	if new_name is not None: name = new_name
	else: name = old_name
	if new_desc is not None: desc = new_desc
	else: 
		if old_desc is not None: desc = old_desc
		else: desc = doc['desc']
 		
	result = await coll.update_one({'_id': doc['_id']}, {'$set': {'name': name, 'desc': desc}})
	return templates.TemplateResponse("layout1.html", {
		"request" : request
	})

    
@app.get("/delete/{name}/{desc}")
async def delete_item(request : Request, name, desc):

	coll = database.getTodo_collec()
	result = await coll.delete_many({'name': name, 'desc' : desc})
	return templates.TemplateResponse("layout1.html", {
		"request" : request
	})

if __name__ == "__main__":
    uvicorn.run("toDo:app", host="127.0.0.1", port=5000, log_level="info")
