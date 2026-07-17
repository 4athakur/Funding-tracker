class First:
    # class ke andar decorator define
    @staticmethod
    def announce(fun):
        def wrapper(*args, **kwargs):
            print("starting")
            result = fun(*args, **kwargs)
            print("Finished")
            return result
        return wrapper


# object create
obj = First()
# obj.event()

@obj.announce
def add(x,y):
    print(x+y)

print(dir(First))
add(3,4)

