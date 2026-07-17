#include<iostream>
#define overflow 1
#define INVALID_INDEX 2
#define UNDERFLOW 3
using namespace std;

class Array{
    int capacity;
    int lastIndex;
    int *ptr;
    public:
    Array(int size){
        printf("Enter the size of an Array !\n");
        capacity = size;
        lastIndex = -1;
        ptr=new int[capacity];
        }
    Array(){
        capacity=10;
        lastIndex=-1;
        ptr= new int[10];
    }
    bool isEmpty();
    void append(int data);
    bool isFull();
    void insert(int,int);
    void edit(int index, int new_data);
    void del(int index);
    int get_element(int index);
    int size_of_array();
    int get_capacity();
    ~Array(){
        delete []ptr;
    }
    int find(int data);
    };
int Array::find(int data){
    for(int i=0;i<=lastIndex;i++){
        if(ptr[i]==data){
            return i;
        }
    return -1;
    }
}
int Array::get_capacity(){
    return capacity;
}
int Array::size_of_array(){
    return lastIndex+1;
}
int Array::get_element(int index){
    if(index<0 || index>lastIndex){
        throw INVALID_INDEX;
    }
    if(isEmpty()){
        throw UNDERFLOW;
    }
}
void Array::del( int index){
    if(isEmpty()){
        throw UNDERFLOW;
    }
    if(index<0 || index>lastIndex){
        throw INVALID_INDEX;
    }
    for(int i=index;i<lastIndex;i++){
        ptr[i]=ptr[i+1];
    }
    lastIndex--;
}
void Array::edit(int index,int new_data){
    if(index<0 || index>lastIndex){
        throw INVALID_INDEX;
    }
    ptr[index]=new_data;
}
void Array::insert(int index, int data){
    if(isFull()){
        throw overflow;
    }
   if(index<0 || index>lastIndex+1){
            throw INVALID_INDEX;
    for(int i=lastIndex;i>=index;i--){
        ptr[i+1]=ptr[i];
    }
    ptr[index]=data;
    lastIndex++;
   }

}
void Array::append(int data){// freind function
          if(isFull){
                throw overflow;
          }
          ++lastIndex;
          ptr[lastIndex]=data;
}
bool Array::isFull(){
    return capacity== (lastIndex+1);
}
bool Array::isEmpty(){
    return lastIndex==-1;
}
int main(){
    Array arr(4);

    int res= arr.isEmpty(arr);
    printf("%d", res);

}