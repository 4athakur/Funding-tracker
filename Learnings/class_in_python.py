class person:
    name='amit'
    age=23
    def change_name(self):
        self.name="rahul"

obj=person()
obj.change_name()
# obj.name='mannat'

print(obj.name, "is a  king age of ",obj.age)