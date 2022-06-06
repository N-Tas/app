from sqlalchemy import Sequence, Column, REAL, Integer
from .db_connection import Base

# -------------------------------------------------------------------
# Model for the DB 
# -------------------------------------------------------------------
class Model_CE(Base):
    # Table name in the DB
    __tablename__ = "plynomials_table"
    # Columns in the table
    id = Column(Integer, Sequence('ploynomial_id_seq'), primary_key=True)
    x = Column(REAL)
    a0 = Column(REAL)
    a1 = Column(REAL)
    a2 = Column(REAL)
    a3 = Column(REAL)
    result = Column(REAL)
    # Constructor when passing an object to the DB 
    def __init__(self, x, a0, a1, a2, a3):
        self.x = x
        self.a0 = a0
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.result = None
    # Returns the ID  
    def get_id(self):
        return self.id