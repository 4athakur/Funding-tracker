def student():
    print("i'm student")
def new():
    print('i m new')
def teacher(later):
    print("teacher")
    later()
    student()
    print("techer gaya")
teacher(new)