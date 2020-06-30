import motor.motor_asyncio


def getUser_collec():
    client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
    db = client.toDo
    return db.user_collec



def getTodo_collec():
    client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
    db = client.toDo
    return db.toDo_collec