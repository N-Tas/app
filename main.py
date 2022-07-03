import uvicorn
import asyncio
from fastapi import FastAPI, status, HTTPException, Depends
from components import polynomial_components as pc
from components import backgroud_manager as bgm
from sqlalchemy.orm import Session
from database import db_connection
from database import db_crud
from database import db_models

# Create metadata 
tags_metadata = [
    {
        "name": "post",
        "description": "Set the polynomial values for calculation.",
    },
    {
        "name": "get_all",
        "description": "Get all polynomials from the database.",
    },
    {
        "name": "get_id",
        "description": "Get the polynomial behind the ID from the database.",
    },]

db_models.Base.metadata.create_all(bind=db_connection.engine)
background_manager = bgm.BGManager(db_connection.session_local)
app = FastAPI(openapi_tags=tags_metadata)


# Dependency
def get_db():
    db = db_connection.session_local()
    try:
        yield db
    finally:
        db.close()


# Run main on startup. 
# Create a new asynchronous task
@app.on_event('startup')
async def app_startup():
        asyncio.create_task(background_manager.run_main())
        
# Add new polynomial to the db and queue
# Return an ID of the newly inserted polynomial
@app.post("/polynomial", status_code=status.HTTP_201_CREATED, tags=["post"])
def insert_polynomial(model_ce : pc.CubicEQN, db : Session = Depends(get_db)):
    id = db_crud.create_polynomial(db= db, model_ce= model_ce)
    if id == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DB or Table not found")
    else:
        background_manager.put(model_ce,id)
        return id

# Get a single polynomial with the passed id        
@app.get("/polynomial/{id}", tags=["get_id"])
def get_single_polynomial(id : int, db : Session = Depends(get_db)):
    polynomial = db_crud.get_polynomial(db= db, id= id)
    if polynomial == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")
    else:
        return polynomial

# Get all polynomials 
@app.get("/polynomial",tags=["get_all"])
def get_list_of_polynomials(db : Session = Depends(get_db)):
    polynomial_lst = db_crud.get_polynomial(db= db)
    if polynomial_lst == None or polynomial_lst == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No items found")
    else:
        return polynomial_lst

# Run uvicorn 
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", 
                port=8000, reload=True, 
                access_log=False)