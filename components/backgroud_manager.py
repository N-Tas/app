import asyncio
import threading
import queue
from .polynomial_components import Bindigns, DummyBindings, CubicEQN, Pair
from database import db_crud

        
# -------------------------------------------------------------------
# Manages the queue & com. to the DB
# Works in the background
# -------------------------------------------------------------------
class BGManager:
# -------------------------------------------------------------------
# PRIVATE
# -------------------------------------------------------------------  
    def __init__(self, session):
        self.calc_queue = queue.Queue()
        self.bindings = DummyBindings()
        self.first_call = True 
        self.session_local = session
        self.DECIMAL_POINT = 4
        
    # Call the C++ lib, compute and update the db
    def __worker(self):
        while True:
            # Wait if the q is empty get item from the q 
            item = self.calc_queue.get()
            # INFO LOG
            print("-----------------------------------------------------------")
            print("Computing:")
            print("ID: {id}".format(id= item.id))
            print("Polynomial: {poly}".format(poly= item.model_ce))
            print("-----------------------------------------------------------")
            # Compute with the C++ lib
            result,compute_time = self.bindings.polynomial_calc(item.model_ce) 
            # Round the result 1/10000
            result = round(result,self.DECIMAL_POINT)
            # Update the polynomial with the computed result over its ID
            db = self.session_local()
            db_crud.update_polynomial(db= db, id= item.id, result= result)
            # INFO LOG
            print("-----------------------------------------------------------")
            print("Computed in {c_time} sec.:".format(c_time= compute_time))
            print("ID: {id}".format(id= item.id))
            print("Result: {res}".format(res= result))
            print("-----------------------------------------------------------")
            # Pop the computed item from the q
            self.calc_queue.task_done()                  
# -------------------------------------------------------------------
# PUBLIC 
# -------------------------------------------------------------------       
    # Insert the polynomial from the POST
    # Put the Cubical with its ID in the queue
    def put(self, model_ce : CubicEQN, id):    
        self.calc_queue.put(Pair(id,model_ce))  
         
    # Call main
    async def run_main(self):
        # Threads for worker. Added 2 for faster computation 
        threading.Thread(target=self.__worker, daemon=True).start()
        threading.Thread(target=self.__worker, daemon=True).start()   
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
             
        # Retrieve all not computed polynomials from the DB and put those in a queue
        # Run once on object creation
        if self.first_call:
            db = self.session_local()
            lst_sql_content = db_crud.get_polynomial(db= db,only_null= True)
            if lst_sql_content:
                for elem in lst_sql_content:
                    row_id = int(elem.get_val("id"))
                    row_x = elem.get_val("x")
                    row_polynomial = elem.get_val("polynomial")
                    model_ce = CubicEQN(x= row_x, polynomial= row_polynomial)
                    print(model_ce)
                    self.calc_queue.put(Pair(row_id,model_ce))      
            self.first_call = False
        while True:
            # await to finish 
            await asyncio.sleep(0.1)
            