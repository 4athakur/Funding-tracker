class person:
    name='amit'
    age=23
    def change_name(self):
        self.name="rahul"
    # def person():
    #     print("Constructor CALLED")
    def __init__(self,name, age):
        self.name=name
        self.age=age
        print(f"Constructor Called {self.name} and age is {self.age}")
obj=person("rana",12)
obj.change_name()
# obj.name='mannat'
print(obj.name, "is a  king age of ",obj.age)

obj2=person("rahul",10)
obj3=person("anil",11)