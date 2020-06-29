import uvicorn
from fastapi import FastAPI, Request, Depends, BackgroundTasks, WebSocket
from fastapi.responses import HTMLResponse
import motor.motor_asyncio


app = FastAPI()
	

@app.get("/insert")
async def insert_item(name, desc):
	client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
	db = client.toDo
	document = {'name': name, 'desc': desc}
	result = await db.toDo_collec.insert_one(document)
	print('result %s' % repr(result.inserted_id))


   
@app.put("/update")
async def update_item(name = None, new_desc = None):
	client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
	db = client.toDo
	
	coll = db.toDo_collec
	#doc = await coll.find_one({'name': old_name})
	
	#name = new_name if new_name is not None else old_name
	#desc = new_desc if new_desc is not None else old_desc
		
	result = await coll.update_one({'name': name}, {'$set': {'desc': new_desc}})
    
    
@app.put("/delete")
async def delete_item(name):

	client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
	db = client.toDo
	
	result = await db.toDo_collec.delete_many({'name': name})


if __name__ == "__main__":
    uvicorn.run("toDo:app", host="127.0.0.3", port=5000, log_level="info")

