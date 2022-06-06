#Create, Read, Update and Delete
from sqlalchemy.orm import Session
from components import polynomial_components as pc
from .db_models import Model_CE

# Extract all the values from the columns in the given table row
def __prep_dict(table_row):
    cubic_dict = pc.PolynomialDict()
    cubic_dict.add('id', table_row.id)
    cubic_dict.add('x', table_row.x)
    cubic_dict.add('polynomial', [table_row.a0, table_row.a1, table_row.a2, table_row.a3])
    cubic_dict.add('result',table_row.result)
    return cubic_dict

# Inserts a new polynomial into the DB
def create_polynomial(db : Session, model_ce : pc.CubicEQN):
    row_id = None
    try:
        polynomial = Model_CE(x= model_ce.x, a0= model_ce.polynomial[0], a1= model_ce.polynomial[1],
                                        a2= model_ce.polynomial[2] ,a3= model_ce.polynomial[3])
        db.add(polynomial)
        db.commit()
        row_id = polynomial.get_id()
    except:
        # INFO LOG
        print("-----------------------------------------------------------")
        print("No DB or Table found")
        print("-----------------------------------------------------------")
    finally:    
        db.close()
        return row_id

# Update the result of the selected polyomial after the heavy calc
def update_polynomial(db : Session, id, result):
    try:
        polynomial = db.query(Model_CE).filter(Model_CE.id == id).first()
        if polynomial:
            polynomial.result = result
            db.commit()
    except:
        # INFO LOG
        print("-----------------------------------------------------------")
        print("No DB or Table found")
        print("-----------------------------------------------------------")  
    finally:
        db.close() 
        
# Returns the wanted polynomial or polynomials 
# When id != None --> Return the table row (polynomial) behind the id
# When id == None and only_null = False --> Return all the table rows (polynomials)
# When id == None and only_null = True --> Return all the table rows (polynomials), where the result is Null
def get_polynomial(db : Session, id= None, only_null = False):
    response = None
    try:
        if id != None:
            row_content = db.query(Model_CE).filter(Model_CE.id == id).first()
            if row_content:
                response = __prep_dict(row_content)
        else:
            if only_null == False:
                table_content = db.query(Model_CE).order_by(Model_CE.id)
            else:
                table_content = db.query(Model_CE).filter(Model_CE.result == None)
            if table_content:
                lst_polynomials = []
                for row in table_content:
                    lst_polynomials.append(__prep_dict(row))
                response = lst_polynomials        
    except:
        # INFO LOG
        print("-----------------------------------------------------------")
        print("No DB or Table found")
        print("-----------------------------------------------------------")
    finally:
        db.close()
        return response