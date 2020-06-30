import uvicorn, secrets
import database
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates



templates = Jinja2Templates(directory = "templates")


app = FastAPI()


@app.get("/")
def authenticate(request : Request):
	return templates.TemplateResponse("login_signup.html", {
		"request" : request
	})


@app.get("/signIn/{name}/{password}")
async def signIn(request : Request, name, password):
	coll = database.getUser_collec()
	doc = await coll.find_one({'name': name})
	if password == doc['password']: return templates.TemplateResponse("layout1.html", {
		"request" : request
	})
	else: return templates.TemplateResponse("incorrect_login.html", {
		"request" : request
	})
    


@app.get("/signUp/{name}/{password}")
async def signUp(request : Request, name : str, password : str):
	coll = database.getUser_collec()
	document = {'name': name, 'password': password}
	doc = await coll.find_one({'name': name})
	result = await coll.insert_one(document)
	return templates.TemplateResponse("layout1.html", {
		"request" : request
	})
	


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
    uvicorn.run("toDo:app", host="127.0.0.4", port=5000, log_level="info")
