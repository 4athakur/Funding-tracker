from pydantic import BaseModel

class emp(BaseModel):
    name: str
    age: int
    weight: float
    married: bool

def insert_emp_data(emp: emp):
    print(emp.name)
    print(emp.age)
    print('Data Inserted')

obj=emp()
insert_emp_data()
# obj.name='amit'
# obj.age=2
# insert_emp_data('laku',12)