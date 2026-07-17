#include<iostream>
using namespace std;

class Test{
    public:
    int id;
    int *data;
    Test(int data){
        this->data= new int(data);
    }
// Deep copy
     Test(const Test& other) {// here other is referencing the t1 (jo obj copy ho raha hai)
        data = new int(*other.data);  // new memory + copy value
        id = other.id;                // normal int copy
    }
    Test(const Test& other){
        data= new int(*other.data);
        id=other.id;
    }
    // Destructor
    ~Test() {
        delete data;
    }
};
int main(){
    Test t1(4);
    t1.id=1;
    Test t2=t1;
    printf("%d\n",t1.data);
    printf("%d\n",t2.data);
    // Ab t1.data aur t2.data same memory ko point kar rahe hain (it happens in case of pointer)
    //but in case of id, it is not coping the address of the id variable
      printf("%d\n",&t1.id);
    printf("%d\n",&t2.id);

}