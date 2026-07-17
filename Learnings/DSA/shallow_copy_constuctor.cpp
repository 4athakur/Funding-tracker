#include<iostream>
using namespace std;

class Test{
    public:
    int id;
    int *data;
    Test(int data){
        this->data= new int(data);
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