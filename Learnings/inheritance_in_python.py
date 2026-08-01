class emp:
    def __init__(self):
        self.name='amit'
class person(emp):
    id=1
    def info(self):
        print('id is ',self.id)  
class three(person):
    a='a'
aa=emp()
a=three()
print(aa.name)
# a.i()
# a.info()
# print(a.a)



