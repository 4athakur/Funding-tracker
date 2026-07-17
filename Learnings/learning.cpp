#include<iostream>
#include<typeinfo>
using namespace std;

class mango{
    public:
    int id;
    void display(){
        cout << "id:1 " << id << endl;
    }
    string name;
};


int main(){
    mango m1;
    mango var=mango();
    int id = 4;
    var.display();
    cout << typeid(var).name() << endl;
        cout << typeid(var).name() << endl;

    return 0;
}