import uvicorn
from fastapi import FastAPI, Request, Depends, BackgroundTasks, WebSocket
from fastapi.responses import HTMLResponse
import motor.motor_asyncio
from typing import Optional


app = FastAPI()




html = """
<!DOCTYPE html>
<html>
    <head>
        <title>ToDo</title>
    </head>
    <body>
        <h1>Insert your Todo</h1>
        <input type="text" id="name" autocomplete="off" placeholder="enter name"/>
        <input type="text" id="desc" autocomplete="off" placeholder="enter desc"/>
        <button onclick="addToDo()">Create</button>
        <button onclick="deleteToDo()">Delete</button>
        <button onclick="update()">Update</button>
		<p>
		<ul>
			<li>create: enter new name and description of toDo and click create,</li>
			<li>update: click on update button to edit toDo,</li>
			<li>delete: enter name and description of toDo and click delete,</li> 	
		</ul>
		</p>
        <script>
        	function addToDo() {
        		name = document.getElementById("name").value
            	desc = document.getElementById("desc").value
				window.location = "http://127.0.0.3:5000/insert/" + name + "/" + desc;
            }
			function update(){
				window.location = "http://127.0.0.3:5000/update"
			}
			function updateToDo() {
        		name = document.getElementById("name").value
            	desc = document.getElementById("desc").value
				window.location = "http://127.0.0.3:5000/update/" + name + "/" + desc;
            }
			function deleteToDo() {
        		name = document.getElementById("name").value
            	desc = document.getElementById("desc").value
				window.location = "http://127.0.0.3:5000/delete/" + name + "/" + desc;
            }
                name.value = ''
                desc.value = ''
        </script>
    </body>
</html>

"""


html2 = """
<!DOCTYPE html>
<html>
    <head>
        <title>ToDo</title>
    </head>
    <body>
        <h1>Insert your Todo</h1>
        <input type="text" id="old_name" autocomplete="off" placeholder="enter old_name"/>
        <input type="text" id="old_desc" autocomplete="off" placeholder="enter old_desc"/>
		<br>
        <input type="text" id="new_name" autocomplete="off" placeholder="enter new_name"/>
        <input type="text" id="new_desc" autocomplete="off" placeholder="enter new_desc"/>
		<br>
		<button onclick="updateToDo()">Update</button>
		<p>
		click on update after entering name of toDo (description if needed)
		</p>
        <script>
			function updateToDo() {
        		old_name = document.getElementById("old_name").value
            	old_desc = document.getElementById("old_desc").value
				new_name = document.getElementById("new_name").value
            	new_desc = document.getElementById("new_desc").value
				window.location = "http://127.0.0.3:5000/update/" + old_name + "/" + old_desc + "/" + new_name + "/" + new_desc;
            }
        </script>
    </body>
</html>

"""
	

@app.get("/update")
async def getUpdate():
    return HTMLResponse(html2)




@app.get("/")
async def get():
    return HTMLResponse(html)




@app.get("/insert/{name}/{desc}")
async def insert_item(name, desc):
	client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
	db = client.toDo
	document = {'name': name, 'desc': desc}
	result = await db.toDo_collec.insert_one(document)
	print('result %s' % repr(result.inserted_id))
	return HTMLResponse(html)


   
@app.get("/update/{old_name}/{old_desc}/{new_name}/{new_desc}")
async def update_item(old_name, old_desc, new_name, new_desc):
	client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
	db = client.toDo
	
	coll = db.toDo_collec
	doc = await coll.find_one({'name': old_name})
	
	if new_name is not None: name = new_name
	else: name = old_name
	if new_desc is not None: desc = new_desc
	else: 
		if old_desc is not None: desc = old_desc
		else: desc = doc['desc']
 		
	result = await coll.update_one({'_id': doc['_id']}, {'$set': {'name': name, 'desc': desc}})
	return HTMLResponse(html)

    
@app.get("/delete/{name}/{desc}")
async def delete_item(name, desc):

	client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
	db = client.toDo
	result = await db.toDo_collec.delete_many({'name': name, 'desc' : desc})
	return HTMLResponse(html)

if __name__ == "__main__":
    uvicorn.run("toDo:app", host="127.0.0.3", port=5000, log_level="info")

